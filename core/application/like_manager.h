#ifndef LESSCHATCORE_CORE_APPLICATION_LIKE_MANAGER_H_
#define LESSCHATCORE_CORE_APPLICATION_LIKE_MANAGER_H_

#include <string>
#include <memory>
#include <vector>
#include <functional>

#include "easySQLite/easySQLite.h"

#include "base/base.h"
#include "director/object_manager.h"
#include "api/web_api.h"

#include "application/like.h"

NS_LCC_BEGIN

class LCC_DLL LikeManager : public ObjectManager {
public:

  // Creation and lifetime --------------------------------------------------------

  explicit LikeManager(Director* director);

  virtual ~LikeManager();

  bool InitOrDie();

  static const LikeManager* DefaultManager();

  // Persisent store --------------------------------------------------------

  void SaveLikeToCache(const Like& like) const;

  void SaveLikesToCache(const std::vector<std::unique_ptr<Like>>& likes) const;

  std::vector<std::unique_ptr<Like>> FetchLikesFromCacheByType(ApplicationType type) const;

  std::unique_ptr<Like> FetchLikeFromCacheByLikeId(const std::string& like_id) const;

  std::vector<std::unique_ptr<Like>> FetchLikesFromCache(ApplicationType type, const std::string& application_id) const;

  void DeleteLikesFromCacheByType(ApplicationType type) const;

  void DeleteLikesFromCache() const;

  void DeleteLikeFromCacheByLikeId(const std::string& like_id) const;

  void DeleteLikesFromCache(ApplicationType type, const std::string& application_id) const;

  void DeleteLikeFromCache(ApplicationType type, const std::string& application_id, const std::string& created_by) const;

private:
  std::unique_ptr<sql::Table> likes_tb_;

  // Utils --------------------------------------------------------

  sql::Record RecordByLike(const Like& like) const;

  std::unique_ptr<Like> LikeFromRecord(sql::Record* record) const;

  void UnsafeSaveLikeToCache(const Like& like) const;


  DISALLOW_COPY_AND_ASSIGN(LikeManager);
};

NS_LCC_END

#endif /* defined(LESSCHATCORE_CORE_APPLICATION_LIKE_MANAGER_H_) */

