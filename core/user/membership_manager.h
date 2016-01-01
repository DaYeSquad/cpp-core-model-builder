#ifndef LESSCHATCORE_CORE_USER_MEMBERSHIP_MANAGER_H_
#define LESSCHATCORE_CORE_USER_MEMBERSHIP_MANAGER_H_

#include <string>
#include <memory>
#include <vector>
#include <functional>

#include "easySQLite/easySQLite.h"

#include "base/base.h"
#include "director/object_manager.h"
#include "api/web_api.h"

#include "user/membership.h"

NS_LCC_BEGIN

class LCC_DLL MembershipManager : public ObjectManager {
public:

  // Creation and lifetime --------------------------------------------------------

  explicit MembershipManager(Director* director);

  virtual ~MembershipManager();

  bool InitOrDie();

  static const MembershipManager* DefaultManager();

  // Persisent store --------------------------------------------------------

  void SaveMembershipToCache(const Membership& membership) const;

  void SaveMembershipsToCache(const std::vector<std::unique_ptr<Membership>>& memberships) const;

  std::vector<std::unique_ptr<Membership>> FetchMembershipsFromCache(const std::string& identifier, Membership::Type type) const;

  std::unique_ptr<Membership> FetchMembershipFromCache(const std::string& uid, const std::string& identifier, Membership::Type type) const;

  void DeleteMembershipFromCache(const std::string& uid, const std::string& identifier, Membership::Type type) const;

  void DeleteMembershipsFromCache() const;

  void DeleteMembershipsFromCache(const std::string& identifier, Membership::Type type) const;

private:
  std::unique_ptr<sql::Table> memberships_tb_;

  // Utils --------------------------------------------------------

  sql::Record RecordByMembership(const Membership& membership) const;

  std::unique_ptr<Membership> MembershipFromRecord(sql::Record* record) const;

  void UnsafeSaveMembershipToCache(const Membership& membership) const;


  DISALLOW_COPY_AND_ASSIGN(MembershipManager);
};

NS_LCC_END

#endif /* defined(LESSCHATCORE_CORE_USER_MEMBERSHIP_MANAGER_H_) */

