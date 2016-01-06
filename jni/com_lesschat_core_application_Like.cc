#include "com_lesschat_core_application_Like.h"
#include "application/like.h"
#include "utils/android/jni_helper.h"

#ifdef __cplusplus
extern "C" {
#endif

JNIEXPORT void JNICALL Java_com_lesschat_core_application_Like_nativeReleaseLike
  (JNIEnv *env, jobject thiz, jlong handler){
  lesschat::Like* like = reinterpret_cast<lesschat::Like*>(handler);
  LCC_SAFE_DELETE(like);
}

JNIEXPORT jstring JNICALL Java_com_lesschat_core_application_Like_nativeGetLikeId
  (JNIEnv *env, jobject thiz, jlong handler){
  lesschat::Like* like = reinterpret_cast<lesschat::Like*>(handler);
  return env->NewStringUTF(like->like_id().c_str());
}

JNIEXPORT jint JNICALL Java_com_lesschat_core_application_Like_nativeGetType
  (JNIEnv *env, jobject thiz, jlong handler){
  lesschat::Like* like = reinterpret_cast<lesschat::Like*>(handler);
  return static_cast<jint>(like->type());
}

JNIEXPORT jstring JNICALL Java_com_lesschat_core_application_Like_nativeGetApplicationId
  (JNIEnv *env, jobject thiz, jlong handler){
  lesschat::Like* like = reinterpret_cast<lesschat::Like*>(handler);
  return env->NewStringUTF(like->application_id().c_str());
}

JNIEXPORT jstring JNICALL Java_com_lesschat_core_application_Like_nativeGetCreatedBy
  (JNIEnv *env, jobject thiz, jlong handler){
  lesschat::Like* like = reinterpret_cast<lesschat::Like*>(handler);
  return env->NewStringUTF(like->created_by().c_str());
}

JNIEXPORT jlong JNICALL Java_com_lesschat_core_application_Like_nativeGetCreatedAt
  (JNIEnv *env, jobject thiz, jlong handler){
  lesschat::Like* like = reinterpret_cast<lesschat::Like*>(handler);
  return static_cast<jlong>(like->created_at()) * 1000;
}

#ifdef __cplusplus
}
#endif