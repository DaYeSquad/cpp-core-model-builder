#include <jni.h>

#ifndef _Included_com_lesschat_core_task_Task
#define _Included_com_lesschat_core_task_Task
#ifdef __cplusplus
extern "C" {
#endif

JNIEXPORT void JNICALL Java_com_lesschat_core_task_Task_nativeReleaseTask
  (JNIEnv *, jobject, jlong);

JNIEXPORT jstring JNICALL Java_com_lesschat_core_task_Task_nativeGetTaskId
  (JNIEnv *, jobject, jlong);

JNIEXPORT jstring JNICALL Java_com_lesschat_core_task_Task_nativeGetTitle
  (JNIEnv *, jobject, jlong);

JNIEXPORT jstring JNICALL Java_com_lesschat_core_task_Task_nativeGetListId
  (JNIEnv *, jobject, jlong);

JNIEXPORT jstring JNICALL Java_com_lesschat_core_task_Task_nativeGetProjectId
  (JNIEnv *, jobject, jlong);

JNIEXPORT jlong JNICALL Java_com_lesschat_core_task_Task_nativeGetCreatedAt
  (JNIEnv *, jobject, jlong);

JNIEXPORT jstring JNICALL Java_com_lesschat_core_task_Task_nativeGetCreatedBy
  (JNIEnv *, jobject, jlong);

JNIEXPORT jlong JNICALL Java_com_lesschat_core_task_Task_nativeGetLastUpdatedAt
  (JNIEnv *, jobject, jlong);

JNIEXPORT jint JNICALL Java_com_lesschat_core_task_Task_nativeGetPosition
  (JNIEnv *, jobject, jlong);

JNIEXPORT jstring JNICALL Java_com_lesschat_core_task_Task_nativeGetTaskNumber
  (JNIEnv *, jobject, jlong);

JNIEXPORT jboolean JNICALL Java_com_lesschat_core_task_Task_nativeIsArchived
  (JNIEnv *, jobject, jlong);

JNIEXPORT jboolean JNICALL Java_com_lesschat_core_task_Task_nativeIsCompleted
  (JNIEnv *, jobject, jlong);

JNIEXPORT jboolean JNICALL Java_com_lesschat_core_task_Task_nativeIsDeleted
  (JNIEnv *, jobject, jlong);

JNIEXPORT jint JNICALL Java_com_lesschat_core_task_Task_nativeGetPermission
  (JNIEnv *, jobject, jlong);

JNIEXPORT jint JNICALL Java_com_lesschat_core_task_Task_nativeGetNumComments
  (JNIEnv *, jobject, jlong);

JNIEXPORT jint JNICALL Java_com_lesschat_core_task_Task_nativeGetNumAttachments
  (JNIEnv *, jobject, jlong);

JNIEXPORT jint JNICALL Java_com_lesschat_core_task_Task_nativeGetNumChildTasks
  (JNIEnv *, jobject, jlong);

JNIEXPORT jint JNICALL Java_com_lesschat_core_task_Task_nativeGetNumCompletedChildTasks
  (JNIEnv *, jobject, jlong);

JNIEXPORT jint JNICALL Java_com_lesschat_core_task_Task_nativeGetNumLike
  (JNIEnv *, jobject, jlong);

JNIEXPORT jstring JNICALL Java_com_lesschat_core_task_Task_nativeGetAssignedTo
  (JNIEnv *, jobject, jlong);

JNIEXPORT jstring JNICALL Java_com_lesschat_core_task_Task_nativeGetAssignedBy
  (JNIEnv *, jobject, jlong);

JNIEXPORT jlong JNICALL Java_com_lesschat_core_task_Task_nativeGetDue
  (JNIEnv *, jobject, jlong);

JNIEXPORT jboolean JNICALL Java_com_lesschat_core_task_Task_nativeIsWithTime
  (JNIEnv *, jobject, jlong);

JNIEXPORT jobjectArray JNICALL Java_com_lesschat_core_task_Task_nativeGetTags
  (JNIEnv *, jobject, jlong);

JNIEXPORT jobjectArray JNICALL Java_com_lesschat_core_task_Task_nativeGetWatchers
  (JNIEnv *, jobject, jlong);

JNIEXPORT jobjectArray JNICALL Java_com_lesschat_core_task_Task_nativeGetComments
  (JNIEnv *, jobject, jlong);

JNIEXPORT jobjectArray JNICALL Java_com_lesschat_core_task_Task_nativeGetLikes
  (JNIEnv *, jobject, jlong);



#ifdef __cplusplus
}
#endif
#endif
