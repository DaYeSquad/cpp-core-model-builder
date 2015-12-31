#include "task_manager.h"
#include "director/director.h"

using std::string;
using std::unique_ptr;
using std::vector;

using sakura::FileUtils;


NS_LCC_BEGIN

// SQLite schema --------------------------------------------------------

static std::string const kTaskId = "task_id";
static std::string const kTitle = "title";
static std::string const kListId = "list_id";
static std::string const kProjectId = "project_id";
static std::string const kCreatedAt = "created_at";
static std::string const kCreatedBy = "created_by";
static std::string const kLastUpdatedAt = "last_updated_at";
static std::string const kPosition = "position";
static std::string const kTaskNumber = "task_number";
static std::string const kArchived = "archived";
static std::string const kCompleted = "completed";
static std::string const kDeleted = "deleted";
static std::string const kPermission = "permission";
static std::string const kNumComments = "num_comments";
static std::string const kNumAttachments = "num_attachments";
static std::string const kNumChildTasks = "num_child_tasks";
static std::string const kNumCompletedChildTasks = "num_completed_child_tasks";
static std::string const kNumLike = "num_like";
static std::string const kAssignedTo = "assigned_to";
static std::string const kAssignedBy = "assigned_by";
static std::string const kDue = "due";
static std::string const kTags = "tags";
static std::string const kWatchers = "watchers";
static std::string const kComments = "comments";
static std::string const kLikes = "likes";

static std::string const kSqlAnd = "AND";

static sql::Field definition_tasks[] = {
  sql::Field(kTaskId, sql::type_text, sql::flag_primary_key),
  sql::Field(kTitle, sql::type_text, sql::flag_not_null),
  sql::Field(kListId, sql::type_text, sql::flag_not_null),
  sql::Field(kProjectId, sql::type_text, sql::flag_not_null),
  sql::Field(kCreatedAt, sql::type_int, sql::flag_not_null),
  sql::Field(kCreatedBy, sql::type_text, sql::flag_not_null),
  sql::Field(kLastUpdatedAt, sql::type_int, sql::flag_not_null),
  sql::Field(kPosition, sql::type_int, sql::flag_not_null),
  sql::Field(kTaskNumber, sql::type_text, sql::flag_not_null),
  sql::Field(kArchived, sql::type_bool, sql::flag_not_null),
  sql::Field(kCompleted, sql::type_bool, sql::flag_not_null),
  sql::Field(kDeleted, sql::type_bool, sql::flag_not_null),
  sql::Field(kPermission, sql::type_int, sql::flag_not_null),
  sql::Field(kNumComments, sql::type_int, sql::flag_not_null),
  sql::Field(kNumAttachments, sql::type_int, sql::flag_not_null),
  sql::Field(kNumChildTasks, sql::type_int, sql::flag_not_null),
  sql::Field(kNumCompletedChildTasks, sql::type_int, sql::flag_not_null),
  sql::Field(kNumLike, sql::type_int, sql::flag_not_null),
  sql::Field(kAssignedTo, sql::type_text, sql::flag_not_null),
  sql::Field(kAssignedBy, sql::type_text, sql::flag_not_null),
  sql::Field(kDue, sql::type_int, sql::flag_not_null),
  sql::Field(kTags, sql::type_text, sql::flag_not_null),
  sql::Field(kWatchers, sql::type_text, sql::flag_not_null),
  sql::Field(kComments, sql::type_text, sql::flag_not_null),
  sql::Field(kLikes, sql::type_text, sql::flag_not_null),
  sql::Field(sql::DEFINITION_END),
};

////////////////////////////////////////////////////////////////////////////////
// TaskManager, public:

// Creation and lifetime --------------------------------------------------------

TaskManager::TaskManager(Director* director)
:ObjectManager(director) {
}

TaskManager::~TaskManager() {
}

bool TaskManager::InitOrDie() {
  bool success = true;

  do {
    tasks_tb_ = unique_ptr<sql::Table>(new sql::Table(MainDatabaseHandler(), "TaskManager", definition_tasks));

    if (!tasks_tb_->exists()) {
      success = tasks_tb_->create();
      LCC_ASSERT(success);
    }

  } while(0);

  return success;
}

const TaskManager* TaskManager::DefaultManager() {
  return Director::DefaultDirector()->task_manager();
}

// SQLite schema --------------------------------------------------------

void TaskManager::SaveTaskToCache(const Task& task) const {
  LockMainDatabase();

  UnsafeSaveTaskToCache(task);

  UnlockMainDatabase();
}

void TaskManager::SaveTasksToCache(const std::vector<std::unique_ptr<Task>>& tasks) const {
  LockMainDatabase();

  for (auto it = tasks.begin(); it != tasks.end(); ++it) {
    UnsafeSaveTaskToCache(**it);
  }

  UnlockMainDatabase();
}

std::unique_ptr<Task> TaskManager::FetchTaskFromCacheByTaskId(const std::string& task_id) const {
  string where_condition = kTaskId + "='" + task_id + "'";

  LockMainDatabase();

  tasks_tb_->open(where_condition);

  if (tasks_tb_->recordCount() != 0) {
    sql::Record* record = tasks_tb_->getRecord(0);
    unique_ptr<Task> rtn(TaskFromRecord(record));
    UnlockMainDatabase();
    return rtn;
  }

  UnlockMainDatabase();

  return nullptr;
}

std::vector<std::unique_ptr<Task>> TaskManager::FetchTasksFromCacheByProjectId(const std::string& project_id) const {

  vector<unique_ptr<Task>> tasks;

  string where_condition = kProjectId + "='" + project_id + "'";

  LockMainDatabase();

  tasks_tb_->open(where_condition);

  for (int i = 0; i < tasks_tb_->recordCount(); ++i) {
    sql::Record* record = tasks_tb_->getRecord(i);
    tasks.push_back(TaskFromRecord(record));
  }

  UnlockMainDatabase();

  return tasks;
}

