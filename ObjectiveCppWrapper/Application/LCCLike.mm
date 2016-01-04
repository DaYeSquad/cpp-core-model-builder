#if !defined(__has_feature) || !__has_feature(objc_arc)
#error "This file requires ARC support."
#endif

#import "LCCLike.h"
#import "LCCLike_CoreAddition.h"

#import "LCCObjcAdapter.h"

@implementation LCCLike

#pragma mark - Property

-(NSString *)likeId {
  return [NSString stringWithUTF8String:_coreHandle->like_id().c_str()];
}

-(void)setLikeId:(NSString *)likeId {
  _coreHandle->set_like_id([likeId UTF8String]);
}

-(LCCApplicationType)type {
  return (LCCApplicationType)_coreHandle->type();
}

-(void)setType:(LCCApplicationType)type {
  _coreHandle->set_type((LCCApplicationType)type);
}

-(NSString *)applicationId {
  return [NSString stringWithUTF8String:_coreHandle->application_id().c_str()];
}

-(void)setApplicationId:(NSString *)applicationId {
  _coreHandle->set_application_id([applicationId UTF8String]);
}

-(NSString *)createdBy {
  return [NSString stringWithUTF8String:_coreHandle->created_by().c_str()];
}

-(void)setCreatedBy:(NSString *)createdBy {
  _coreHandle->set_created_by([createdBy UTF8String]);
}

-(NSTimeInterval)createdAt {
  return (NSTimeInterval)_coreHandle->created_at();
}

-(void)setCreatedAt:(NSTimeInterval)createdAt {
  _coreHandle->set_created_at((NSTimeInterval)created_at);
}

#pragma mark - Core Addition

+ (instancetype)likeWithCoreLike:(const lesschat::Like&)coreLike {
  LCCLike *like = [[LCCLike alloc] init];
  like->_coreHandle = coreLike.Clone();
  return like;
}

@end
