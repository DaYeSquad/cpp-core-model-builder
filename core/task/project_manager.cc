#include "project_manager.h"
#include "director/director.h"

using std::string;
using std::unique_ptr;
using std::vector;

using sakura::FileUtils;


NS_LCC_BEGIN

// SQLite schema --------------------------------------------------------

static std::string const kProjectId = "project_id";
static std::string const kVisibility = "visibility";
static std::string const kColor = "color";
static std::string const kName = "name";
static std::string const kGroupId = "group_id";

static std::string const kSqlAnd = " AND ";

static sql::Field definition_projects[] = {
  sql::Field(kProjectId, sql::type_text, sql::flag_primary_key),
  sql::Field(kVisibility, sql::type_int, sql::flag_not_null),
  sql::Field(kColor, sql::type_text, sql::flag_not_null),
  sql::Field(kName, sql::type_text, sql::flag_not_null),
  sql::Field(kGroupId, sql::type_text, sql::flag_not_null),
  sql::Field(sql::DEFINITION_END),
};

////////////////////////////////////////////////////////////////////////////////
// ProjectManager, public:

// Creation and lifetime --------------------------------------------------------

ProjectManager::ProjectManager(Director* director)
:ObjectManager(director) {
}

ProjectManager::~ProjectManager() {
}

bool ProjectManager::InitOrDie() {
  bool success = true;

  do {
    projects_tb_ = unique_ptr<sql::Table>(new sql::Table(MainDatabaseHandler(), "ProjectManager", definition_projects));

    if (!projects_tb_->exists()) {
      success = projects_tb_->create();
      LCC_ASSERT(success);
    }

  } while(0);

  return success;
}

const ProjectManager* ProjectManager::DefaultManager() {
  return Director::DefaultDirector()->project_manager();
}

// SQLite schema --------------------------------------------------------

void ProjectManager::SaveProjectToCache(const Project& project) const {
  LockMainDatabase();

  UnsafeSaveProjectToCache(project);

  UnlockMainDatabase();
}

void ProjectManager::SaveProjectsToCache(const std::vector<std::unique_ptr<Project>>& projects) const {
  LockMainDatabase();

  for (auto it = projects.begin(); it != projects.end(); ++it) {
    UnsafeSaveProjectToCache(**it);
  }

  UnlockMainDatabase();
}

std::vector<std::unique_ptr<Project>> ProjectManager::FetchProjectsFromCache() const {

  vector<unique_ptr<Project>> projects;

  string where_condition = "";

  LockMainDatabase();

  projects_tb_->open(where_condition);

  for (int i = 0; i < projects_tb_->recordCount(); ++i) {
    sql::Record* record = projects_tb_->getRecord(i);
    projects.push_back(ProjectFromRecord(record));
  }

  UnlockMainDatabase();

  return projects;
}

////////////////////////////////////////////////////////////////////////////////
// ProjectManager, private:

// Utils --------------------------------------------------------

void ProjectManager::UnsafeSaveProjectToCache(const Project& project) const {
  sql::Record record = RecordByProject(project);
  projects_tb_->addOrReplaceRecord(&record);
}

sql::Record ProjectManager::RecordByProject(const Project& project) const {
  sql::Record record(projects_tb_->fields());

  record.setString(kProjectId, project.project_id());
  record.setInteger(kVisibility, static_cast<int>(project.visibility()));
  record.setString(kColor, project.color());
  record.setString(kName, project.name());
  record.setString(kGroupId, project.group_id());

  return record;
}

std::unique_ptr<Project> ProjectManager::ProjectFromRecord(sql::Record* record) const {
  std::string project_id = record->getValue(kProjectId)->asString();
  Project::Visibility visibility = static_cast<Project::Visibility>(record->getValue(kVisibility)->asInteger());
  std::string color = record->getValue(kColor)->asString();
  std::string name = record->getValue(kName)->asString();
  std::string group_id = record->getValue(kGroupId)->asString();

  unique_ptr<Project> project(new Project());
  project->Init(project_id, visibility, color, name, group_id);
  return project;
}

NS_LCC_END

