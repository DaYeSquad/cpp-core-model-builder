#include <jni.h>

#ifndef _Included_com_lesschat_core_task_ProjectManager
#define _Included_com_lesschat_core_task_ProjectManager
#ifdef __cplusplus
extern "C" {
#endif

JNIEXPORT jlongArray JNICALL Java_com_lesschat_core_task_ProjectManager_nativeFetchProjectsFromCache
  (JNIEnv *, jobject, jlong);

JNIEXPORT jlong JNICALL Java_com_lesschat_core_task_ProjectManager_nativeFetchProjectFromCacheByProjectId
  (JNIEnv *, jobject, jlong, jstring);

#ifdef __cplusplus
}
#endif
#endif
