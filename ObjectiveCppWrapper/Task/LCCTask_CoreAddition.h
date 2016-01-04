#include "task.h"

@interface LCCTask () {
@package
  std::unique_ptr<lesschat::Task> _coreHandle;
}

+ (instancetype)taskWithCoreTask:(const lesschat::Task&)coreTask;

@end