#include "permission.h"

@interface LCCPermission () {
@package
  std::unique_ptr<lesschat::Permission> _coreHandle;
}

+ (instancetype)permissionWithCorePermission:(const lesschat::Permission&)corePermission;

@end