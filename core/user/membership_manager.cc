#include "membership_manager.h"
#include "director/director.h"

using std::string;
using std::unique_ptr;
using std::vector;

using sakura::FileUtils;


NS_LCC_BEGIN

// SQLite schema --------------------------------------------------------

static std::string const kMembershipId = "membership_id";
static std::string const kUid = "uid";
static std::string const kIdentifier = "identifier";
static std::string const kType = "type";

static std::string const kSqlAnd = " AND ";

static sql::Field definition_memberships[] = {
  sql::Field(kMembershipId, sql::type_text, sql::flag_primary_key),
  sql::Field(kUid, sql::type_text, sql::flag_not_null),
  sql::Field(kIdentifier, sql::type_text, sql::flag_not_null),
  sql::Field(kType, sql::type_int, sql::flag_not_null),
  sql::Field(sql::DEFINITION_END),
};

////////////////////////////////////////////////////////////////////////////////
// MembershipManager, public:

// Creation and lifetime --------------------------------------------------------

MembershipManager::MembershipManager(Director* director)
:ObjectManager(director) {
}

MembershipManager::~MembershipManager() {
}

bool MembershipManager::InitOrDie() {
  bool success = true;

  do {
    memberships_tb_ = unique_ptr<sql::Table>(new sql::Table(MainDatabaseHandler(), "MembershipManager", definition_memberships));

    if (!memberships_tb_->exists()) {
      success = memberships_tb_->create();
      LCC_ASSERT(success);
    }

  } while(0);

  return success;
}

const MembershipManager* MembershipManager::DefaultManager() {
  return Director::DefaultDirector()->membership_manager();
}

// Persisent store --------------------------------------------------------
void MembershipManager::SaveMembershipToCache(const Membership& membership) const {
  LockMainDatabase();

  UnsafeSaveMembershipToCache(membership);

  UnlockMainDatabase();
}

void MembershipManager::SaveMembershipsToCache(const std::vector<std::unique_ptr<Membership>>& memberships) const {
  LockMainDatabase();

  for (auto it = memberships.begin(); it != memberships.end(); ++it) {
    UnsafeSaveMembershipToCache(**it);
  }

  UnlockMainDatabase();
}

std::vector<std::unique_ptr<Membership>> MembershipManager::FetchMembershipsFromCache(const std::string& uid, Membership::Type type) const {

  vector<unique_ptr<Membership>> memberships;

  string where_condition = kUid + "='" + uid + "'" + kSqlAnd + kType + "=" + std::to_string(static_cast<int>(type));;

  LockMainDatabase();

  memberships_tb_->open(where_condition);

  for (int i = 0; i < memberships_tb_->recordCount(); ++i) {
    sql::Record* record = memberships_tb_->getRecord(i);
    memberships.push_back(MembershipFromRecord(record));
  }

  UnlockMainDatabase();

  return memberships;
}

std::vector<std::unique_ptr<Membership>> MembershipManager::FetchMembershipsFromCache(const std::string& identifier, Membership::Type type) const {

  vector<unique_ptr<Membership>> memberships;

  string where_condition = kIdentifier + "='" + identifier + "'" + kSqlAnd + kType + "=" + std::to_string(static_cast<int>(type));;

  LockMainDatabase();

  memberships_tb_->open(where_condition);

  for (int i = 0; i < memberships_tb_->recordCount(); ++i) {
    sql::Record* record = memberships_tb_->getRecord(i);
    memberships.push_back(MembershipFromRecord(record));
  }

  UnlockMainDatabase();

  return memberships;
}

std::unique_ptr<Membership> MembershipManager::FetchMembershipFromCache(const std::string& uid, const std::string& identifier, Membership::Type type) const {
  string where_condition = kUid + "='" + uid + "'" + kSqlAnd + kIdentifier + "='" + identifier + "'" + kSqlAnd + kType + "=" + std::to_string(static_cast<int>(type));;

  LockMainDatabase();

  memberships_tb_->open(where_condition);

  if (memberships_tb_->recordCount() != 0) {
    sql::Record* record = memberships_tb_->getRecord(0);
    unique_ptr<Membership> rtn(MembershipFromRecord(record));
    UnlockMainDatabase();
    return rtn;
  }

  UnlockMainDatabase();

  return nullptr;
}

void MembershipManager::DeleteMembershipFromCache(const std::string& uid, const std::string& identifier, Membership::Type type) const {
  string where_condition = kUid + "='" + uid + "'" + kSqlAnd + kIdentifier + "='" + identifier + "'" + kSqlAnd + kType + "=" + std::to_string(static_cast<int>(type));;

  LockMainDatabase();

  memberships_tb_->deleteRecords(where_condition);

  UnlockMainDatabase();
}

void MembershipManager::DeleteMembershipsFromCache() const {
  string where_condition = "";

  LockMainDatabase();

  memberships_tb_->deleteRecords(where_condition);

  UnlockMainDatabase();
}

void MembershipManager::DeleteMembershipsFromCache(const std::string& identifier, Membership::Type type) const {
  string where_condition = kIdentifier + "='" + identifier + "'" + kSqlAnd + kType + "=" + std::to_string(static_cast<int>(type));;

  LockMainDatabase();

  memberships_tb_->deleteRecords(where_condition);

  UnlockMainDatabase();
}

////////////////////////////////////////////////////////////////////////////////
// MembershipManager, private:

// Utils --------------------------------------------------------

void MembershipManager::UnsafeSaveMembershipToCache(const Membership& membership) const {
  sql::Record record = RecordByMembership(membership);
  memberships_tb_->addOrReplaceRecord(&record);
}

sql::Record MembershipManager::RecordByMembership(const Membership& membership) const {
  sql::Record record(memberships_tb_->fields());

  record.setString(kMembershipId, membership.membership_id());
  record.setString(kUid, membership.uid());
  record.setString(kIdentifier, membership.identifier());
  record.setInteger(kType, static_cast<int>(membership.type()));

  return record;
}

std::unique_ptr<Membership> MembershipManager::MembershipFromRecord(sql::Record* record) const {
  std::string membership_id = record->getValue(kMembershipId)->asString();
  std::string uid = record->getValue(kUid)->asString();
  std::string identifier = record->getValue(kIdentifier)->asString();
  Membership::Type type = static_cast<Membership::Type>(record->getValue(kType)->asInteger());

  unique_ptr<Membership> membership(new Membership());
  membership->Init(membership_id, uid, identifier, type);
  return membership;
}

NS_LCC_END

