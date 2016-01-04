#import <Foundation/Foundation.h>

typedef NS_ENUM(NSUInteger, LCCTaskType) {
  LCCTaskTypeNormal = 0,
  LCCTaskTypeTemplate = 1,
};


typedef NS_ENUM(NSUInteger, LCCTaskPriority) {
  LCCTaskPriorityLow = 1,
  LCCTaskPriorityNormal = 2,
  LCCTaskPriorityHigh = 3,
};


typedef NS_ENUM(NSUInteger, LCCTaskVisibility) {
  LCCTaskVisibilityPublic = 0,
  LCCTaskVisibilityPrivate = 1,
  LCCTaskVisibilityPersonal = 2,
};


NS_ASSUME_NONNULL_BEGIN
@interface LCCTask : NSObject

@property (nonatomic, copy) NSString *taskId;

@property (nonatomic, copy) NSString *title;

@property (nonatomic, copy) NSString *listId;

@property (nonatomic, copy) NSString *projectId;

@property (nonatomic) NSTimeInterval createdAt;

@property (nonatomic, copy) NSString *createdBy;

@property (nonatomic) NSTimeInterval lastUpdatedAt;

@property (nonatomic) NSInteger position;

@property (nonatomic, copy) NSString *taskNumber;

@property (nonatomic, getter=isArchived) BOOL archived;

@property (nonatomic, getter=isCompleted) BOOL completed;

@property (nonatomic, getter=isDeleted) BOOL deleted;

@property (nonatomic) NSInteger permission;

@property (nonatomic) NSInteger numComments;

@property (nonatomic) NSInteger numAttachments;

@property (nonatomic) NSInteger numChildTasks;

@property (nonatomic) NSInteger numCompletedChildTasks;

@property (nonatomic) NSInteger numLike;

@property (nonatomic, copy) NSString *assignedTo;

@property (nonatomic, copy) NSString *assignedBy;

@property (nonatomic) NSTimeInterval due;

@property (nonatomic, getter=isWithTime) BOOL withTime;

@property (nonatomic, copy) NSArray<NSString *> *tags;

@property (nonatomic, copy) NSArray<NSString *> *watchers;

@property (nonatomic, copy) NSArray<NSString *> *comments;

@property (nonatomic, copy) NSArray<NSString *> *likes;

@end
NS_ASSUME_NONNULL_END

