#include "com_lesschat_core_task_ListManager.h"
#include "task/list_manager.h"
#include "utils/android/jni_helper.h"

#ifdef __cplusplus
extern "C" {
#endif

JNIEXPORT jlongArray JNICALL Java_com_lesschat_core_task_ListManager_nativeFetchListsFromCache
  (JNIEnv *env, jobject thiz, jlong handler){
  const lesschat::ListManager* core_manager = reinterpret_cast<lesschat::ListManager*>(handler);

  std::vector<std::unique_ptr<lesschat::List>> core_objects = core_manager->FetchListsFromCache();

  return lesschat::JniHelper::JlongArrayFromNativeArray(std::move(core_objects));
}

JNIEXPORT jlongArray JNICALL Java_com_lesschat_core_task_ListManager_nativeFetchListsFromCacheByProjectId
  (JNIEnv *env, jobject thiz, jlong handler, jstring projectId){
  const lesschat::ListManager* core_manager = reinterpret_cast<lesschat::ListManager*>(handler);

  std::string cpp_projectId = lesschat::JniHelper::StringFromJstring(projectId);
  std::vector<std::unique_ptr<lesschat::List>> core_objects = core_manager->FetchListsFromCacheByProjectId(cpp_projectId);

  return lesschat::JniHelper::JlongArrayFromNativeArray(std::move(core_objects));
}

#ifdef __cplusplus
}
#endif
