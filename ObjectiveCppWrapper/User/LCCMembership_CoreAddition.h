#include "membership.h"

@interface LCCMembership () {
@package
  std::unique_ptr<lesschat::Membership> _coreHandle;
}

+ (instancetype)membershipWithCoreMembership:(const lesschat::Membership&)coreMembership;

@end