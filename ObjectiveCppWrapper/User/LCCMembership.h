#import <Foundation/Foundation.h>

typedef NS_ENUM(NSUInteger, LCCMembershipType) {
  LCCMembershipTypeUserGroup = 0,
  LCCMembershipTypeProject = 1,
};


NS_ASSUME_NONNULL_BEGIN
@interface LCCMembership : NSObject

@property (nonatomic, copy) NSString *membershipId;

@property (nonatomic, copy) NSString *uid;

@property (nonatomic, copy) NSString *identifier;

@property (nonatomic) LCCMembershipType type;

@end
NS_ASSUME_NONNULL_END

