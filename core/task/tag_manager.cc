#include "tag_manager.h"
#include "director/director.h"

using std::string;
using std::unique_ptr;
using std::vector;

using sakura::FileUtils;


NS_LCC_BEGIN

// SQLite schema --------------------------------------------------------

static std::string const kTagId = "tag_id";
static std::string const kType = "type";
static std::string const kColor = "color";
static std::string const kName = "name";

static std::string const kSqlAnd = "AND";

static sql::Field definition_tags[] = {
  sql::Field(kTagId, sql::type_text, sql::flag_primary_key),
  sql::Field(kType, sql::type_int, sql::flag_not_null),
  sql::Field(kColor, sql::type_text, sql::flag_not_null),
  sql::Field(kName, sql::type_text, sql::flag_not_null),
  sql::Field(sql::DEFINITION_END),
};

////////////////////////////////////////////////////////////////////////////////
// TagManager, public:

// Creation and lifetime --------------------------------------------------------

TagManager::TagManager(Director* director)
:ObjectManager(director) {
}

TagManager::~TagManager() {
}

bool TagManager::InitOrDie() {
  bool success = true;

  do {
    tags_tb_ = unique_ptr<sql::Table>(new sql::Table(MainDatabaseHandler(), "TagManager", definition_tags));

    if (!tags_tb_->exists()) {
      success = tags_tb_->create();
      LCC_ASSERT(success);
    }

  } while(0);

  return success;
}

const TagManager* TagManager::DefaultManager() {
  return Director::DefaultDirector()->tag_manager();
}

// SQLite schema --------------------------------------------------------

void TagManager::SaveTagToCache(const Tag& tag) const {
  LockMainDatabase();

  UnsafeSaveTagToCache(tag);

  UnlockMainDatabase();
}

void TagManager::SaveTagsToCache(const std::vector<std::unique_ptr<Tag>>& tags) const {
  LockMainDatabase();

  for (auto it = tags.begin(); it != tags.end(); ++it) {
    UnsafeSaveTagToCache(**it);
  }

  UnlockMainDatabase();
}

std::vector<std::unique_ptr<Tag>> TagManager::FetchTagsFromCacheByType(Tag::Type type) const {

  vector<unique_ptr<Tag>> tags;

  string where_condition = kType + "=" + std::to_string(static_cast<int>(type));;

  LockMainDatabase();

  tags_tb_->open(where_condition);

  for (int i = 0; i < tags_tb_->recordCount(); ++i) {
    sql::Record* record = tags_tb_->getRecord(i);
    tags.push_back(TagFromRecord(record));
  }

  UnlockMainDatabase();

  return tags;
}

////////////////////////////////////////////////////////////////////////////////
// TagManager, private:

// Utils --------------------------------------------------------

void TagManager::UnsafeSaveTagToCache(const Tag& tag) const {
  sql::Record record = RecordByTag(tag);
  tags_tb_->addOrReplaceRecord(&record);
}

sql::Record TagManager::RecordByTag(const Tag& tag) const {
  sql::Record record(tags_tb_->fields());

  record.setString(kTagId, tag.tag_id());
  record.setInteger(kType, static_cast<int>(tag.type()));
  record.setString(kColor, tag.color());
  record.setString(kName, tag.name());

  return record;}

std::unique_ptr<Tag> TagManager::TagFromRecord(sql::Record* record) const {
  std::string tag_id = record->getValue(kTagId)->asString();
  Tag::Type type = static_cast<Tag::Type>(record->getValue(kType)->asInteger());
  std::string color = record->getValue(kColor)->asString();
  std::string name = record->getValue(kName)->asString();

  unique_ptr<Tag> tag(new Tag());
  tag->Init(tag_id, type, color, name);
  return tag;
}

NS_LCC_END

