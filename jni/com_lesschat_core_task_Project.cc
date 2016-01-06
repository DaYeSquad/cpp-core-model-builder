#include "com_lesschat_core_task_Project.h"
#include "task/project.h"
#include "utils/android/jni_helper.h"

#ifdef __cplusplus
extern "C" {
#endif

JNIEXPORT void JNICALL Java_com_lesschat_core_task_Project_nativeReleaseProject
  (JNIEnv *env, jobject thiz, jlong handler){
  lesschat::Project* project = reinterpret_cast<lesschat::Project*>(handler);
  LCC_SAFE_DELETE(project);
}

JNIEXPORT jstring JNICALL Java_com_lesschat_core_task_Project_nativeGetProjectId
  (JNIEnv *env, jobject thiz, jlong handler){
  lesschat::Project* project = reinterpret_cast<lesschat::Project*>(handler);
  return env->NewStringUTF(project->project_id().c_str());
}

JNIEXPORT jint JNICALL Java_com_lesschat_core_task_Project_nativeGetVisibility
  (JNIEnv *env, jobject thiz, jlong handler){
  lesschat::Project* project = reinterpret_cast<lesschat::Project*>(handler);
  return static_cast<jint>(project->visibility());
}

JNIEXPORT jstring JNICALL Java_com_lesschat_core_task_Project_nativeGetColor
  (JNIEnv *env, jobject thiz, jlong handler){
  lesschat::Project* project = reinterpret_cast<lesschat::Project*>(handler);
  return env->NewStringUTF(project->color().c_str());
}

JNIEXPORT jstring JNICALL Java_com_lesschat_core_task_Project_nativeGetName
  (JNIEnv *env, jobject thiz, jlong handler){
  lesschat::Project* project = reinterpret_cast<lesschat::Project*>(handler);
  return env->NewStringUTF(project->name().c_str());
}

JNIEXPORT jstring JNICALL Java_com_lesschat_core_task_Project_nativeGetGroupId
  (JNIEnv *env, jobject thiz, jlong handler){
  lesschat::Project* project = reinterpret_cast<lesschat::Project*>(handler);
  return env->NewStringUTF(project->group_id().c_str());
}

#ifdef __cplusplus
}
#endif