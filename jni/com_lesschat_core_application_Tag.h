#include <jni.h>

#ifndef _Included_com_lesschat_core_application_Tag
#define _Included_com_lesschat_core_application_Tag
#ifdef __cplusplus
extern "C" {
#endif

JNIEXPORT void JNICALL Java_com_lesschat_core_application_Tag_nativeReleaseTag
  (JNIEnv *, jobject, jlong);

JNIEXPORT jstring JNICALL Java_com_lesschat_core_application_Tag_nativeGetTagId
  (JNIEnv *, jobject, jlong);

JNIEXPORT jint JNICALL Java_com_lesschat_core_application_Tag_nativeGetType
  (JNIEnv *, jobject, jlong);

JNIEXPORT jstring JNICALL Java_com_lesschat_core_application_Tag_nativeGetColor
  (JNIEnv *, jobject, jlong);

JNIEXPORT jstring JNICALL Java_com_lesschat_core_application_Tag_nativeGetName
  (JNIEnv *, jobject, jlong);



#ifdef __cplusplus
}
#endif
#endif
