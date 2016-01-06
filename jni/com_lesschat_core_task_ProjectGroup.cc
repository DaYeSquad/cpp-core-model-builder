#include "com_lesschat_core_task_ProjectGroup.h"
#include "task/projectGroup.h"
#include "utils/android/jni_helper.h"

#ifdef __cplusplus
extern "C" {
#endif

JNIEXPORT void JNICALL Java_com_lesschat_core_task_ProjectGroup_nativeReleaseProjectGroup
  (JNIEnv *env, jobject thiz, jlong handler){
  lesschat::ProjectGroup* projectGroup = reinterpret_cast<lesschat::ProjectGroup*>(handler);
  LCC_SAFE_DELETE(projectGroup);
}

JNIEXPORT jstring JNICALL Java_com_lesschat_core_task_ProjectGroup_nativeGetGroupId
  (JNIEnv *env, jobject thiz, jlong handler){
  lesschat::ProjectGroup* projectGroup = reinterpret_cast<lesschat::ProjectGroup*>(handler);
  return env->NewStringUTF(projectGroup->group_id().c_str());
}

JNIEXPORT jstring JNICALL Java_com_lesschat_core_task_ProjectGroup_nativeGetTeamId
  (JNIEnv *env, jobject thiz, jlong handler){
  lesschat::ProjectGroup* projectGroup = reinterpret_cast<lesschat::ProjectGroup*>(handler);
  return env->NewStringUTF(projectGroup->team_id().c_str());
}

JNIEXPORT jstring JNICALL Java_com_lesschat_core_task_ProjectGroup_nativeGetOwner
  (JNIEnv *env, jobject thiz, jlong handler){
  lesschat::ProjectGroup* projectGroup = reinterpret_cast<lesschat::ProjectGroup*>(handler);
  return env->NewStringUTF(projectGroup->owner().c_str());
}

JNIEXPORT jstring JNICALL Java_com_lesschat_core_task_ProjectGroup_nativeGetName
  (JNIEnv *env, jobject thiz, jlong handler){
  lesschat::ProjectGroup* projectGroup = reinterpret_cast<lesschat::ProjectGroup*>(handler);
  return env->NewStringUTF(projectGroup->name().c_str());
}

JNIEXPORT jint JNICALL Java_com_lesschat_core_task_ProjectGroup_nativeGetPosition
  (JNIEnv *env, jobject thiz, jlong handler){
  lesschat::ProjectGroup* projectGroup = reinterpret_cast<lesschat::ProjectGroup*>(handler);
  return static_cast<jint>(projectGroup->position());
}

#ifdef __cplusplus
}
#endif