#include "project_group.h"

@interface LCCProjectGroup () {
@package
  std::unique_ptr<lesschat::ProjectGroup> _coreHandle;
}

+ (instancetype)projectGroupWithCoreProjectGroup:(const lesschat::ProjectGroup&)coreProjectGroup;

@end