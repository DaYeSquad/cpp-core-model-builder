#include "com_lesschat_core_application_Tag.h"
#include "application/tag.h"
#include "utils/android/jni_helper.h"

#ifdef __cplusplus
extern "C" {
#endif

JNIEXPORT void JNICALL Java_com_lesschat_core_application_Tag_nativeReleaseTag
  (JNIEnv *env, jobject thiz, jlong handler){
  lesschat::Tag* tag = reinterpret_cast<lesschat::Tag*>(handler);
  LCC_SAFE_DELETE(tag);
}

JNIEXPORT jstring JNICALL Java_com_lesschat_core_application_Tag_nativeGetTagId
  (JNIEnv *env, jobject thiz, jlong handler){
  lesschat::Tag* tag = reinterpret_cast<lesschat::Tag*>(handler);
  return env->NewStringUTF(tag->tag_id().c_str());
}

JNIEXPORT jint JNICALL Java_com_lesschat_core_application_Tag_nativeGetType
  (JNIEnv *env, jobject thiz, jlong handler){
  lesschat::Tag* tag = reinterpret_cast<lesschat::Tag*>(handler);
  return static_cast<jint>(tag->type());
}

JNIEXPORT jstring JNICALL Java_com_lesschat_core_application_Tag_nativeGetColor
  (JNIEnv *env, jobject thiz, jlong handler){
  lesschat::Tag* tag = reinterpret_cast<lesschat::Tag*>(handler);
  return env->NewStringUTF(tag->color().c_str());
}

JNIEXPORT jstring JNICALL Java_com_lesschat_core_application_Tag_nativeGetName
  (JNIEnv *env, jobject thiz, jlong handler){
  lesschat::Tag* tag = reinterpret_cast<lesschat::Tag*>(handler);
  return env->NewStringUTF(tag->name().c_str());
}

#ifdef __cplusplus
}
#endif