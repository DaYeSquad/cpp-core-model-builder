#include <jni.h>

#ifndef _Included_com_lesschat_core_task_ProjectGroup
#define _Included_com_lesschat_core_task_ProjectGroup
#ifdef __cplusplus
extern "C" {
#endif

JNIEXPORT void JNICALL Java_com_lesschat_core_task_ProjectGroup_nativeReleaseProjectGroup
  (JNIEnv *, jobject, jlong);

JNIEXPORT jstring JNICALL Java_com_lesschat_core_task_ProjectGroup_nativeGetGroupId
  (JNIEnv *, jobject, jlong);

JNIEXPORT jstring JNICALL Java_com_lesschat_core_task_ProjectGroup_nativeGetTeamId
  (JNIEnv *, jobject, jlong);

JNIEXPORT jstring JNICALL Java_com_lesschat_core_task_ProjectGroup_nativeGetOwner
  (JNIEnv *, jobject, jlong);

JNIEXPORT jstring JNICALL Java_com_lesschat_core_task_ProjectGroup_nativeGetName
  (JNIEnv *, jobject, jlong);

JNIEXPORT jint JNICALL Java_com_lesschat_core_task_ProjectGroup_nativeGetPosition
  (JNIEnv *, jobject, jlong);



#ifdef __cplusplus
}
#endif
#endif
