#include <jni.h>

#ifndef _Included_com_lesschat_core_application_TagManager
#define _Included_com_lesschat_core_application_TagManager
#ifdef __cplusplus
extern "C" {
#endif

JNIEXPORT jlongArray JNICALL Java_com_lesschat_core_application_TagManager_nativeFetchTagsFromCacheByType
  (JNIEnv *, jobject, jlong, jint);

JNIEXPORT jlong JNICALL Java_com_lesschat_core_application_TagManager_nativeFetchTagFromCacheByTagId
  (JNIEnv *, jobject, jlong, jstring);

#ifdef __cplusplus
}
#endif
#endif
