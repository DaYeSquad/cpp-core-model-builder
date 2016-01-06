#include "com_lesschat_core_user_UserManager.h"
#include "user/user_manager.h"
#include "utils/android/jni_helper.h"

#ifdef __cplusplus
extern "C" {
#endif

JNIEXPORT jlong JNICALL Java_com_lesschat_core_user_UserManager_nativeFetchUserFromCacheByUid
  (JNIEnv *env, jobject thiz, jlong handler, jstring uid){
  const lesschat::UserManager* core_manager = reinterpret_cast<lesschat::UserManager*>(handler);

  std::string cpp_uid = lesschat::JniHelper::StringFromJstring(uid);

  std::unique_ptr<lesschat::User> core_object = core_manager->FetchUserFromCacheByUid(cpp_uid);

  if(core_object == nullptr){
    return 0;
  }
  return reinterpret_cast<long>(core_object.release());
}

JNIEXPORT jlongArray JNICALL Java_com_lesschat_core_user_UserManager_nativeFetchUsersFromCache
  (JNIEnv *env, jobject thiz, jlong handler){
  const lesschat::UserManager* core_manager = reinterpret_cast<lesschat::UserManager*>(handler);

  std::vector<std::unique_ptr<lesschat::User>> core_objects = core_manager->FetchUsersFromCache();

  return lesschat::JniHelper::JlongArrayFromNativeArray(std::move(core_objects));
}

#ifdef __cplusplus
}
#endif
