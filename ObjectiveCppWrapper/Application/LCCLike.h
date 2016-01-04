#import <Foundation/Foundation.h>

NS_ASSUME_NONNULL_BEGIN
@interface LCCLike : NSObject

@property (nonatomic, copy) NSString *likeId;

@property (nonatomic) LCCApplicationType type;

@property (nonatomic, copy) NSString *applicationId;

@property (nonatomic, copy) NSString *createdBy;

@property (nonatomic) NSTimeInterval createdAt;

@end
NS_ASSUME_NONNULL_END

