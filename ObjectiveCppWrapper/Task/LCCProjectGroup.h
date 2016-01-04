#import <Foundation/Foundation.h>

NS_ASSUME_NONNULL_BEGIN
@interface LCCProjectGroup : NSObject

@property (nonatomic, copy) NSString *groupId;

@property (nonatomic, copy) NSString *teamId;

@property (nonatomic, copy) NSString *owner;

@property (nonatomic, copy) NSString *name;

@property (nonatomic) NSInteger position;

@end
NS_ASSUME_NONNULL_END

