#if !defined(__has_feature) || !__has_feature(objc_arc)
#error "This file requires ARC support."
#endif

#import "LCCProject.h"
#import "LCCProject_CoreAddition.h"

#import "LCCObjcAdapter.h"

@implementation LCCProject

#pragma mark - Property

-(NSString *)projectId {
  return [NSString stringWithUTF8String:_coreHandle->project_id().c_str()];
}

-(void)setProjectId:(NSString *)projectId {
  _coreHandle->set_project_id([projectId UTF8String]);
}

-(LCCProjectVisibility)visibility {
  return (LCCProjectVisibility)_coreHandle->visibility();
}

-(void)setVisibility:(LCCProjectVisibility)visibility {
  _coreHandle->set_visibility((LCCProjectVisibility)visibility);
}

-(NSString *)color {
  return [NSString stringWithUTF8String:_coreHandle->color().c_str()];
}

-(void)setColor:(NSString *)color {
  _coreHandle->set_color([color UTF8String]);
}

-(NSString *)name {
  return [NSString stringWithUTF8String:_coreHandle->name().c_str()];
}

-(void)setName:(NSString *)name {
  _coreHandle->set_name([name UTF8String]);
}

-(NSString *)groupId {
  return [NSString stringWithUTF8String:_coreHandle->group_id().c_str()];
}

-(void)setGroupId:(NSString *)groupId {
  _coreHandle->set_group_id([groupId UTF8String]);
}

#pragma mark - Core Addition

+ (instancetype)projectWithCoreProject:(const lesschat::Project&)coreProject {
  LCCProject *project = [[LCCProject alloc] init];
  project->_coreHandle = coreProject.Clone();
  return project;
}

@end
