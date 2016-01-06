#include <jni.h>

#ifndef _Included_com_lesschat_core_user_User
#define _Included_com_lesschat_core_user_User
#ifdef __cplusplus
extern "C" {
#endif

JNIEXPORT void JNICALL Java_com_lesschat_core_user_User_nativeReleaseUser
  (JNIEnv *, jobject, jlong);

JNIEXPORT jstring JNICALL Java_com_lesschat_core_user_User_nativeGetUid
  (JNIEnv *, jobject, jlong);

JNIEXPORT jstring JNICALL Java_com_lesschat_core_user_User_nativeGetUsername
  (JNIEnv *, jobject, jlong);

JNIEXPORT jstring JNICALL Java_com_lesschat_core_user_User_nativeGetDisplayName
  (JNIEnv *, jobject, jlong);

JNIEXPORT jstring JNICALL Java_com_lesschat_core_user_User_nativeGetPinyin
  (JNIEnv *, jobject, jlong);

JNIEXPORT jstring JNICALL Java_com_lesschat_core_user_User_nativeGetHeaderUri
  (JNIEnv *, jobject, jlong);

JNIEXPORT jboolean JNICALL Java_com_lesschat_core_user_User_nativeIsDeleted
  (JNIEnv *, jobject, jlong);

JNIEXPORT jint JNICALL Java_com_lesschat_core_user_User_nativeGetRole
  (JNIEnv *, jobject, jlong);

JNIEXPORT jint JNICALL Java_com_lesschat_core_user_User_nativeGetState
  (JNIEnv *, jobject, jlong);

JNIEXPORT jint JNICALL Java_com_lesschat_core_user_User_nativeGetStatus
  (JNIEnv *, jobject, jlong);

JNIEXPORT jstring JNICALL Java_com_lesschat_core_user_User_nativeGetPhoneNumber
  (JNIEnv *, jobject, jlong);

JNIEXPORT jstring JNICALL Java_com_lesschat_core_user_User_nativeGetJobTitle
  (JNIEnv *, jobject, jlong);

JNIEXPORT jstring JNICALL Java_com_lesschat_core_user_User_nativeGetDepartment
  (JNIEnv *, jobject, jlong);

JNIEXPORT jstring JNICALL Java_com_lesschat_core_user_User_nativeGetEmail
  (JNIEnv *, jobject, jlong);



#ifdef __cplusplus
}
#endif
#endif
