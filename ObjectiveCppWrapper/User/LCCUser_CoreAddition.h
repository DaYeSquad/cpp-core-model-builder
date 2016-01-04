#include "user.h"

@interface LCCUser () {
@package
  std::unique_ptr<lesschat::User> _coreHandle;
}

+ (instancetype)userWithCoreUser:(const lesschat::User&)coreUser;

@end