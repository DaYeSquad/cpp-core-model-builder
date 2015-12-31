#ifndef LESSCHATCORE_CORE_TASK_TAG_MANAGER_H_
#define LESSCHATCORE_CORE_TASK_TAG_MANAGER_H_

#include <string>
#include <memory>
#include <vector>
#include <functional>

#include "easySQLite/easySQLite.h"

#include "base/base.h"
#include "director/object_manager.h"
#include "api/web_api.h"

#include "task/tag.h"

NS_LCC_BEGIN

class LCC_DLL TagManager : public ObjectManager {
public:

  // Creation and lifetime --------------------------------------------------------

  explicit TagManager(Director* director);

  virtual ~TagManager();

  bool InitOrDie();

  static const TagManager* DefaultManager();

  // Persisent store --------------------------------------------------------

  void SaveTagToCache(const Tag& tag) const;

  void SaveTagsToCache(const std::vector<std::unique_ptr<Tag>>& tags) const;

  std::vector<std::unique_ptr<Tag>> FetchTagsFromCacheByType(Tag::Type type) const;

private:
  std::unique_ptr<sql::Table> tags_tb_;

  // Utils --------------------------------------------------------

  sql::Record RecordByTag(const Tag& tag) const;

  std::unique_ptr<Tag> TagFromRecord(sql::Record* record) const;

  void UnsafeSaveTagToCache(const Tag& tag) const;


  DISALLOW_COPY_AND_ASSIGN(TagManager);
};

NS_LCC_END

#endif /* defined(LESSCHATCORE_CORE_TASK_TAG_MANAGER_H_) */

