#include <jni.h>

#ifndef _Included_com_lesschat_core_task_ListManager
#define _Included_com_lesschat_core_task_ListManager
#ifdef __cplusplus
extern "C" {
#endif

JNIEXPORT jlongArray JNICALL Java_com_lesschat_core_task_ListManager_nativeFetchListsFromCache
  (JNIEnv *, jobject, jlong);

JNIEXPORT jlongArray JNICALL Java_com_lesschat_core_task_ListManager_nativeFetchListsFromCacheByProjectId
  (JNIEnv *, jobject, jlong, jstring);

#ifdef __cplusplus
}
#endif
#endif
