#ifndef LESSCHATCORE_CORE_CORE/USER_USER_MANAGER_H_
#define LESSCHATCORE_CORE_CORE/USER_USER_MANAGER_H_

#include <string>
#include <memory>
#include <vector>
#include <functional>

#include "easySQLite/easySQLite.h"

#include "base/base.h"
#include "director/object_manager.h"
#include "api/web_api.h"

#include "core/user/user.h"

NS_LCC_BEGIN

class LCC_DLL UserManager : public ObjectManager {
public:

  // Creation and lifetime --------------------------------------------------------

  explicit UserManager(Director* director);

  virtual ~UserManager();

  bool InitOrDie();

  static const UserManager* DefaultManager();

  // Persisent store --------------------------------------------------------

  void SaveUserToCache(const User& user) const;

  void SaveUsersToCache(const std::vector<std::unique_ptr<User>>& users) const;

  std::unique_ptr<User> FetchUserFromCacheByUid(const std::string& uid) const;

  std::vector<std::unique_ptr<User>> FetchUsersFromCache() const;

  void DeleteUserFromCache() const;

  void DeleteUsersFromCache() const;

  void DeleteUserFromCacheByUid(const std::string& uid) const;

  void DeleteUserFromCache(const std::string& uid, const std::string& username) const;

private:
  std::unique_ptr<sql::Table> users_tb_;

  // Utils --------------------------------------------------------

  sql::Record RecordByUser(const User& user) const;

  std::unique_ptr<User> UserFromRecord(sql::Record* record) const;

  void UnsafeSaveUserToCache(const User& user) const;


  DISALLOW_COPY_AND_ASSIGN(UserManager);
};

NS_LCC_END

#endif /* defined(LESSCHATCORE_CORE_CORE/USER_USER_MANAGER_H_) */

