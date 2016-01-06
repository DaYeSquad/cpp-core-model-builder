#include <jni.h>

#ifndef _Included_com_lesschat_core_application_Like
#define _Included_com_lesschat_core_application_Like
#ifdef __cplusplus
extern "C" {
#endif

JNIEXPORT void JNICALL Java_com_lesschat_core_application_Like_nativeReleaseLike
  (JNIEnv *, jobject, jlong);

JNIEXPORT jstring JNICALL Java_com_lesschat_core_application_Like_nativeGetLikeId
  (JNIEnv *, jobject, jlong);

JNIEXPORT jint JNICALL Java_com_lesschat_core_application_Like_nativeGetType
  (JNIEnv *, jobject, jlong);

JNIEXPORT jstring JNICALL Java_com_lesschat_core_application_Like_nativeGetApplicationId
  (JNIEnv *, jobject, jlong);

JNIEXPORT jstring JNICALL Java_com_lesschat_core_application_Like_nativeGetCreatedBy
  (JNIEnv *, jobject, jlong);

JNIEXPORT jlong JNICALL Java_com_lesschat_core_application_Like_nativeGetCreatedAt
  (JNIEnv *, jobject, jlong);



#ifdef __cplusplus
}
#endif
#endif
