#include "com_lesschat_core_task_ProjectGroupManager.h"
#include "task/project_group_manager.h"
#include "utils/android/jni_helper.h"

#ifdef __cplusplus
extern "C" {
#endif

JNIEXPORT jlongArray JNICALL Java_com_lesschat_core_task_ProjectGroupManager_nativeFetchProjectGroupsFromCache
  (JNIEnv *env, jobject thiz, jlong handler){
  const lesschat::ProjectGroupManager* core_manager = reinterpret_cast<lesschat::ProjectGroupManager*>(handler);

  std::vector<std::unique_ptr<lesschat::ProjectGroup>> core_objects = core_manager->FetchProjectGroupsFromCache();

  return lesschat::JniHelper::JlongArrayFromNativeArray(std::move(core_objects));
}

JNIEXPORT jlong JNICALL Java_com_lesschat_core_task_ProjectGroupManager_nativeFetchProjectGroupFromCacheByGroupId
  (JNIEnv *env, jobject thiz, jlong handler, jstring groupId){
  const lesschat::ProjectGroupManager* core_manager = reinterpret_cast<lesschat::ProjectGroupManager*>(handler);

  std::string cpp_groupId = lesschat::JniHelper::StringFromJstring(groupId);

  std::unique_ptr<lesschat::ProjectGroup> core_object = core_manager->FetchProjectGroupFromCacheByGroupId(cpp_groupId);

  if(core_object == nullptr){
    return 0;
  }
  return reinterpret_cast<long>(core_object.release());
}

#ifdef __cplusplus
}
#endif
