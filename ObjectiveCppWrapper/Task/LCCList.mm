#if !defined(__has_feature) || !__has_feature(objc_arc)
#error "This file requires ARC support."
#endif

#import "LCCList.h"
#import "LCCList_CoreAddition.h"

#import "LCCObjcAdapter.h"

@implementation LCCList

#pragma mark - Property

-(NSString *)listId {
  return [NSString stringWithUTF8String:_coreHandle->list_id().c_str()];
}

-(void)setListId:(NSString *)listId {
  _coreHandle->set_list_id([listId UTF8String]);
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

-(NSString *)projectId {
  return [NSString stringWithUTF8String:_coreHandle->project_id().c_str()];
}

-(void)setProjectId:(NSString *)projectId {
  _coreHandle->set_project_id([projectId UTF8String]);
}

#pragma mark - Core Addition

+ (instancetype)listWithCoreList:(const lesschat::List&)coreList {
  LCCList *list = [[LCCList alloc] init];
  list->_coreHandle = coreList.Clone();
  return list;
}

@end
