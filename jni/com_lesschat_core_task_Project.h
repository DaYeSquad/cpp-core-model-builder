#include <jni.h>

#ifndef _Included_com_lesschat_core_task_Project
#define _Included_com_lesschat_core_task_Project
#ifdef __cplusplus
extern "C" {
#endif

JNIEXPORT void JNICALL Java_com_lesschat_core_task_Project_nativeReleaseProject
  (JNIEnv *, jobject, jlong);

JNIEXPORT jstring JNICALL Java_com_lesschat_core_task_Project_nativeGetProjectId
  (JNIEnv *, jobject, jlong);

JNIEXPORT jint JNICALL Java_com_lesschat_core_task_Project_nativeGetVisibility
  (JNIEnv *, jobject, jlong);

JNIEXPORT jstring JNICALL Java_com_lesschat_core_task_Project_nativeGetColor
  (JNIEnv *, jobject, jlong);

JNIEXPORT jstring JNICALL Java_com_lesschat_core_task_Project_nativeGetName
  (JNIEnv *, jobject, jlong);

JNIEXPORT jstring JNICALL Java_com_lesschat_core_task_Project_nativeGetGroupId
  (JNIEnv *, jobject, jlong);



#ifdef __cplusplus
}
#endif
#endif
