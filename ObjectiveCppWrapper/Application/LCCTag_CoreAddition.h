#include "tag.h"

@interface LCCTag () {
@package
  std::unique_ptr<lesschat::Tag> _coreHandle;
}

+ (instancetype)tagWithCoreTag:(const lesschat::Tag&)coreTag;

@end