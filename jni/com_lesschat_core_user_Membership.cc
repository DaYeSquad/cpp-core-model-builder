#include "com_lesschat_core_user_Membership.h"
#include "user/membership.h"
#include "utils/android/jni_helper.h"

#ifdef __cplusplus
extern "C" {
#endif

JNIEXPORT void JNICALL Java_com_lesschat_core_user_Membership_nativeReleaseMembership
  (JNIEnv *env, jobject thiz, jlong handler){
  lesschat::Membership* membership = reinterpret_cast<lesschat::Membership*>(handler);
  LCC_SAFE_DELETE(membership);
}

JNIEXPORT jstring JNICALL Java_com_lesschat_core_user_Membership_nativeGetMembershipId
  (JNIEnv *env, jobject thiz, jlong handler){
  lesschat::Membership* membership = reinterpret_cast<lesschat::Membership*>(handler);
  return env->NewStringUTF(membership->membership_id().c_str());
}

JNIEXPORT jstring JNICALL Java_com_lesschat_core_user_Membership_nativeGetUid
  (JNIEnv *env, jobject thiz, jlong handler){
  lesschat::Membership* membership = reinterpret_cast<lesschat::Membership*>(handler);
  return env->NewStringUTF(membership->uid().c_str());
}

JNIEXPORT jstring JNICALL Java_com_lesschat_core_user_Membership_nativeGetIdentifier
  (JNIEnv *env, jobject thiz, jlong handler){
  lesschat::Membership* membership = reinterpret_cast<lesschat::Membership*>(handler);
  return env->NewStringUTF(membership->identifier().c_str());
}

JNIEXPORT jint JNICALL Java_com_lesschat_core_user_Membership_nativeGetType
  (JNIEnv *env, jobject thiz, jlong handler){
  lesschat::Membership* membership = reinterpret_cast<lesschat::Membership*>(handler);
  return static_cast<jint>(membership->type());
}

#ifdef __cplusplus
}
#endif