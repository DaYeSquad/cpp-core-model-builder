#include "com_lesschat_core_user_User.h"
#include "user/user.h"
#include "utils/android/jni_helper.h"

#ifdef __cplusplus
extern "C" {
#endif

JNIEXPORT void JNICALL Java_com_lesschat_core_user_User_nativeReleaseUser
  (JNIEnv *env, jobject thiz, jlong handler){
  lesschat::User* user = reinterpret_cast<lesschat::User*>(handler);
  LCC_SAFE_DELETE(user);
}

JNIEXPORT jstring JNICALL Java_com_lesschat_core_user_User_nativeGetUid
  (JNIEnv *env, jobject thiz, jlong handler){
  lesschat::User* user = reinterpret_cast<lesschat::User*>(handler);
  return env->NewStringUTF(user->uid().c_str());
}

JNIEXPORT jstring JNICALL Java_com_lesschat_core_user_User_nativeGetUsername
  (JNIEnv *env, jobject thiz, jlong handler){
  lesschat::User* user = reinterpret_cast<lesschat::User*>(handler);
  return env->NewStringUTF(user->username().c_str());
}

JNIEXPORT jstring JNICALL Java_com_lesschat_core_user_User_nativeGetDisplayName
  (JNIEnv *env, jobject thiz, jlong handler){
  lesschat::User* user = reinterpret_cast<lesschat::User*>(handler);
  return env->NewStringUTF(user->display_name().c_str());
}

JNIEXPORT jstring JNICALL Java_com_lesschat_core_user_User_nativeGetPinyin
  (JNIEnv *env, jobject thiz, jlong handler){
  lesschat::User* user = reinterpret_cast<lesschat::User*>(handler);
  return env->NewStringUTF(user->pinyin().c_str());
}

JNIEXPORT jstring JNICALL Java_com_lesschat_core_user_User_nativeGetHeaderUri
  (JNIEnv *env, jobject thiz, jlong handler){
  lesschat::User* user = reinterpret_cast<lesschat::User*>(handler);
  return env->NewStringUTF(user->header_uri().c_str());
}

JNIEXPORT jboolean JNICALL Java_com_lesschat_core_user_User_nativeIsDeleted
  (JNIEnv *env, jobject thiz, jlong handler){
  lesschat::User* user = reinterpret_cast<lesschat::User*>(handler);
  return user->is_deleted();
}

JNIEXPORT jint JNICALL Java_com_lesschat_core_user_User_nativeGetRole
  (JNIEnv *env, jobject thiz, jlong handler){
  lesschat::User* user = reinterpret_cast<lesschat::User*>(handler);
  return static_cast<jint>(user->role());
}

JNIEXPORT jint JNICALL Java_com_lesschat_core_user_User_nativeGetState
  (JNIEnv *env, jobject thiz, jlong handler){
  lesschat::User* user = reinterpret_cast<lesschat::User*>(handler);
  return static_cast<jint>(user->state());
}

JNIEXPORT jint JNICALL Java_com_lesschat_core_user_User_nativeGetStatus
  (JNIEnv *env, jobject thiz, jlong handler){
  lesschat::User* user = reinterpret_cast<lesschat::User*>(handler);
  return static_cast<jint>(user->status());
}

JNIEXPORT jstring JNICALL Java_com_lesschat_core_user_User_nativeGetPhoneNumber
  (JNIEnv *env, jobject thiz, jlong handler){
  lesschat::User* user = reinterpret_cast<lesschat::User*>(handler);
  return env->NewStringUTF(user->phone_number().c_str());
}

JNIEXPORT jstring JNICALL Java_com_lesschat_core_user_User_nativeGetJobTitle
  (JNIEnv *env, jobject thiz, jlong handler){
  lesschat::User* user = reinterpret_cast<lesschat::User*>(handler);
  return env->NewStringUTF(user->job_title().c_str());
}

JNIEXPORT jstring JNICALL Java_com_lesschat_core_user_User_nativeGetDepartment
  (JNIEnv *env, jobject thiz, jlong handler){
  lesschat::User* user = reinterpret_cast<lesschat::User*>(handler);
  return env->NewStringUTF(user->department().c_str());
}

JNIEXPORT jstring JNICALL Java_com_lesschat_core_user_User_nativeGetEmail
  (JNIEnv *env, jobject thiz, jlong handler){
  lesschat::User* user = reinterpret_cast<lesschat::User*>(handler);
  return env->NewStringUTF(user->email().c_str());
}

#ifdef __cplusplus
}
#endif