#include <jni.h>

#ifndef _Included_com_lesschat_core_user_Membership
#define _Included_com_lesschat_core_user_Membership
#ifdef __cplusplus
extern "C" {
#endif

JNIEXPORT void JNICALL Java_com_lesschat_core_user_Membership_nativeReleaseMembership
  (JNIEnv *, jobject, jlong);

JNIEXPORT jstring JNICALL Java_com_lesschat_core_user_Membership_nativeGetMembershipId
  (JNIEnv *, jobject, jlong);

JNIEXPORT jstring JNICALL Java_com_lesschat_core_user_Membership_nativeGetUid
  (JNIEnv *, jobject, jlong);

JNIEXPORT jstring JNICALL Java_com_lesschat_core_user_Membership_nativeGetIdentifier
  (JNIEnv *, jobject, jlong);

JNIEXPORT jint JNICALL Java_com_lesschat_core_user_Membership_nativeGetType
  (JNIEnv *, jobject, jlong);



#ifdef __cplusplus
}
#endif
#endif
