#if !defined(__has_feature) || !__has_feature(objc_arc)
#error "This file requires ARC support."
#endif

#import "LCCTag.h"
#import "LCCTag_CoreAddition.h"

#import "LCCObjcAdapter.h"

@implementation LCCTag

#pragma mark - Property

-(NSString *)tagId {
  return [NSString stringWithUTF8String:_coreHandle->tag_id().c_str()];
}

-(void)setTagId:(NSString *)tagId {
  _coreHandle->set_tag_id([tagId UTF8String]);
}

-(LCCApplicationType)type {
  return (LCCApplicationType)_coreHandle->type();
}

-(void)setType:(LCCApplicationType)type {
  _coreHandle->set_type((LCCApplicationType)type);
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

#pragma mark - Core Addition

+ (instancetype)tagWithCoreTag:(const lesschat::Tag&)coreTag {
  LCCTag *tag = [[LCCTag alloc] init];
  tag->_coreHandle = coreTag.Clone();
  return tag;
}

@end
