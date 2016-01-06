#include <jni.h>

#ifndef _Included_com_lesschat_core_task_TaskManager
#define _Included_com_lesschat_core_task_TaskManager
#ifdef __cplusplus
extern "C" {
#endif

JNIEXPORT jlong JNICALL Java_com_lesschat_core_task_TaskManager_nativeFetchTaskFromCacheByTaskId
  (JNIEnv *, jobject, jlong, jstring);

JNIEXPORT jlongArray JNICALL Java_com_lesschat_core_task_TaskManager_nativeFetchTasksFromCacheByProjectId
  (JNIEnv *, jobject, jlong, jstring);

JNIEXPORT jlongArray JNICALL Java_com_lesschat_core_task_TaskManager_nativeFetchTasksFromCacheByAssignedTo
  (JNIEnv *, jobject, jlong, jstring);

#ifdef __cplusplus
}
#endif
#endif
