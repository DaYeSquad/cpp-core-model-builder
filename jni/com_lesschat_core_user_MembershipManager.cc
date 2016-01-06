#include "com_lesschat_core_user_MembershipManager.h"
#include "user/membership_manager.h"
#include "utils/android/jni_helper.h"

#ifdef __cplusplus
extern "C" {
#endif

JNIEXPORT jlongArray JNICALL Java_com_lesschat_core_user_MembershipManager_nativeFetchMembershipsFromCache__JLjava/lang/String_2I
  (JNIEnv *env, jobject thiz, jlong handler, jstring uid, jint type){
  const lesschat::MembershipManager* core_manager = reinterpret_cast<lesschat::MembershipManager*>(handler);

  std::string cpp_uid = lesschat::JniHelper::StringFromJstring(uid);
  lesschat::Membership::Type cpp_type = static_cast<lesschat::Membership::Type>(type);
  std::vector<std::unique_ptr<lesschat::Membership>> core_objects = core_manager->FetchMembershipsFromCache(cpp_uid, cpp_type);

  return lesschat::JniHelper::JlongArrayFromNativeArray(std::move(core_objects));
}

JNIEXPORT jlongArray JNICALL Java_com_lesschat_core_user_MembershipManager_nativeFetchMembershipsFromCache__JLjava/lang/String_2I
  (JNIEnv *env, jobject thiz, jlong handler, jstring identifier, jint type){
  const lesschat::MembershipManager* core_manager = reinterpret_cast<lesschat::MembershipManager*>(handler);

  std::string cpp_identifier = lesschat::JniHelper::StringFromJstring(identifier);
  lesschat::Membership::Type cpp_type = static_cast<lesschat::Membership::Type>(type);
  std::vector<std::unique_ptr<lesschat::Membership>> core_objects = core_manager->FetchMembershipsFromCache(cpp_identifier, cpp_type);

  return lesschat::JniHelper::JlongArrayFromNativeArray(std::move(core_objects));
}

JNIEXPORT jlong JNICALL Java_com_lesschat_core_user_MembershipManager_nativeFetchMembershipFromCache__JLjava/lang/String_2Ljava/lang/String_2I
  (JNIEnv *env, jobject thiz, jlong handler, jstring uid, jstring identifier, jint type){
  const lesschat::MembershipManager* core_manager = reinterpret_cast<lesschat::MembershipManager*>(handler);

  std::string cpp_uid = lesschat::JniHelper::StringFromJstring(uid);  std::string cpp_identifier = lesschat::JniHelper::StringFromJstring(identifier);  Membership::Type cpp_type = static_cast<lesschat::Membership::Type>(type);

  std::unique_ptr<lesschat::Membership> core_object = core_manager->FetchMembershipFromCache(cpp_uid, cpp_identifier, cpp_type);

  if(core_object == nullptr){
    return 0;
  }
  return reinterpret_cast<long>(core_object.release());
}

#ifdef __cplusplus
}
#endif
