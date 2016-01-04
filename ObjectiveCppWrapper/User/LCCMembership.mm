#if !defined(__has_feature) || !__has_feature(objc_arc)
#error "This file requires ARC support."
#endif

#import "LCCMembership.h"
#import "LCCMembership_CoreAddition.h"

#import "LCCObjcAdapter.h"

@implementation LCCMembership

#pragma mark - Property

-(NSString *)membershipId {
  return [NSString stringWithUTF8String:_coreHandle->membership_id().c_str()];
}

-(void)setMembershipId:(NSString *)membershipId {
  _coreHandle->set_membership_id([membershipId UTF8String]);
}

-(NSString *)uid {
  return [NSString stringWithUTF8String:_coreHandle->uid().c_str()];
}

-(void)setUid:(NSString *)uid {
  _coreHandle->set_uid([uid UTF8String]);
}

-(NSString *)identifier {
  return [NSString stringWithUTF8String:_coreHandle->identifier().c_str()];
}

-(void)setIdentifier:(NSString *)identifier {
  _coreHandle->set_identifier([identifier UTF8String]);
}

-(LCCMembershipType)type {
  return (LCCMembershipType)_coreHandle->type();
}

-(void)setType:(LCCMembershipType)type {
  _coreHandle->set_type((LCCMembershipType)type);
}

#pragma mark - Core Addition

+ (instancetype)membershipWithCoreMembership:(const lesschat::Membership&)coreMembership {
  LCCMembership *membership = [[LCCMembership alloc] init];
  membership->_coreHandle = coreMembership.Clone();
  return membership;
}

@end
