#include <jni.h>

#ifndef _Included_com_lesschat_core_task_ProjectGroupManager
#define _Included_com_lesschat_core_task_ProjectGroupManager
#ifdef __cplusplus
extern "C" {
#endif

JNIEXPORT jlongArray JNICALL Java_com_lesschat_core_task_ProjectGroupManager_nativeFetchProjectGroupsFromCache
  (JNIEnv *, jobject, jlong);

JNIEXPORT jlong JNICALL Java_com_lesschat_core_task_ProjectGroupManager_nativeFetchProjectGroupFromCacheByGroupId
  (JNIEnv *, jobject, jlong, jstring);

#ifdef __cplusplus
}
#endif
#endif
