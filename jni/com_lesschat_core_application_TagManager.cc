#include "com_lesschat_core_application_TagManager.h"
#include "application/tag_manager.h"
#include "utils/android/jni_helper.h"

#ifdef __cplusplus
extern "C" {
#endif

JNIEXPORT jlongArray JNICALL Java_com_lesschat_core_application_TagManager_nativeFetchTagsFromCacheByType
  (JNIEnv *env, jobject thiz, jlong handler, jint type){
  const lesschat::TagManager* core_manager = reinterpret_cast<lesschat::TagManager*>(handler);

  lesschat::ApplicationType cpp_type = static_cast<lesschat::ApplicationType>(type);
  std::vector<std::unique_ptr<lesschat::Tag>> core_objects = core_manager->FetchTagsFromCacheByType(cpp_type);

  return lesschat::JniHelper::JlongArrayFromNativeArray(std::move(core_objects));
}

JNIEXPORT jlong JNICALL Java_com_lesschat_core_application_TagManager_nativeFetchTagFromCacheByTagId
  (JNIEnv *env, jobject thiz, jlong handler, jstring tagId){
  const lesschat::TagManager* core_manager = reinterpret_cast<lesschat::TagManager*>(handler);

  std::string cpp_tagId = lesschat::JniHelper::StringFromJstring(tagId);

  std::unique_ptr<lesschat::Tag> core_object = core_manager->FetchTagFromCacheByTagId(cpp_tagId);

  if(core_object == nullptr){
    return 0;
  }
  return reinterpret_cast<long>(core_object.release());
}

#ifdef __cplusplus
}
#endif
