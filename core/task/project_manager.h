#ifndef LESSCHATCORE_CORE_TASK_PROJECT_MANAGER_H_
#define LESSCHATCORE_CORE_TASK_PROJECT_MANAGER_H_

#include <string>
#include <memory>
#include <vector>
#include <functional>

#include "easySQLite/easySQLite.h"

#include "base/base.h"
#include "director/object_manager.h"
#include "api/web_api.h"

#include "task/project.h"

NS_LCC_BEGIN

class LCC_DLL ProjectManager : public ObjectManager {
public:

  // Creation and lifetime --------------------------------------------------------

  explicit ProjectManager(Director* director);

  virtual ~ProjectManager();

  bool InitOrDie();

  static const ProjectManager* DefaultManager();

  // Persisent store --------------------------------------------------------

  void SaveProjectToCache(const Project& project) const;

  void SaveProjectsToCache(const std::vector<std::unique_ptr<Project>>& projects) const;

  std::vector<std::unique_ptr<Project>> FetchProjectsFromCache() const;

  std::unique_ptr<Project> FetchProjectFromCacheByProjectId(const std::string& project_id) const;

  void DeleteProjectsFromCache() const;

private:
  std::unique_ptr<sql::Table> projects_tb_;

  // Utils --------------------------------------------------------

  sql::Record RecordByProject(const Project& project) const;

  std::unique_ptr<Project> ProjectFromRecord(sql::Record* record) const;

  void UnsafeSaveProjectToCache(const Project& project) const;


  DISALLOW_COPY_AND_ASSIGN(ProjectManager);
};

NS_LCC_END

#endif /* defined(LESSCHATCORE_CORE_TASK_PROJECT_MANAGER_H_) */

