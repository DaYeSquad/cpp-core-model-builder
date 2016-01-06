#include <jni.h>

#ifndef _Included_com_lesschat_core_director_Permission
#define _Included_com_lesschat_core_director_Permission
#ifdef __cplusplus
extern "C" {
#endif

JNIEXPORT void JNICALL Java_com_lesschat_core_director_Permission_nativeReleasePermission
  (JNIEnv *, jobject, jlong);

JNIEXPORT jint JNICALL Java_com_lesschat_core_director_Permission_nativeGetType
  (JNIEnv *, jobject, jlong);

JNIEXPORT jstring JNICALL Java_com_lesschat_core_director_Permission_nativeGetIdentifier
  (JNIEnv *, jobject, jlong);

JNIEXPORT jint JNICALL Java_com_lesschat_core_director_Permission_nativeGetValue
  (JNIEnv *, jobject, jlong);



#ifdef __cplusplus
}
#endif
#endif
