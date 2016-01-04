#include "list_manager.h"
#include "director/director.h"

using std::string;
using std::unique_ptr;
using std::vector;

using sakura::FileUtils;


NS_LCC_BEGIN

// SQLite schema --------------------------------------------------------

static std::string const kListId = "list_id";
static std::string const kName = "name";
static std::string const kPosition = "position";
static std::string const kProjectId = "project_id";

static std::string const kSqlAnd = " AND ";

static sql::Field definition_lists[] = {
  sql::Field(kListId, sql::type_text, sql::flag_primary_key),
  sql::Field(kName, sql::type_text, sql::flag_not_null),
  sql::Field(kPosition, sql::type_int, sql::flag_not_null),
  sql::Field(kProjectId, sql::type_text, sql::flag_not_null),
  sql::Field(sql::DEFINITION_END),
};

////////////////////////////////////////////////////////////////////////////////
// ListManager, public:

// Creation and lifetime --------------------------------------------------------

ListManager::ListManager(Director* director)
:ObjectManager(director) {
}

ListManager::~ListManager() {
}

bool ListManager::InitOrDie() {
  bool success = true;

  do {
    lists_tb_ = unique_ptr<sql::Table>(new sql::Table(MainDatabaseHandler(), "ListManager", definition_lists));

    if (!lists_tb_->exists()) {
      success = lists_tb_->create();
      LCC_ASSERT(success);
    }

  } while(0);

  return success;
}

const ListManager* ListManager::DefaultManager() {
  return Director::DefaultDirector()->list_manager();
}

// Persisent store --------------------------------------------------------

void ListManager::SaveListToCache(const List& list) const {
  LockMainDatabase();

  UnsafeSaveListToCache(list);

  UnlockMainDatabase();
}

void ListManager::SaveListsToCache(const std::vector<std::unique_ptr<List>>& lists) const {
  LockMainDatabase();

  for (auto it = lists.begin(); it != lists.end(); ++it) {
    UnsafeSaveListToCache(**it);
  }

  UnlockMainDatabase();
}

std::vector<std::unique_ptr<List>> ListManager::FetchListsFromCache() const {

  vector<unique_ptr<List>> lists;

  string where_condition = "";

  LockMainDatabase();

  lists_tb_->open(where_condition);

  for (int i = 0; i < lists_tb_->recordCount(); ++i) {
    sql::Record* record = lists_tb_->getRecord(i);
    lists.push_back(ListFromRecord(record));
  }

  UnlockMainDatabase();

  return lists;
}

std::vector<std::unique_ptr<List>> ListManager::FetchListsFromCacheByProjectId(const std::string& project_id) const {

  vector<unique_ptr<List>> lists;

  string where_condition = kProjectId + "='" + project_id + "'";

  LockMainDatabase();

  lists_tb_->open(where_condition);

  for (int i = 0; i < lists_tb_->recordCount(); ++i) {
    sql::Record* record = lists_tb_->getRecord(i);
    lists.push_back(ListFromRecord(record));
  }

  UnlockMainDatabase();

  return lists;
}

void ListManager::DeleteListsFromCache() const {
  string where_condition = "";

  LockMainDatabase();

  lists_tb_->deleteRecords(where_condition);

  UnlockMainDatabase();
}

void ListManager::DeleteListsFromCacheByProjectId(const std::string& project_id) const {
  string where_condition = kProjectId + "='" + project_id + "'";

  LockMainDatabase();

  lists_tb_->deleteRecords(where_condition);

  UnlockMainDatabase();
}

////////////////////////////////////////////////////////////////////////////////
// ListManager, private:

// Utils --------------------------------------------------------

void ListManager::UnsafeSaveListToCache(const List& list) const {
  sql::Record record = RecordByList(list);
  lists_tb_->addOrReplaceRecord(&record);
}

sql::Record ListManager::RecordByList(const List& list) const {
  sql::Record record(lists_tb_->fields());

  record.setString(kListId, list.list_id());
  record.setString(kName, list.name());
  record.setInteger(kPosition, list.position());
  record.setString(kProjectId, list.project_id());

  return record;
}

std::unique_ptr<List> ListManager::ListFromRecord(sql::Record* record) const {
  std::string list_id = record->getValue(kListId)->asString();
  std::string name = record->getValue(kName)->asString();
  int position = static_cast<int>(record->getValue(kPosition)->asInteger());
  std::string project_id = record->getValue(kProjectId)->asString();

  unique_ptr<List> list(new List());
  list->Init(list_id, name, position, project_id);
  return list;
}

NS_LCC_END

