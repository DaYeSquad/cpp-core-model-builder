#include "com_lesschat_core_director_PermissionManager.h"
#include "director/permission_manager.h"
#include "utils/android/jni_helper.h"

#ifdef __cplusplus
extern "C" {
#endif

JNIEXPORT jlongArray JNICALL Java_com_lesschat_core_director_PermissionManager_nativeFetchPermissionsFromCache
  (JNIEnv *env, jobject thiz, jlong handler, jstring identifier, jint type){
  const lesschat::PermissionManager* core_manager = reinterpret_cast<lesschat::PermissionManager*>(handler);

  std::string cpp_identifier = lesschat::JniHelper::StringFromJstring(identifier);
  lesschat::Permission::Type cpp_type = static_cast<lesschat::Permission::Type>(type);
  std::vector<std::unique_ptr<lesschat::Permission>> core_objects = core_manager->FetchPermissionsFromCache(cpp_identifier, cpp_type);

  return lesschat::JniHelper::JlongArrayFromNativeArray(std::move(core_objects));
}

#ifdef __cplusplus
}
#endif
