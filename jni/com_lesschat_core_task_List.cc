#include "com_lesschat_core_task_List.h"
#include "task/list.h"
#include "utils/android/jni_helper.h"

#ifdef __cplusplus
extern "C" {
#endif

JNIEXPORT void JNICALL Java_com_lesschat_core_task_List_nativeReleaseList
  (JNIEnv *env, jobject thiz, jlong handler){
  lesschat::List* list = reinterpret_cast<lesschat::List*>(handler);
  LCC_SAFE_DELETE(list);
}

JNIEXPORT jstring JNICALL Java_com_lesschat_core_task_List_nativeGetListId
  (JNIEnv *env, jobject thiz, jlong handler){
  lesschat::List* list = reinterpret_cast<lesschat::List*>(handler);
  return env->NewStringUTF(list->list_id().c_str());
}

JNIEXPORT jstring JNICALL Java_com_lesschat_core_task_List_nativeGetName
  (JNIEnv *env, jobject thiz, jlong handler){
  lesschat::List* list = reinterpret_cast<lesschat::List*>(handler);
  return env->NewStringUTF(list->name().c_str());
}

JNIEXPORT jint JNICALL Java_com_lesschat_core_task_List_nativeGetPosition
  (JNIEnv *env, jobject thiz, jlong handler){
  lesschat::List* list = reinterpret_cast<lesschat::List*>(handler);
  return static_cast<jint>(list->position());
}

JNIEXPORT jstring JNICALL Java_com_lesschat_core_task_List_nativeGetProjectId
  (JNIEnv *env, jobject thiz, jlong handler){
  lesschat::List* list = reinterpret_cast<lesschat::List*>(handler);
  return env->NewStringUTF(list->project_id().c_str());
}

#ifdef __cplusplus
}
#endif