#include "project_group_manager.h"
#include "director/director.h"

using std::string;
using std::unique_ptr;
using std::vector;

using sakura::FileUtils;


NS_LCC_BEGIN

// SQLite schema --------------------------------------------------------

static std::string const kGroupId = "group_id";
static std::string const kTeamId = "team_id";
static std::string const kOwner = "owner";
static std::string const kName = "name";
static std::string const kPosition = "position";

static std::string const kSqlAnd = " AND ";

static sql::Field definition_projectgroups[] = {
  sql::Field(kGroupId, sql::type_text, sql::flag_primary_key),
  sql::Field(kTeamId, sql::type_text, sql::flag_not_null),
  sql::Field(kOwner, sql::type_text, sql::flag_not_null),
  sql::Field(kName, sql::type_text, sql::flag_not_null),
  sql::Field(kPosition, sql::type_int, sql::flag_not_null),
  sql::Field(sql::DEFINITION_END),
};

////////////////////////////////////////////////////////////////////////////////
// ProjectGroupManager, public:

// Creation and lifetime --------------------------------------------------------

ProjectGroupManager::ProjectGroupManager(Director* director)
:ObjectManager(director) {
}

ProjectGroupManager::~ProjectGroupManager() {
}

bool ProjectGroupManager::InitOrDie() {
  bool success = true;

  do {
    projectgroups_tb_ = unique_ptr<sql::Table>(new sql::Table(MainDatabaseHandler(), "ProjectGroupManager", definition_projectgroups));

    if (!projectgroups_tb_->exists()) {
      success = projectgroups_tb_->create();
      LCC_ASSERT(success);
    }

  } while(0);

  return success;
}

const ProjectGroupManager* ProjectGroupManager::DefaultManager() {
  return Director::DefaultDirector()->project_group_manager();
}

// Persisent store --------------------------------------------------------
void ProjectGroupManager::SaveProjectGroupToCache(const ProjectGroup& projectgroup) const {
  LockMainDatabase();

  UnsafeSaveProjectGroupToCache(projectgroup);

  UnlockMainDatabase();
}

void ProjectGroupManager::SaveProjectGroupsToCache(const std::vector<std::unique_ptr<ProjectGroup>>& projectgroups) const {
  LockMainDatabase();

  for (auto it = projectgroups.begin(); it != projectgroups.end(); ++it) {
    UnsafeSaveProjectGroupToCache(**it);
  }

  UnlockMainDatabase();
}

std::vector<std::unique_ptr<ProjectGroup>> ProjectGroupManager::FetchProjectGroupsFromCache() const {

  vector<unique_ptr<ProjectGroup>> projectgroups;

  string where_condition = "";

  LockMainDatabase();

  projectgroups_tb_->open(where_condition);

  for (int i = 0; i < projectgroups_tb_->recordCount(); ++i) {
    sql::Record* record = projectgroups_tb_->getRecord(i);
    projectgroups.push_back(ProjectGroupFromRecord(record));
  }

  UnlockMainDatabase();

  return projectgroups;
}

std::unique_ptr<ProjectGroup> ProjectGroupManager::FetchProjectGroupFromCacheByGroupId(const std::string& group_id) const {
  string where_condition = kGroupId + "='" + group_id + "'";

  LockMainDatabase();

  projectgroups_tb_->open(where_condition);

  if (projectgroups_tb_->recordCount() != 0) {
    sql::Record* record = projectgroups_tb_->getRecord(0);
    unique_ptr<ProjectGroup> rtn(ProjectGroupFromRecord(record));
    UnlockMainDatabase();
    return rtn;
  }

  UnlockMainDatabase();

  return nullptr;
}

void ProjectGroupManager::DeleteProjectGroupsFromCache() const {
  string where_condition = "";

  LockMainDatabase();

  projectgroups_tb_->deleteRecords(where_condition);

  UnlockMainDatabase();
}

void ProjectGroupManager::DeleteProjectGroupFromCacheByGroupId(const std::string& group_id) const {
  string where_condition = kGroupId + "='" + group_id + "'";

  LockMainDatabase();

  projectgroups_tb_->deleteRecords(where_condition);

  UnlockMainDatabase();
}

////////////////////////////////////////////////////////////////////////////////
// ProjectGroupManager, private:

// Utils --------------------------------------------------------

void ProjectGroupManager::UnsafeSaveProjectGroupToCache(const ProjectGroup& projectgroup) const {
  sql::Record record = RecordByProjectGroup(projectgroup);
  projectgroups_tb_->addOrReplaceRecord(&record);
}

sql::Record ProjectGroupManager::RecordByProjectGroup(const ProjectGroup& projectgroup) const {
  sql::Record record(projectgroups_tb_->fields());

  record.setString(kGroupId, projectgroup.group_id());
  record.setString(kTeamId, projectgroup.team_id());
  record.setString(kOwner, projectgroup.owner());
  record.setString(kName, projectgroup.name());
  record.setInteger(kPosition, projectgroup.position());

  return record;
}

std::unique_ptr<ProjectGroup> ProjectGroupManager::ProjectGroupFromRecord(sql::Record* record) const {
  std::string group_id = record->getValue(kGroupId)->asString();
  std::string team_id = record->getValue(kTeamId)->asString();
  std::string owner = record->getValue(kOwner)->asString();
  std::string name = record->getValue(kName)->asString();
  int position = static_cast<int>(record->getValue(kPosition)->asInteger());

  unique_ptr<ProjectGroup> projectgroup(new ProjectGroup());
  projectgroup->Init(group_id, team_id, owner, name, position);
  return projectgroup;
}

NS_LCC_END

