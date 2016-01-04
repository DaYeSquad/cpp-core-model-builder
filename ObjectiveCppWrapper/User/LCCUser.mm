#if !defined(__has_feature) || !__has_feature(objc_arc)
#error "This file requires ARC support."
#endif

#import "LCCUser.h"
#import "LCCUser_CoreAddition.h"

#import "LCCObjcAdapter.h"

@implementation LCCUser

#pragma mark - Property

-(NSString *)uid {
  return [NSString stringWithUTF8String:_coreHandle->uid().c_str()];
}

-(void)setUid:(NSString *)uid {
  _coreHandle->set_uid([uid UTF8String]);
}

-(NSString *)username {
  return [NSString stringWithUTF8String:_coreHandle->username().c_str()];
}

-(void)setUsername:(NSString *)username {
  _coreHandle->set_username([username UTF8String]);
}

-(NSString *)displayName {
  return [NSString stringWithUTF8String:_coreHandle->display_name().c_str()];
}

-(void)setDisplayName:(NSString *)displayName {
  _coreHandle->set_display_name([displayName UTF8String]);
}

-(NSString *)pinyin {
  return [NSString stringWithUTF8String:_coreHandle->pinyin().c_str()];
}

-(void)setPinyin:(NSString *)pinyin {
  _coreHandle->set_pinyin([pinyin UTF8String]);
}

-(NSString *)headerUri {
  return [NSString stringWithUTF8String:_coreHandle->header_uri().c_str()];
}

-(void)setHeaderUri:(NSString *)headerUri {
  _coreHandle->set_header_uri([headerUri UTF8String]);
}

-(BOOL)isDeleted {
  return _coreHandle->is_deleted();
}

-(void)setDeleted:(BOOL)deleted {
  _coreHandle->set_deleted((BOOL)deleted);
}

-(LCCUserRole)role {
  return (LCCUserRole)_coreHandle->role();
}

-(void)setRole:(LCCUserRole)role {
  _coreHandle->set_role((LCCUserRole)role);
}

-(LCCUserState)state {
  return (LCCUserState)_coreHandle->state();
}

-(void)setState:(LCCUserState)state {
  _coreHandle->set_state((LCCUserState)state);
}

-(LCCUserStatus)status {
  return (LCCUserStatus)_coreHandle->status();
}

-(void)setStatus:(LCCUserStatus)status {
  _coreHandle->set_status((LCCUserStatus)status);
}

-(NSString *)phoneNumber {
  return [NSString stringWithUTF8String:_coreHandle->phone_number().c_str()];
}

-(void)setPhoneNumber:(NSString *)phoneNumber {
  _coreHandle->set_phone_number([phoneNumber UTF8String]);
}

-(NSString *)jobTitle {
  return [NSString stringWithUTF8String:_coreHandle->job_title().c_str()];
}

-(void)setJobTitle:(NSString *)jobTitle {
  _coreHandle->set_job_title([jobTitle UTF8String]);
}

-(NSString *)department {
  return [NSString stringWithUTF8String:_coreHandle->department().c_str()];
}

-(void)setDepartment:(NSString *)department {
  _coreHandle->set_department([department UTF8String]);
}

-(NSString *)email {
  return [NSString stringWithUTF8String:_coreHandle->email().c_str()];
}

-(void)setEmail:(NSString *)email {
  _coreHandle->set_email([email UTF8String]);
}

#pragma mark - Core Addition

+ (instancetype)userWithCoreUser:(const lesschat::User&)coreUser {
  LCCUser *user = [[LCCUser alloc] init];
  user->_coreHandle = coreUser.Clone();
  return user;
}

@end
