#import <Foundation/Foundation.h>

NS_ASSUME_NONNULL_BEGIN
@interface LCCTag : NSObject

@property (nonatomic, copy) NSString *tagId;

@property (nonatomic) LCCApplicationType type;

@property (nonatomic, copy) NSString *color;

@property (nonatomic, copy) NSString *name;

@end
NS_ASSUME_NONNULL_END

