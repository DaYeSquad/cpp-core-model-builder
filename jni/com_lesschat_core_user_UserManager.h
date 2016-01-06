#include <jni.h>

#ifndef _Included_com_lesschat_core_user_UserManager
#define _Included_com_lesschat_core_user_UserManager
#ifdef __cplusplus
extern "C" {
#endif

JNIEXPORT jlong JNICALL Java_com_lesschat_core_user_UserManager_nativeFetchUserFromCacheByUid
  (JNIEnv *, jobject, jlong, jstring);

JNIEXPORT jlongArray JNICALL Java_com_lesschat_core_user_UserManager_nativeFetchUsersFromCache
  (JNIEnv *, jobject, jlong);

#ifdef __cplusplus
}
#endif
#endif
