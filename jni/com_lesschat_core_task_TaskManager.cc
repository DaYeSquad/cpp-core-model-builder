#include "com_lesschat_core_task_TaskManager.h"
#include "task/task_manager.h"
#include "utils/android/jni_helper.h"

#ifdef __cplusplus
extern "C" {
#endif

JNIEXPORT jlong JNICALL Java_com_lesschat_core_task_TaskManager_nativeFetchTaskFromCacheByTaskId
  (JNIEnv *env, jobject thiz, jlong handler, jstring taskId){
  const lesschat::TaskManager* core_manager = reinterpret_cast<lesschat::TaskManager*>(handler);

  std::string cpp_taskId = lesschat::JniHelper::StringFromJstring(taskId);

  std::unique_ptr<lesschat::Task> core_object = core_manager->FetchTaskFromCacheByTaskId(cpp_taskId);

  if(core_object == nullptr){
    return 0;
  }
  return reinterpret_cast<long>(core_object.release());
}

JNIEXPORT jlongArray JNICALL Java_com_lesschat_core_task_TaskManager_nativeFetchTasksFromCacheByProjectId
  (JNIEnv *env, jobject thiz, jlong handler, jstring projectId){
  const lesschat::TaskManager* core_manager = reinterpret_cast<lesschat::TaskManager*>(handler);

  std::string cpp_projectId = lesschat::JniHelper::StringFromJstring(projectId);
  std::vector<std::unique_ptr<lesschat::Task>> core_objects = core_manager->FetchTasksFromCacheByProjectId(cpp_projectId);

  return lesschat::JniHelper::JlongArrayFromNativeArray(std::move(core_objects));
}

JNIEXPORT jlongArray JNICALL Java_com_lesschat_core_task_TaskManager_nativeFetchTasksFromCacheByAssignedTo
  (JNIEnv *env, jobject thiz, jlong handler, jstring assignedTo){
  const lesschat::TaskManager* core_manager = reinterpret_cast<lesschat::TaskManager*>(handler);

  std::string cpp_assignedTo = lesschat::JniHelper::StringFromJstring(assignedTo);
  std::vector<std::unique_ptr<lesschat::Task>> core_objects = core_manager->FetchTasksFromCacheByAssignedTo(cpp_assignedTo);

  return lesschat::JniHelper::JlongArrayFromNativeArray(std::move(core_objects));
}

#ifdef __cplusplus
}
#endif
