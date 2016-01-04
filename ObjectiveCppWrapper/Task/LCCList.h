#import <Foundation/Foundation.h>

NS_ASSUME_NONNULL_BEGIN
@interface LCCList : NSObject

@property (nonatomic, copy) NSString *listId;

@property (nonatomic, copy) NSString *name;

@property (nonatomic) NSInteger position;

@property (nonatomic, copy) NSString *projectId;

@end
NS_ASSUME_NONNULL_END

