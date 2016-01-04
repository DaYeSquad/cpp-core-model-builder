#include "list.h"

@interface LCCList () {
@package
  std::unique_ptr<lesschat::List> _coreHandle;
}

+ (instancetype)listWithCoreList:(const lesschat::List&)coreList;

@end