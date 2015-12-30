#include "task_manager.h"

using std::string;
using std::unique_ptr;
using std::vector;

using sakura::FileUtils;


NS_LCC_BEGIN

// SQLite schema --------------------------------------------------------

static std::string const kTaskId = "task_id";
static std::string const kTitle = "title";
static std::string const kProjectId = "project_id";
static std::string const kArchived = "archived";
static std::string const kCompleted = "completed";
static std::string const kDeleted = "deleted";
static std::string const kPermission = "permission";
static std::string const kPosition = "position";
static std::string const kCreatedAt = "created_at";
static std::string const kPhoneNumber = "phone_number";
static std::string const kCreatedBy = "created_by";
static std::string const kTags = "tags";

static std::string const kSqlAnd = "AND";

static sql::Field definition_tasks[] = {
  sql::Field(kTaskId, sql::type_text, sql::flag_primary_key),
  sql::Field(kTitle, sql::type_text, sql::flag_not_null),
  sql::Field(kProjectId, sql::type_text, sql::flag_not_null),
  sql::Field(kArchived, sql::type_bool, sql::flag_not_null),
  sql::Field(kCompleted, sql::type_bool, sql::flag_not_null),
  sql::Field(kDeleted, sql::type_bool, sql::flag_not_null),
  sql::Field(kPermission, sql::type_int, sql::flag_not_null),
  sql::Field(kPosition, sql::type_int, sql::flag_not_null),
  sql::Field(kCreatedAt, sql::type_int, sql::flag_not_null),
  sql::Field(kPhoneNumber, sql::type_text, sql::flag_not_null),
  sql::Field(kCreatedBy, sql::type_text, sql::flag_not_null),
  sql::Field(kTags, sql::type_text, sql::flag_not_null),
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
    UnsafeSaveTaskToCache(task);
  }

  UnlockMainDatabase();
}

std::unique_ptr<Task> FetchTaskFromCacheByTaskId(const std::string& task_id) const {
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

std::vector<std::unique_ptr<Task>> FetchTasksFromCache() const;

  vector<unique_ptr<Task>> tasks;

  string where_condition = "";

  LockMainDatabase();

  tasks_tb_->open(where_condition);

  for (int i = 0; i < tasks_tb_->recordCount(); ++i) {
    sql::Record* record = tasks_tb_->getRecord(i);
    tasks.push_back(TaskFromRecord(record));
  }

  UnlockMainDatabase();

  return tasks;
}

void TaskManager::DeleteTaskFromCache() const {
  string where_condition = "";

  LockMainDatabase();

  tasks_tb_->deleteRecords(where_condition);

  UnlockMainDatabase();
}

void TaskManager::DeleteTasksFromCache() const {
  string where_condition = "";

  LockMainDatabase();

  tasks_tb_->deleteRecords(where_condition);

  UnlockMainDatabase();
}

void TaskManager::DeleteTaskFromCacheByTaskId(const std::string& task_id) const {
  string where_condition = kTaskId + "='" + task_id + "'";

  LockMainDatabase();

  tasks_tb_->deleteRecords(where_condition);

  UnlockMainDatabase();
}

void TaskManager::DeleteTaskFromCache(const std::string& task_id, const std::string& project_id) const {
  string where_condition = kTaskId + "='" + task_id + "'" + kSqlAnd + kProjectId + "='" + project_id + "'";

  LockMainDatabase();

  tasks_tb_->deleteRecords(where_condition);

  UnlockMainDatabase();
}

////////////////////////////////////////////////////////////////////////////////
// TaskManager, private:

// Utils --------------------------------------------------------

void TaskManager::UnsafeSaveTaskToCache(const Task& task) const {
  sql::Record record = RecordByTask(task);
  return tasks_tb_->addOrReplaceRecord(&record);
}

sql::Record TaskManager::RecordByTask(const Task& task) const {
  sql::Record record(tasks_tb_->fields());

  record.setString(kTaskId, task.task_id());
  record.setString(kTitle, task.title());
  record.setString(kProjectId, task.project_id());
  record.setBool(kArchived, task.archived());
  record.setBool(kCompleted, task.completed());
  record.setBool(kDeleted, task.deleted());
  record.setInteger(kPermission, task.permission());
  record.setInteger(kPosition, task.position());
  record.setInteger(kCreatedAt, task.created_at());
  record.setString(kPhoneNumber, task.phone_number());
  record.setString(kCreatedBy, task.created_by());
  record.setString(kTags, sakura::string_vector_join(task.tags(), ","));

  return record;}

std::unique_ptr<Task> TaskManager::TaskFromRecord(sql::Record* record) const {
  std::string task_id = static_cast<const std::string&>(record->getValue(kTaskId)->asString());
  std::string title = static_cast<const std::string&>(record->getValue(kTitle)->asString());
  std::string project_id = static_cast<const std::string&>(record->getValue(kProjectId)->asString());
  bool archived = static_cast<bool>(record->getValue(kArchived)->asBool());
  bool completed = static_cast<bool>(record->getValue(kCompleted)->asBool());
  bool deleted = static_cast<bool>(record->getValue(kDeleted)->asBool());
  int permission = static_cast<int>(record->getValue(kPermission)->asInteger());
  int position = static_cast<int>(record->getValue(kPosition)->asInteger());
  int created_at = static_cast<int>(record->getValue(kCreatedAt)->asInteger());
  std::string phone_number = static_cast<const std::string&>(record->getValue(kPhoneNumber)->asString());
  std::string created_by = static_cast<const std::string&>(record->getValue(kCreatedBy)->asString());
  std::vector<std::string> tags = sakura::string_split(record->getValue(kTags)->asString(), ",");

  unique_ptr<Task> task(new Task());
  task->Init(task_id, title, project_id, archived, completed, deleted, permission, position, created_at, phone_number, created_by, tags);
  return task;
}

NS_LCC_END

