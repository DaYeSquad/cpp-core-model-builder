#import <Foundation/Foundation.h>

typedef NS_ENUM(NSUInteger, LCCPermissionType) {
  LCCPermissionTypeUnknown = 0,
  LCCPermissionTypeProject = 1,
};


NS_ASSUME_NONNULL_BEGIN
@interface LCCPermission : NSObject

@property (nonatomic) LCCPermissionType type;

@property (nonatomic, copy) NSString *identifier;

@property (nonatomic) NSInteger value;

@end
NS_ASSUME_NONNULL_END

