#ifndef LESSCHATCORE_CORE_CORE/TASK_TASK_MANAGER_H_
#define LESSCHATCORE_CORE_CORE/TASK_TASK_MANAGER_H_

#include <string>
#include <memory>
#include <vector>
#include <functional>

#include "easySQLite/easySQLite.h"

#include "base/base.h"
#include "director/object_manager.h"
#include "api/web_api.h"

#include "core/task/task.h"

NS_LCC_BEGIN

class LCC_DLL TaskManager : public ObjectManager {
public:

  // Creation and lifetime --------------------------------------------------------

  explicit TaskManager(Director* director);

  virtual ~TaskManager();

  bool InitOrDie();

  static const TaskManager* DefaultManager();

  // Persisent store --------------------------------------------------------

  void SaveTaskToCache(const Task& task) const;

  void SaveTasksToCache(const std::vector<std::unique_ptr<Task>>& tasks) const;

  std::unique_ptr<Task> FetchTaskFromCacheByTaskId(const std::string& task_id) const;

  std::vector<std::unique_ptr<Task>> FetchTasksFromCache() const;

  void DeleteTasksFromCacheByTaskId(const std::string& task_id) const;

  void DeleteTasksFromCacheByProjectId(const std::string& project_id) const;

private:
  std::unique_ptr<sql::Table> tasks_tb_;

  // Utils --------------------------------------------------------

  sql::Record RecordByTask(const Task& task) const;

  std::unique_ptr<Task> TaskFromRecord(sql::Record* record) const;

  void UnsafeSaveTaskToCache(const Task& task) const;


  DISALLOW_COPY_AND_ASSIGN(TaskManager);
};

NS_LCC_END

#endif /* defined(LESSCHATCORE_CORE_CORE/TASK_TASK_MANAGER_H_) */

