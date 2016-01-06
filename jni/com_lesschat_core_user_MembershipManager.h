#include <jni.h>

#ifndef _Included_com_lesschat_core_user_MembershipManager
#define _Included_com_lesschat_core_user_MembershipManager
#ifdef __cplusplus
extern "C" {
#endif

JNIEXPORT jlongArray JNICALL Java_com_lesschat_core_user_MembershipManager_nativeFetchMembershipsFromCache__JLjava/lang/String_2I
  (JNIEnv *, jobject, jlong, jstring, jint);

JNIEXPORT jlongArray JNICALL Java_com_lesschat_core_user_MembershipManager_nativeFetchMembershipsFromCache__JLjava/lang/String_2I
  (JNIEnv *, jobject, jlong, jstring, jint);

JNIEXPORT jlong JNICALL Java_com_lesschat_core_user_MembershipManager_nativeFetchMembershipFromCache__JLjava/lang/String_2Ljava/lang/String_2I
  (JNIEnv *, jobject, jlong, jstring, jstring, jint);

#ifdef __cplusplus
}
#endif
#endif
