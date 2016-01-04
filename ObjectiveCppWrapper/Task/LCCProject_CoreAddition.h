#include "project.h"

@interface LCCProject () {
@package
  std::unique_ptr<lesschat::Project> _coreHandle;
}

+ (instancetype)projectWithCoreProject:(const lesschat::Project&)coreProject;

@end