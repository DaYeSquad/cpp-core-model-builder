#include "com_lesschat_core_application_LikeManager.h"
#include "application/like_manager.h"
#include "utils/android/jni_helper.h"

#ifdef __cplusplus
extern "C" {
#endif

JNIEXPORT jlongArray JNICALL Java_com_lesschat_core_application_LikeManager_nativeFetchLikesFromCacheByType
  (JNIEnv *env, jobject thiz, jlong handler, jint type){
  const lesschat::LikeManager* core_manager = reinterpret_cast<lesschat::LikeManager*>(handler);

  lesschat::ApplicationType cpp_type = static_cast<lesschat::ApplicationType>(type);
  std::vector<std::unique_ptr<lesschat::Like>> core_objects = core_manager->FetchLikesFromCacheByType(cpp_type);

  return lesschat::JniHelper::JlongArrayFromNativeArray(std::move(core_objects));
}

JNIEXPORT jlong JNICALL Java_com_lesschat_core_application_LikeManager_nativeFetchLikeFromCacheByLikeId
  (JNIEnv *env, jobject thiz, jlong handler, jstring likeId){
  const lesschat::LikeManager* core_manager = reinterpret_cast<lesschat::LikeManager*>(handler);

  std::string cpp_likeId = lesschat::JniHelper::StringFromJstring(likeId);

  std::unique_ptr<lesschat::Like> core_object = core_manager->FetchLikeFromCacheByLikeId(cpp_likeId);

  if(core_object == nullptr){
    return 0;
  }
  return reinterpret_cast<long>(core_object.release());
}

JNIEXPORT jlongArray JNICALL Java_com_lesschat_core_application_LikeManager_nativeFetchLikesFromCache
  (JNIEnv *env, jobject thiz, jlong handler, jint type, jstring applicationId){
  const lesschat::LikeManager* core_manager = reinterpret_cast<lesschat::LikeManager*>(handler);

  lesschat::ApplicationType cpp_type = static_cast<lesschat::ApplicationType>(type);
  std::string cpp_applicationId = lesschat::JniHelper::StringFromJstring(applicationId);
  std::vector<std::unique_ptr<lesschat::Like>> core_objects = core_manager->FetchLikesFromCache(cpp_type, cpp_applicationId);

  return lesschat::JniHelper::JlongArrayFromNativeArray(std::move(core_objects));
}

#ifdef __cplusplus
}
#endif
