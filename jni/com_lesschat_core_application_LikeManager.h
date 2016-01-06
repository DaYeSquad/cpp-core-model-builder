#include <jni.h>

#ifndef _Included_com_lesschat_core_application_LikeManager
#define _Included_com_lesschat_core_application_LikeManager
#ifdef __cplusplus
extern "C" {
#endif

JNIEXPORT jlongArray JNICALL Java_com_lesschat_core_application_LikeManager_nativeFetchLikesFromCacheByType
  (JNIEnv *, jobject, jlong, jint);

JNIEXPORT jlong JNICALL Java_com_lesschat_core_application_LikeManager_nativeFetchLikeFromCacheByLikeId
  (JNIEnv *, jobject, jlong, jstring);

JNIEXPORT jlongArray JNICALL Java_com_lesschat_core_application_LikeManager_nativeFetchLikesFromCache
  (JNIEnv *, jobject, jlong, jint, jstring);

#ifdef __cplusplus
}
#endif
#endif
