#include "permission_manager.h"
#include "director/director.h"

using std::string;
using std::unique_ptr;
using std::vector;

using sakura::FileUtils;


NS_LCC_BEGIN

// SQLite schema --------------------------------------------------------

static std::string const kType = "type";
static std::string const kIdentifier = "identifier";
static std::string const kValue = "value";

static std::string const kSqlAnd = " AND ";

static sql::Field definition_permissions[] = {
  sql::Field(kType, sql::type_int, sql::flag_not_null),
  sql::Field(kIdentifier, sql::type_text, sql::flag_primary_key),
  sql::Field(kValue, sql::type_int, sql::flag_not_null),
  sql::Field(sql::DEFINITION_END),
};

////////////////////////////////////////////////////////////////////////////////
// PermissionManager, public:

// Creation and lifetime --------------------------------------------------------

PermissionManager::PermissionManager(Director* director)
:ObjectManager(director) {
}

PermissionManager::~PermissionManager() {
}

bool PermissionManager::InitOrDie() {
  bool success = true;

  do {
    permissions_tb_ = unique_ptr<sql::Table>(new sql::Table(MainDatabaseHandler(), "PermissionManager", definition_permissions));

    if (!permissions_tb_->exists()) {
      success = permissions_tb_->create();
      LCC_ASSERT(success);
    }

  } while(0);

  return success;
}

const PermissionManager* PermissionManager::DefaultManager() {
  return Director::DefaultDirector()->permission_manager();
}

// Persisent store --------------------------------------------------------

void PermissionManager::SavePermissionToCache(const Permission& permission) const {
  LockMainDatabase();

  UnsafeSavePermissionToCache(permission);

  UnlockMainDatabase();
}

void PermissionManager::SavePermissionsToCache(const std::vector<std::unique_ptr<Permission>>& permissions) const {
  LockMainDatabase();

  for (auto it = permissions.begin(); it != permissions.end(); ++it) {
    UnsafeSavePermissionToCache(**it);
  }

  UnlockMainDatabase();
}

std::vector<std::unique_ptr<Permission>> PermissionManager::FetchPermissionsFromCache(const std::string& identifier, Permission::Type type) const {

  vector<unique_ptr<Permission>> permissions;

  string where_condition = kIdentifier + "='" + identifier + "'" + kSqlAnd + kType + "=" + std::to_string(static_cast<int>(type));

  LockMainDatabase();

  permissions_tb_->open(where_condition);

  for (int i = 0; i < permissions_tb_->recordCount(); ++i) {
    sql::Record* record = permissions_tb_->getRecord(i);
    permissions.push_back(PermissionFromRecord(record));
  }

  UnlockMainDatabase();

  return permissions;
}

void PermissionManager::DeletePermissionsFromCache() const {
  string where_condition = "";

  LockMainDatabase();

  permissions_tb_->deleteRecords(where_condition);

  UnlockMainDatabase();
}

void PermissionManager::DeletePermissionsFromCache(const std::string& identifier, Permission::Type type) const {
  string where_condition = kIdentifier + "='" + identifier + "'" + kSqlAnd + kType + "=" + std::to_string(static_cast<int>(type));

  LockMainDatabase();

  permissions_tb_->deleteRecords(where_condition);

  UnlockMainDatabase();
}

////////////////////////////////////////////////////////////////////////////////
// PermissionManager, private:

// Utils --------------------------------------------------------

void PermissionManager::UnsafeSavePermissionToCache(const Permission& permission) const {
  sql::Record record = RecordByPermission(permission);
  permissions_tb_->addOrReplaceRecord(&record);
}

sql::Record PermissionManager::RecordByPermission(const Permission& permission) const {
  sql::Record record(permissions_tb_->fields());

  record.setInteger(kType, static_cast<int>(permission.type()));
  record.setString(kIdentifier, permission.identifier());
  record.setInteger(kValue, permission.value());

  return record;
}

std::unique_ptr<Permission> PermissionManager::PermissionFromRecord(sql::Record* record) const {
  Permission::Type type = static_cast<Permission::Type>(record->getValue(kType)->asInteger());
  std::string identifier = record->getValue(kIdentifier)->asString();
  int value = static_cast<int>(record->getValue(kValue)->asInteger());

  unique_ptr<Permission> permission(new Permission());
  permission->Init(type, identifier, value);
  return permission;
}

NS_LCC_END

