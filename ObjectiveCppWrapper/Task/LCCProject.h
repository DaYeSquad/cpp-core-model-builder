#import <Foundation/Foundation.h>

typedef NS_ENUM(NSUInteger, LCCProjectVisibility) {
  LCCProjectVisibilityPublic = 0,
  LCCProjectVisibilityPrivate = 1,
  LCCProjectVisibilityPersonal = 2,
};


NS_ASSUME_NONNULL_BEGIN
@interface LCCProject : NSObject

@property (nonatomic, copy) NSString *projectId;

@property (nonatomic) LCCProjectVisibility visibility;

@property (nonatomic, copy) NSString *color;

@property (nonatomic, copy) NSString *name;

@property (nonatomic, copy) NSString *groupId;

@end
NS_ASSUME_NONNULL_END

