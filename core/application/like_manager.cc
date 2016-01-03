#include "like_manager.h"
#include "director/director.h"

using std::string;
using std::unique_ptr;
using std::vector;

using sakura::FileUtils;


NS_LCC_BEGIN

// SQLite schema --------------------------------------------------------

static std::string const kLikeId = "like_id";
static std::string const kType = "type";
static std::string const kApplicationId = "application_id";
static std::string const kCreatedBy = "created_by";
static std::string const kCreatedAt = "created_at";

static std::string const kSqlAnd = " AND ";

static sql::Field definition_likes[] = {
  sql::Field(kLikeId, sql::type_text, sql::flag_primary_key),
  sql::Field(kType, sql::type_int, sql::flag_not_null),
  sql::Field(kApplicationId, sql::type_text, sql::flag_not_null),
  sql::Field(kCreatedBy, sql::type_text, sql::flag_not_null),
  sql::Field(kCreatedAt, sql::type_int, sql::flag_not_null),
  sql::Field(sql::DEFINITION_END),
};

////////////////////////////////////////////////////////////////////////////////
// LikeManager, public:

// Creation and lifetime --------------------------------------------------------

LikeManager::LikeManager(Director* director)
:ObjectManager(director) {
}

LikeManager::~LikeManager() {
}

bool LikeManager::InitOrDie() {
  bool success = true;

  do {
    likes_tb_ = unique_ptr<sql::Table>(new sql::Table(MainDatabaseHandler(), "LikeManager", definition_likes));

    if (!likes_tb_->exists()) {
      success = likes_tb_->create();
      LCC_ASSERT(success);
    }

  } while(0);

  return success;
}

const LikeManager* LikeManager::DefaultManager() {
  return Director::DefaultDirector()->like_manager();
}

// HTTP --------------------------------------------------------

void LikeManager::LikeApplication(ApplicationType type,
                                  const std::string& application_id,
                                  std::function<void(bool success,
                                                     const std::string& error,
                                                     std::unique_ptr<Like> like)> callback) const
{
  WebApi::Api()
  ->PostLikeAtApplication(type,
                          application_id,
                          [this, callback](bool success, const std::string &error, std::unique_ptr<Like> like) {
                            if (success) {
                              this->SaveLikeToCache(*like);
                            }
                            callback(success, error, std::move(like));
  });
}

void LikeManager::RemoveLikeFromApplication(ApplicationType type,
                                            const std::string& application_id,
                                            std::function<void(bool success,
                                                               const std::string& error)> callback) const
{
  WebApi::Api()
  ->DeleteLikeFromApplication(type,
                              application_id,
                              [this, callback](bool success, const std::string &error) {
    if (success) {
      this->deletelike
    }
    callback(success, error);
  });
}

// Persisent store --------------------------------------------------------

void LikeManager::SaveLikeToCache(const Like& like) const {
  LockMainDatabase();

  UnsafeSaveLikeToCache(like);

  UnlockMainDatabase();
}

void LikeManager::SaveLikesToCache(const std::vector<std::unique_ptr<Like>>& likes) const {
  LockMainDatabase();

  for (auto it = likes.begin(); it != likes.end(); ++it) {
    UnsafeSaveLikeToCache(**it);
  }

  UnlockMainDatabase();
}

std::vector<std::unique_ptr<Like>> LikeManager::FetchLikesFromCacheByType(ApplicationType type) const {

  vector<unique_ptr<Like>> likes;

  string where_condition = kType + "=" + std::to_string(static_cast<int>(type));;

  LockMainDatabase();

  likes_tb_->open(where_condition);

  for (int i = 0; i < likes_tb_->recordCount(); ++i) {
    sql::Record* record = likes_tb_->getRecord(i);
    likes.push_back(LikeFromRecord(record));
  }

  UnlockMainDatabase();

  return likes;
}

