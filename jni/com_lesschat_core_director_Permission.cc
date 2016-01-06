#include "com_lesschat_core_director_Permission.h"
#include "director/permission.h"
#include "utils/android/jni_helper.h"

#ifdef __cplusplus
extern "C" {
#endif

JNIEXPORT void JNICALL Java_com_lesschat_core_director_Permission_nativeReleasePermission
  (JNIEnv *env, jobject thiz, jlong handler){
  lesschat::Permission* permission = reinterpret_cast<lesschat::Permission*>(handler);
  LCC_SAFE_DELETE(permission);
}

JNIEXPORT jint JNICALL Java_com_lesschat_core_director_Permission_nativeGetType
  (JNIEnv *env, jobject thiz, jlong handler){
  lesschat::Permission* permission = reinterpret_cast<lesschat::Permission*>(handler);
  return static_cast<jint>(permission->type());
}

JNIEXPORT jstring JNICALL Java_com_lesschat_core_director_Permission_nativeGetIdentifier
  (JNIEnv *env, jobject thiz, jlong handler){
  lesschat::Permission* permission = reinterpret_cast<lesschat::Permission*>(handler);
  return env->NewStringUTF(permission->identifier().c_str());
}

JNIEXPORT jint JNICALL Java_com_lesschat_core_director_Permission_nativeGetValue
  (JNIEnv *env, jobject thiz, jlong handler){
  lesschat::Permission* permission = reinterpret_cast<lesschat::Permission*>(handler);
  return static_cast<jint>(permission->value());
}

#ifdef __cplusplus
}
#endif