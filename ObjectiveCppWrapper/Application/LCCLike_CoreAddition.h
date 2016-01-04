#include "like.h"

@interface LCCLike () {
@package
  std::unique_ptr<lesschat::Like> _coreHandle;
}

+ (instancetype)likeWithCoreLike:(const lesschat::Like&)coreLike;

@end