std::unique_ptr<Like> LikeManager::FetchLikeFromCacheByLikeId(const std::string& like_id) const {
  string where_condition = kLikeId + "='" + like_id + "'";

  LockMainDatabase();

  likes_tb_->open(where_condition);

  if (likes_tb_->recordCount() != 0) {
    sql::Record* record = likes_tb_->getRecord(0);
    unique_ptr<Like> rtn(LikeFromRecord(record));
    UnlockMainDatabase();
    return rtn;
  }

  UnlockMainDatabase();

  return nullptr;
}

std::vector<std::unique_ptr<Like>> LikeManager::FetchLikesFromCache(ApplicationType type, const std::string& application_id) const {

  vector<unique_ptr<Like>> likes;

  string where_condition = kType + "=" + std::to_string(static_cast<int>(type)); + kSqlAnd + kApplicationId + "='" + application_id + "'";

  LockMainDatabase();

  likes_tb_->open(where_condition);

  for (int i = 0; i < likes_tb_->recordCount(); ++i) {
    sql::Record* record = likes_tb_->getRecord(i);
    likes.push_back(LikeFromRecord(record));
  }

  UnlockMainDatabase();

  return likes;
}

void LikeManager::DeleteLikesFromCacheByType(ApplicationType type) const {
  string where_condition = kType + "=" + std::to_string(static_cast<int>(type));;

  LockMainDatabase();

  likes_tb_->deleteRecords(where_condition);

  UnlockMainDatabase();
}

void LikeManager::DeleteLikesFromCache() const {
  string where_condition = "";

  LockMainDatabase();

  likes_tb_->deleteRecords(where_condition);

  UnlockMainDatabase();
}

void LikeManager::DeleteLikeFromCacheByLikeId(const std::string& like_id) const {
  string where_condition = kLikeId + "='" + like_id + "'";

  LockMainDatabase();

  likes_tb_->deleteRecords(where_condition);

  UnlockMainDatabase();
}

void LikeManager::DeleteLikesFromCache(ApplicationType type, const std::string& application_id) const {
  string where_condition = kType + "=" + std::to_string(static_cast<int>(type)); + kSqlAnd + kApplicationId + "='" + application_id + "'";

  LockMainDatabase();

  likes_tb_->deleteRecords(where_condition);

  UnlockMainDatabase();
}

void LikeManager::DeleteLikeFromCache(ApplicationType type, const std::string& application_id, const std::string& created_by) const {
  string where_condition = kType + "=" + std::to_string(static_cast<int>(type)); + kSqlAnd + kApplicationId + "='" + application_id + "'" + kSqlAnd + kCreatedBy + "='" + created_by + "'";

  LockMainDatabase();

  likes_tb_->deleteRecords(where_condition);

  UnlockMainDatabase();
}

////////////////////////////////////////////////////////////////////////////////
// LikeManager, private:

// Utils --------------------------------------------------------

void LikeManager::UnsafeSaveLikeToCache(const Like& like) const {
  sql::Record record = RecordByLike(like);
  likes_tb_->addOrReplaceRecord(&record);
}

sql::Record LikeManager::RecordByLike(const Like& like) const {
  sql::Record record(likes_tb_->fields());

  record.setString(kLikeId, like.like_id());
  record.setInteger(kType, static_cast<int>(like.type()));
  record.setString(kApplicationId, like.application_id());
  record.setString(kCreatedBy, like.created_by());
  record.setInteger(kCreatedAt, like.created_at());

  return record;
}

std::unique_ptr<Like> LikeManager::LikeFromRecord(sql::Record* record) const {
  std::string like_id = record->getValue(kLikeId)->asString();
  ApplicationType type = static_cast<ApplicationType>(record->getValue(kType)->asInteger());
  std::string application_id = record->getValue(kApplicationId)->asString();
  std::string created_by = record->getValue(kCreatedBy)->asString();
  time_t created_at = static_cast<time_t>(record->getValue(kCreatedAt)->asInteger());

  unique_ptr<Like> like(new Like());
  like->Init(like_id, type, application_id, created_by, created_at);
  return like;
}

NS_LCC_END

