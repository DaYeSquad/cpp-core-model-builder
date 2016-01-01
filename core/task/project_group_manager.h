#ifndef LESSCHATCORE_CORE_TASK_PROJECT_GROUP_MANAGER_H_
#define LESSCHATCORE_CORE_TASK_PROJECT_GROUP_MANAGER_H_

#include <string>
#include <memory>
#include <vector>
#include <functional>

#include "easySQLite/easySQLite.h"

#include "base/base.h"
#include "director/object_manager.h"
#include "api/web_api.h"

#include "task/project_group.h"

NS_LCC_BEGIN

class LCC_DLL ProjectGroupManager : public ObjectManager {
public:

  // Creation and lifetime --------------------------------------------------------

  explicit ProjectGroupManager(Director* director);

  virtual ~ProjectGroupManager();

  bool InitOrDie();

  static const ProjectGroupManager* DefaultManager();

  // Persisent store --------------------------------------------------------

  void SaveProjectGroupToCache(const ProjectGroup& projectgroup) const;

  void SaveProjectGroupsToCache(const std::vector<std::unique_ptr<ProjectGroup>>& projectgroups) const;

  std::vector<std::unique_ptr<ProjectGroup>> FetchProjectGroupsFromCache() const;

  std::unique_ptr<ProjectGroup> FetchProjectGroupFromCacheByGroupId(const std::string& group_id) const;

  void DeleteProjectGroupsFromCache() const;

private:
  std::unique_ptr<sql::Table> projectgroups_tb_;

  // Utils --------------------------------------------------------

  sql::Record RecordByProjectGroup(const ProjectGroup& projectgroup) const;

  std::unique_ptr<ProjectGroup> ProjectGroupFromRecord(sql::Record* record) const;

  void UnsafeSaveProjectGroupToCache(const ProjectGroup& projectgroup) const;


  DISALLOW_COPY_AND_ASSIGN(ProjectGroupManager);
};

NS_LCC_END

#endif /* defined(LESSCHATCORE_CORE_TASK_PROJECT_GROUP_MANAGER_H_) */

