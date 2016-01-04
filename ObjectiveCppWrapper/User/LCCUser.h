#import <Foundation/Foundation.h>

typedef NS_ENUM(NSUInteger, LCCUserRole) {
  LCCUserRoleMember = 1,
  LCCUserRoleAdmin = 2,
  LCCUserRoleGuest = 3,
  LCCUserRoleOwner = 4,
  LCCUserRoleRobot = 5,
};


typedef NS_ENUM(NSUInteger, LCCUserStatus) {
  LCCUserStatusOffline = 0,
  LCCUserStatusOnline = 1,
  LCCUserStatusBusy = 2,
  LCCUserStatusAway = 3,
};


typedef NS_ENUM(NSUInteger, LCCUserState) {
  LCCUserStateAll = 0,
  LCCUserStateNormal = 1,
  LCCUserStateDisabled = 2,
  LCCUserStateInvited = 3,
  LCCUserStatePending = 4,
};


NS_ASSUME_NONNULL_BEGIN
@interface LCCUser : NSObject

@property (nonatomic, copy) NSString *uid;

@property (nonatomic, copy) NSString *username;

@property (nonatomic, copy) NSString *displayName;

@property (nonatomic, copy) NSString *pinyin;

@property (nonatomic, copy) NSString *headerUri;

@property (nonatomic, getter=isDeleted) BOOL deleted;

@property (nonatomic) LCCUserRole role;

@property (nonatomic) LCCUserState state;

@property (nonatomic) LCCUserStatus status;

@property (nonatomic, copy) NSString *phoneNumber;

@property (nonatomic, copy) NSString *jobTitle;

@property (nonatomic, copy) NSString *department;

@property (nonatomic, copy) NSString *email;

@end
NS_ASSUME_NONNULL_END

