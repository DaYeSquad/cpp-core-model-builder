#include <jni.h>

#ifndef _Included_com_lesschat_core_task_List
#define _Included_com_lesschat_core_task_List
#ifdef __cplusplus
extern "C" {
#endif

JNIEXPORT void JNICALL Java_com_lesschat_core_task_List_nativeReleaseList
  (JNIEnv *, jobject, jlong);

JNIEXPORT jstring JNICALL Java_com_lesschat_core_task_List_nativeGetListId
  (JNIEnv *, jobject, jlong);

JNIEXPORT jstring JNICALL Java_com_lesschat_core_task_List_nativeGetName
  (JNIEnv *, jobject, jlong);

JNIEXPORT jint JNICALL Java_com_lesschat_core_task_List_nativeGetPosition
  (JNIEnv *, jobject, jlong);

JNIEXPORT jstring JNICALL Java_com_lesschat_core_task_List_nativeGetProjectId
  (JNIEnv *, jobject, jlong);



#ifdef __cplusplus
}
#endif
#endif
