#include "com_lesschat_core_task_Task.h"
#include "task/task.h"
#include "utils/android/jni_helper.h"

#ifdef __cplusplus
extern "C" {
#endif

JNIEXPORT void JNICALL Java_com_lesschat_core_task_Task_nativeReleaseTask
  (JNIEnv *env, jobject thiz, jlong handler){
  lesschat::Task* task = reinterpret_cast<lesschat::Task*>(handler);
  LCC_SAFE_DELETE(task);
}

JNIEXPORT jstring JNICALL Java_com_lesschat_core_task_Task_nativeGetTaskId
  (JNIEnv *env, jobject thiz, jlong handler){
  lesschat::Task* task = reinterpret_cast<lesschat::Task*>(handler);
  return env->NewStringUTF(task->task_id().c_str());
}

JNIEXPORT jstring JNICALL Java_com_lesschat_core_task_Task_nativeGetTitle
  (JNIEnv *env, jobject thiz, jlong handler){
  lesschat::Task* task = reinterpret_cast<lesschat::Task*>(handler);
  return env->NewStringUTF(task->title().c_str());
}

JNIEXPORT jstring JNICALL Java_com_lesschat_core_task_Task_nativeGetListId
  (JNIEnv *env, jobject thiz, jlong handler){
  lesschat::Task* task = reinterpret_cast<lesschat::Task*>(handler);
  return env->NewStringUTF(task->list_id().c_str());
}

JNIEXPORT jstring JNICALL Java_com_lesschat_core_task_Task_nativeGetProjectId
  (JNIEnv *env, jobject thiz, jlong handler){
  lesschat::Task* task = reinterpret_cast<lesschat::Task*>(handler);
  return env->NewStringUTF(task->project_id().c_str());
}

JNIEXPORT jlong JNICALL Java_com_lesschat_core_task_Task_nativeGetCreatedAt
  (JNIEnv *env, jobject thiz, jlong handler){
  lesschat::Task* task = reinterpret_cast<lesschat::Task*>(handler);
  return static_cast<jlong>(task->created_at()) * 1000;
}

JNIEXPORT jstring JNICALL Java_com_lesschat_core_task_Task_nativeGetCreatedBy
  (JNIEnv *env, jobject thiz, jlong handler){
  lesschat::Task* task = reinterpret_cast<lesschat::Task*>(handler);
  return env->NewStringUTF(task->created_by().c_str());
}

JNIEXPORT jlong JNICALL Java_com_lesschat_core_task_Task_nativeGetLastUpdatedAt
  (JNIEnv *env, jobject thiz, jlong handler){
  lesschat::Task* task = reinterpret_cast<lesschat::Task*>(handler);
  return static_cast<jlong>(task->last_updated_at()) * 1000;
}

JNIEXPORT jint JNICALL Java_com_lesschat_core_task_Task_nativeGetPosition
  (JNIEnv *env, jobject thiz, jlong handler){
  lesschat::Task* task = reinterpret_cast<lesschat::Task*>(handler);
  return static_cast<jint>(task->position());
}

JNIEXPORT jstring JNICALL Java_com_lesschat_core_task_Task_nativeGetTaskNumber
  (JNIEnv *env, jobject thiz, jlong handler){
  lesschat::Task* task = reinterpret_cast<lesschat::Task*>(handler);
  return env->NewStringUTF(task->task_number().c_str());
}

JNIEXPORT jboolean JNICALL Java_com_lesschat_core_task_Task_nativeIsArchived
  (JNIEnv *env, jobject thiz, jlong handler){
  lesschat::Task* task = reinterpret_cast<lesschat::Task*>(handler);
  return task->is_archived();
}

JNIEXPORT jboolean JNICALL Java_com_lesschat_core_task_Task_nativeIsCompleted
  (JNIEnv *env, jobject thiz, jlong handler){
  lesschat::Task* task = reinterpret_cast<lesschat::Task*>(handler);
  return task->is_completed();
}

JNIEXPORT jboolean JNICALL Java_com_lesschat_core_task_Task_nativeIsDeleted
  (JNIEnv *env, jobject thiz, jlong handler){
  lesschat::Task* task = reinterpret_cast<lesschat::Task*>(handler);
  return task->is_deleted();
}

JNIEXPORT jint JNICALL Java_com_lesschat_core_task_Task_nativeGetPermission
  (JNIEnv *env, jobject thiz, jlong handler){
  lesschat::Task* task = reinterpret_cast<lesschat::Task*>(handler);
  return static_cast<jint>(task->permission());
}

JNIEXPORT jint JNICALL Java_com_lesschat_core_task_Task_nativeGetNumComments
  (JNIEnv *env, jobject thiz, jlong handler){
  lesschat::Task* task = reinterpret_cast<lesschat::Task*>(handler);
  return static_cast<jint>(task->num_comments());
}

JNIEXPORT jint JNICALL Java_com_lesschat_core_task_Task_nativeGetNumAttachments
  (JNIEnv *env, jobject thiz, jlong handler){
  lesschat::Task* task = reinterpret_cast<lesschat::Task*>(handler);
  return static_cast<jint>(task->num_attachments());
}

JNIEXPORT jint JNICALL Java_com_lesschat_core_task_Task_nativeGetNumChildTasks
  (JNIEnv *env, jobject thiz, jlong handler){
  lesschat::Task* task = reinterpret_cast<lesschat::Task*>(handler);
  return static_cast<jint>(task->num_child_tasks());
}

JNIEXPORT jint JNICALL Java_com_lesschat_core_task_Task_nativeGetNumCompletedChildTasks
  (JNIEnv *env, jobject thiz, jlong handler){
  lesschat::Task* task = reinterpret_cast<lesschat::Task*>(handler);
  return static_cast<jint>(task->num_completed_child_tasks());
}

JNIEXPORT jint JNICALL Java_com_lesschat_core_task_Task_nativeGetNumLike
  (JNIEnv *env, jobject thiz, jlong handler){
  lesschat::Task* task = reinterpret_cast<lesschat::Task*>(handler);
  return static_cast<jint>(task->num_like());
}

JNIEXPORT jstring JNICALL Java_com_lesschat_core_task_Task_nativeGetAssignedTo
  (JNIEnv *env, jobject thiz, jlong handler){
  lesschat::Task* task = reinterpret_cast<lesschat::Task*>(handler);
  return env->NewStringUTF(task->assigned_to().c_str());
}

JNIEXPORT jstring JNICALL Java_com_lesschat_core_task_Task_nativeGetAssignedBy
  (JNIEnv *env, jobject thiz, jlong handler){
  lesschat::Task* task = reinterpret_cast<lesschat::Task*>(handler);
  return env->NewStringUTF(task->assigned_by().c_str());
}

JNIEXPORT jlong JNICALL Java_com_lesschat_core_task_Task_nativeGetDue
  (JNIEnv *env, jobject thiz, jlong handler){
  lesschat::Task* task = reinterpret_cast<lesschat::Task*>(handler);
  return static_cast<jlong>(task->due()) * 1000;
}

JNIEXPORT jboolean JNICALL Java_com_lesschat_core_task_Task_nativeIsWithTime
  (JNIEnv *env, jobject thiz, jlong handler){
  lesschat::Task* task = reinterpret_cast<lesschat::Task*>(handler);
  return task->is_with_time();
}

JNIEXPORT jobjectArray JNICALL Java_com_lesschat_core_task_Task_nativeGetTags
  (JNIEnv *env, jobject thiz, jlong handler){
  lesschat::Task* task = reinterpret_cast<lesschat::Task*>(handler);
  return lesschat::JniHelper::JobjectArrayFromStringVector(task->tags());
}

JNIEXPORT jobjectArray JNICALL Java_com_lesschat_core_task_Task_nativeGetWatchers
  (JNIEnv *env, jobject thiz, jlong handler){
  lesschat::Task* task = reinterpret_cast<lesschat::Task*>(handler);
  return lesschat::JniHelper::JobjectArrayFromStringVector(task->watchers());
}

JNIEXPORT jobjectArray JNICALL Java_com_lesschat_core_task_Task_nativeGetComments
  (JNIEnv *env, jobject thiz, jlong handler){
  lesschat::Task* task = reinterpret_cast<lesschat::Task*>(handler);
  return lesschat::JniHelper::JobjectArrayFromStringVector(task->comments());
}

JNIEXPORT jobjectArray JNICALL Java_com_lesschat_core_task_Task_nativeGetLikes
  (JNIEnv *env, jobject thiz, jlong handler){
  lesschat::Task* task = reinterpret_cast<lesschat::Task*>(handler);
  return lesschat::JniHelper::JobjectArrayFromStringVector(task->likes());
}

#ifdef __cplusplus
}
#endif