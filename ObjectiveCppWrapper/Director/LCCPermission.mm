#if !defined(__has_feature) || !__has_feature(objc_arc)
#error "This file requires ARC support."
#endif

#import "LCCPermission.h"
#import "LCCPermission_CoreAddition.h"

#import "LCCObjcAdapter.h"

@implementation LCCPermission

#pragma mark - Property

-(LCCPermissionType)type {
  return (LCCPermissionType)_coreHandle->type();
}

-(void)setType:(LCCPermissionType)type {
  _coreHandle->set_type((LCCPermissionType)type);
}

-(NSString *)identifier {
  return [NSString stringWithUTF8String:_coreHandle->identifier().c_str()];
}

-(void)setIdentifier:(NSString *)identifier {
  _coreHandle->set_identifier([identifier UTF8String]);
}

-(NSInteger)value {
  return (NSInteger)_coreHandle->value();
}

-(void)setValue:(NSInteger)value {
  _coreHandle->set_value((NSInteger)value);
}

#pragma mark - Core Addition

+ (instancetype)permissionWithCorePermission:(const lesschat::Permission&)corePermission {
  LCCPermission *permission = [[LCCPermission alloc] init];
  permission->_coreHandle = corePermission.Clone();
  return permission;
}

@end