std::vector<std::unique_ptr<Task>> TaskManager::FetchTasksFromCacheByAssignedTo(const std::string& assigned_to) const {

  vector<unique_ptr<Task>> tasks;

  string where_condition = kAssignedTo + "='" + assigned_to + "'";

  LockMainDatabase();

  tasks_tb_->open(where_condition);

  for (int i = 0; i < tasks_tb_->recordCount(); ++i) {
    sql::Record* record = tasks_tb_->getRecord(i);
    tasks.push_back(TaskFromRecord(record));
  }

  UnlockMainDatabase();

  return tasks;
}

void TaskManager::DeleteTasksFromCacheByTaskId(const std::string& task_id) const {
  string where_condition = kTaskId + "='" + task_id + "'";

  LockMainDatabase();

  tasks_tb_->deleteRecords(where_condition);

  UnlockMainDatabase();
}

void TaskManager::DeleteTasksFromCacheByProjectId(const std::string& project_id) const {
  string where_condition = kProjectId + "='" + project_id + "'";

  LockMainDatabase();

  tasks_tb_->deleteRecords(where_condition);

  UnlockMainDatabase();
}

////////////////////////////////////////////////////////////////////////////////
// TaskManager, private:

// Utils --------------------------------------------------------

void TaskManager::UnsafeSaveTaskToCache(const Task& task) const {
  sql::Record record = RecordByTask(task);
  tasks_tb_->addOrReplaceRecord(&record);
}

sql::Record TaskManager::RecordByTask(const Task& task) const {
  sql::Record record(tasks_tb_->fields());

  record.setString(kTaskId, task.task_id());
  record.setString(kTitle, task.title());
  record.setString(kListId, task.list_id());
  record.setString(kProjectId, task.project_id());
  record.setInteger(kCreatedAt, task.created_at());
  record.setString(kCreatedBy, task.created_by());
  record.setInteger(kLastUpdatedAt, task.last_updated_at());
  record.setInteger(kPosition, task.position());
  record.setString(kTaskNumber, task.task_number());
  record.setBool(kArchived, task.is_archived());
  record.setBool(kCompleted, task.is_completed());
  record.setBool(kDeleted, task.is_deleted());
  record.setInteger(kPermission, task.permission());
  record.setInteger(kNumComments, task.num_comments());
  record.setInteger(kNumAttachments, task.num_attachments());
  record.setInteger(kNumChildTasks, task.num_child_tasks());
  record.setInteger(kNumCompletedChildTasks, task.num_completed_child_tasks());
  record.setInteger(kNumLike, task.num_like());
  record.setString(kAssignedTo, task.assigned_to());
  record.setString(kAssignedBy, task.assigned_by());
  record.setInteger(kDue, task.due());
  record.setString(kTags, sakura::string_vector_join(task.tags(), ","));
  record.setString(kWatchers, sakura::string_vector_join(task.watchers(), ","));
  record.setString(kComments, sakura::string_vector_join(task.comments(), ","));
  record.setString(kLikes, sakura::string_vector_join(task.likes(), ","));

  return record;}

std::unique_ptr<Task> TaskManager::TaskFromRecord(sql::Record* record) const {
  std::string task_id = record->getValue(kTaskId)->asString();
  std::string title = record->getValue(kTitle)->asString();
  std::string list_id = record->getValue(kListId)->asString();
  std::string project_id = record->getValue(kProjectId)->asString();
  time_t created_at = static_cast<time_t>(record->getValue(kCreatedAt)->asInteger());
  std::string created_by = record->getValue(kCreatedBy)->asString();
  time_t last_updated_at = static_cast<time_t>(record->getValue(kLastUpdatedAt)->asInteger());
  int position = static_cast<int>(record->getValue(kPosition)->asInteger());
  std::string task_number = record->getValue(kTaskNumber)->asString();
  bool archived = record->getValue(kArchived)->asBool();
  bool completed = record->getValue(kCompleted)->asBool();
  bool deleted = record->getValue(kDeleted)->asBool();
  int permission = static_cast<int>(record->getValue(kPermission)->asInteger());
  int num_comments = static_cast<int>(record->getValue(kNumComments)->asInteger());
  int num_attachments = static_cast<int>(record->getValue(kNumAttachments)->asInteger());
  int num_child_tasks = static_cast<int>(record->getValue(kNumChildTasks)->asInteger());
  int num_completed_child_tasks = static_cast<int>(record->getValue(kNumCompletedChildTasks)->asInteger());
  int num_like = static_cast<int>(record->getValue(kNumLike)->asInteger());
  std::string assigned_to = record->getValue(kAssignedTo)->asString();
  std::string assigned_by = record->getValue(kAssignedBy)->asString();
  time_t due = static_cast<time_t>(record->getValue(kDue)->asInteger());
  std::vector<std::string> tags = sakura::string_split(record->getValue(kTags)->asString(), ",");
  std::vector<std::string> watchers = sakura::string_split(record->getValue(kWatchers)->asString(), ",");
  std::vector<std::string> comments = sakura::string_split(record->getValue(kComments)->asString(), ",");
  std::vector<std::string> likes = sakura::string_split(record->getValue(kLikes)->asString(), ",");

  unique_ptr<Task> task(new Task());
  task->Init(task_id, title, list_id, project_id, created_at, created_by, last_updated_at, position, task_number, archived, completed, deleted, permission, num_comments, num_attachments, num_child_tasks, num_completed_child_tasks, num_like, assigned_to, assigned_by, due, tags, watchers, comments, likes);
  return task;
}

NS_LCC_END

