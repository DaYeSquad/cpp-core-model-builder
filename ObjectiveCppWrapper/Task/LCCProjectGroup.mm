#if !defined(__has_feature) || !__has_feature(objc_arc)
#error "This file requires ARC support."
#endif

#import "LCCProjectGroup.h"
#import "LCCProjectGroup_CoreAddition.h"

#import "LCCObjcAdapter.h"

@implementation LCCProjectGroup

#pragma mark - Property

-(NSString *)groupId {
  return [NSString stringWithUTF8String:_coreHandle->group_id().c_str()];
}

-(void)setGroupId:(NSString *)groupId {
  _coreHandle->set_group_id([groupId UTF8String]);
}

-(NSString *)teamId {
  return [NSString stringWithUTF8String:_coreHandle->team_id().c_str()];
}

-(void)setTeamId:(NSString *)teamId {
  _coreHandle->set_team_id([teamId UTF8String]);
}

-(NSString *)owner {
  return [NSString stringWithUTF8String:_coreHandle->owner().c_str()];
}

-(void)setOwner:(NSString *)owner {
  _coreHandle->set_owner([owner UTF8String]);
}

-(NSString *)name {
  return [NSString stringWithUTF8String:_coreHandle->name().c_str()];
}

-(void)setName:(NSString *)name {
  _coreHandle->set_name([name UTF8String]);
}

-(NSInteger)position {
  return (NSInteger)_coreHandle->position();
}

-(void)setPosition:(NSInteger)position {
  _coreHandle->set_position((NSInteger)position);
}

#pragma mark - Core Addition

+ (instancetype)projectGroupWithCoreProjectGroup:(const lesschat::ProjectGroup&)coreProjectGroup {
  LCCProjectGroup *projectGroup = [[LCCProjectGroup alloc] init];
  projectGroup->_coreHandle = coreProjectGroup.Clone();
  return projectGroup;
}

@end
