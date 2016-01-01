#ifndef LESSCHATCORE_CORE_DIRECTOR_PERMISSION_MANAGER_H_
#define LESSCHATCORE_CORE_DIRECTOR_PERMISSION_MANAGER_H_

#include <string>
#include <memory>
#include <vector>
#include <functional>

#include "easySQLite/easySQLite.h"

#include "base/base.h"
#include "director/object_manager.h"
#include "api/web_api.h"

#include "director/permission.h"

NS_LCC_BEGIN

class LCC_DLL PermissionManager : public ObjectManager {
public:

  // Creation and lifetime --------------------------------------------------------

  explicit PermissionManager(Director* director);

  virtual ~PermissionManager();

  bool InitOrDie();

  static const PermissionManager* DefaultManager();

  // Persisent store --------------------------------------------------------

  void SavePermissionToCache(const Permission& permission) const;

  void SavePermissionsToCache(const std::vector<std::unique_ptr<Permission>>& permissions) const;

  std::vector<std::unique_ptr<Permission>> FetchPermissionsFromCache(const std::string& identifier, Permission::Type type) const;

  void DeletePermissionsFromCache() const;

  void DeletePermissionsFromCache(const std::string& identifier, Permission::Type type) const;

private:
  std::unique_ptr<sql::Table> permissions_tb_;

  // Utils --------------------------------------------------------

  sql::Record RecordByPermission(const Permission& permission) const;

  std::unique_ptr<Permission> PermissionFromRecord(sql::Record* record) const;

  void UnsafeSavePermissionToCache(const Permission& permission) const;


  DISALLOW_COPY_AND_ASSIGN(PermissionManager);
};

NS_LCC_END

#endif /* defined(LESSCHATCORE_CORE_DIRECTOR_PERMISSION_MANAGER_H_) */

