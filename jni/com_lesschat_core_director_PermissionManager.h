#include <jni.h>

#ifndef _Included_com_lesschat_core_director_PermissionManager
#define _Included_com_lesschat_core_director_PermissionManager
#ifdef __cplusplus
extern "C" {
#endif

JNIEXPORT jlongArray JNICALL Java_com_lesschat_core_director_PermissionManager_nativeFetchPermissionsFromCache
  (JNIEnv *, jobject, jlong, jstring, jint);

#ifdef __cplusplus
}
#endif
#endif
