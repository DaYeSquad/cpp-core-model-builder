#include "com_lesschat_core_task_ProjectManager.h"
#include "task/project_manager.h"
#include "utils/android/jni_helper.h"

#ifdef __cplusplus
extern "C" {
#endif

JNIEXPORT jlongArray JNICALL Java_com_lesschat_core_task_ProjectManager_nativeFetchProjectsFromCache
  (JNIEnv *env, jobject thiz, jlong handler){
  const lesschat::ProjectManager* core_manager = reinterpret_cast<lesschat::ProjectManager*>(handler);

  std::vector<std::unique_ptr<lesschat::Project>> core_objects = core_manager->FetchProjectsFromCache();

  return lesschat::JniHelper::JlongArrayFromNativeArray(std::move(core_objects));
}

JNIEXPORT jlong JNICALL Java_com_lesschat_core_task_ProjectManager_nativeFetchProjectFromCacheByProjectId
  (JNIEnv *env, jobject thiz, jlong handler, jstring projectId){
  const lesschat::ProjectManager* core_manager = reinterpret_cast<lesschat::ProjectManager*>(handler);

  std::string cpp_projectId = lesschat::JniHelper::StringFromJstring(projectId);

  std::unique_ptr<lesschat::Project> core_object = core_manager->FetchProjectFromCacheByProjectId(cpp_projectId);

  if(core_object == nullptr){
    return 0;
  }
  return reinterpret_cast<long>(core_object.release());
}

#ifdef __cplusplus
}
#endif
