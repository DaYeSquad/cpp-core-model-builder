#include "user_manager.h"
#include "director/director.h"

using std::string;
using std::unique_ptr;
using std::vector;

using sakura::FileUtils;


NS_LCC_BEGIN

// SQLite schema --------------------------------------------------------

static std::string const kUid = "uid";
static std::string const kUsername = "username";
static std::string const kDisplayName = "display_name";
static std::string const kPinyin = "pinyin";
static std::string const kHeaderUri = "header_uri";
static std::string const kDeleted = "deleted";
static std::string const kRole = "role";
static std::string const kState = "state";
static std::string const kStatus = "status";
static std::string const kPhoneNumber = "phone_number";
static std::string const kJobTitle = "job_title";
static std::string const kDepartment = "department";
static std::string const kEmail = "email";

static std::string const kSqlAnd = "AND";

static sql::Field definition_users[] = {
  sql::Field(kUid, sql::type_text, sql::flag_primary_key),
  sql::Field(kUsername, sql::type_text, sql::flag_not_null),
  sql::Field(kDisplayName, sql::type_text, sql::flag_not_null),
  sql::Field(kPinyin, sql::type_text, sql::flag_not_null),
  sql::Field(kHeaderUri, sql::type_text, sql::flag_not_null),
  sql::Field(kDeleted, sql::type_bool, sql::flag_not_null),
  sql::Field(kRole, sql::type_int, sql::flag_not_null),
  sql::Field(kState, sql::type_int, sql::flag_not_null),
  sql::Field(kStatus, sql::type_int, sql::flag_not_null),
  sql::Field(kPhoneNumber, sql::type_text, sql::flag_not_null),
  sql::Field(kJobTitle, sql::type_text, sql::flag_not_null),
  sql::Field(kDepartment, sql::type_text, sql::flag_not_null),
  sql::Field(kEmail, sql::type_text, sql::flag_not_null),
  sql::Field(sql::DEFINITION_END),
};

////////////////////////////////////////////////////////////////////////////////
// UserManager, public:

// Creation and lifetime --------------------------------------------------------

UserManager::UserManager(Director* director)
:ObjectManager(director) {
}

UserManager::~UserManager() {
}

bool UserManager::InitOrDie() {
  bool success = true;

  do {
    users_tb_ = unique_ptr<sql::Table>(new sql::Table(MainDatabaseHandler(), "UserManager", definition_users));

    if (!users_tb_->exists()) {
      success = users_tb_->create();
      LCC_ASSERT(success);
    }

  } while(0);

  return success;
}

const UserManager* UserManager::DefaultManager() {
  return Director::DefaultDirector()->user_manager();
}

// SQLite schema --------------------------------------------------------

void UserManager::SaveUserToCache(const User& user) const {
  LockMainDatabase();

  UnsafeSaveUserToCache(user);

  UnlockMainDatabase();
}

void UserManager::SaveUsersToCache(const std::vector<std::unique_ptr<User>>& users) const {
  LockMainDatabase();

  for (auto it = users.begin(); it != users.end(); ++it) {
    UnsafeSaveUserToCache(**it);
  }

  UnlockMainDatabase();
}

std::unique_ptr<User> UserManager::FetchUserFromCacheByUid(const std::string& uid) const {
  string where_condition = kUid + "='" + uid + "'";

  LockMainDatabase();

  users_tb_->open(where_condition);

  if (users_tb_->recordCount() != 0) {
    sql::Record* record = users_tb_->getRecord(0);
    unique_ptr<User> rtn(UserFromRecord(record));
    UnlockMainDatabase();
    return rtn;
  }

  UnlockMainDatabase();

  return nullptr;
}

std::vector<std::unique_ptr<User>> UserManager::FetchUsersFromCache() const {

  vector<unique_ptr<User>> users;

  string where_condition = "";

  LockMainDatabase();

  users_tb_->open(where_condition);

  for (int i = 0; i < users_tb_->recordCount(); ++i) {
    sql::Record* record = users_tb_->getRecord(i);
    users.push_back(UserFromRecord(record));
  }

  UnlockMainDatabase();

  return users;
}

void UserManager::DeleteUserFromCache() const {
  string where_condition = "";

  LockMainDatabase();

  users_tb_->deleteRecords(where_condition);

  UnlockMainDatabase();
}

void UserManager::DeleteUsersFromCache() const {
  string where_condition = "";

  LockMainDatabase();

  users_tb_->deleteRecords(where_condition);

  UnlockMainDatabase();
}

void UserManager::DeleteUserFromCacheByUid(const std::string& uid) const {
  string where_condition = kUid + "='" + uid + "'";

  LockMainDatabase();

  users_tb_->deleteRecords(where_condition);

  UnlockMainDatabase();
}

void UserManager::DeleteUserFromCache(const std::string& uid, const std::string& username) const {
  string where_condition = kUid + "='" + uid + "'" + kSqlAnd + kUsername + "='" + username + "'";

  LockMainDatabase();

  users_tb_->deleteRecords(where_condition);

  UnlockMainDatabase();
}

////////////////////////////////////////////////////////////////////////////////
// UserManager, private:

// Utils --------------------------------------------------------

void UserManager::UnsafeSaveUserToCache(const User& user) const {
  sql::Record record = RecordByUser(user);
  users_tb_->addOrReplaceRecord(&record);
}

sql::Record UserManager::RecordByUser(const User& user) const {
  sql::Record record(users_tb_->fields());

  record.setString(kUid, user.uid());
  record.setString(kUsername, user.username());
  record.setString(kDisplayName, user.display_name());
  record.setString(kPinyin, user.pinyin());
  record.setString(kHeaderUri, user.header_uri());
  record.setBool(kDeleted, user.is_deleted());
  record.setInteger(kRole, static_cast<int>(user.role()));
  record.setInteger(kState, static_cast<int>(user.state()));
  record.setInteger(kStatus, static_cast<int>(user.status()));
  record.setString(kPhoneNumber, user.phone_number());
  record.setString(kJobTitle, user.job_title());
  record.setString(kDepartment, user.department());
  record.setString(kEmail, user.email());

  return record;}

std::unique_ptr<User> UserManager::UserFromRecord(sql::Record* record) const {
  std::string uid = record->getValue(kUid)->asString();
  std::string username = record->getValue(kUsername)->asString();
  std::string display_name = record->getValue(kDisplayName)->asString();
  std::string pinyin = record->getValue(kPinyin)->asString();
  std::string header_uri = record->getValue(kHeaderUri)->asString();
  bool deleted = record->getValue(kDeleted)->asBool();
  User::Status role = static_cast<User::Status>(record->getValue(kRole)->asInteger());
  User::Status state = static_cast<User::Status>(record->getValue(kState)->asInteger());
  User::Status status = static_cast<User::Status>(record->getValue(kStatus)->asInteger());
  std::string phone_number = record->getValue(kPhoneNumber)->asString();
  std::string job_title = record->getValue(kJobTitle)->asString();
  std::string department = record->getValue(kDepartment)->asString();
  std::string email = record->getValue(kEmail)->asString();

  unique_ptr<User> user(new User());
  user->Init(uid, username, display_name, pinyin, header_uri, deleted, role, state, status, phone_number, job_title, department, email);
  return user;
}

NS_LCC_END

