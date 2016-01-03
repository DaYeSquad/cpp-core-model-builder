#ifndef LESSCHATCORE_CORE_TASK_LIST_MANAGER_H_
#define LESSCHATCORE_CORE_TASK_LIST_MANAGER_H_

#include <string>
#include <memory>
#include <vector>
#include <functional>

#include "easySQLite/easySQLite.h"

#include "base/base.h"
#include "director/object_manager.h"
#include "api/web_api.h"

#include "task/list.h"

NS_LCC_BEGIN

class LCC_DLL ListManager : public ObjectManager {
public:

  // Creation and lifetime --------------------------------------------------------

  explicit ListManager(Director* director);

  virtual ~ListManager();

  bool InitOrDie();

  static const ListManager* DefaultManager();

  // Persisent store --------------------------------------------------------

  void SaveListToCache(const List& list) const;

  void SaveListsToCache(const std::vector<std::unique_ptr<List>>& lists) const;

  std::vector<std::unique_ptr<List>> FetchListsFromCache() const;

  std::vector<std::unique_ptr<List>> FetchListsFromCacheByProjectId(const std::string& project_id) const;

  void DeleteListsFromCache() const;

  void DeleteListsFromCacheByProjectId(const std::string& project_id) const;

private:
  std::unique_ptr<sql::Table> lists_tb_;

  // Utils --------------------------------------------------------

  sql::Record RecordByList(const List& list) const;

  std::unique_ptr<List> ListFromRecord(sql::Record* record) const;

  void UnsafeSaveListToCache(const List& list) const;


  DISALLOW_COPY_AND_ASSIGN(ListManager);
};

NS_LCC_END

#endif /* defined(LESSCHATCORE_CORE_TASK_LIST_MANAGER_H_) */

