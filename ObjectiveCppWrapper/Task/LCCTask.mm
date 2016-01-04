#if !defined(__has_feature) || !__has_feature(objc_arc)
#error "This file requires ARC support."
#endif

#import "LCCTask.h"
#import "LCCTask_CoreAddition.h"

#import "LCCObjcAdapter.h"

@implementation LCCTask

#pragma mark - Property

-(NSString *)taskId {
  return [NSString stringWithUTF8String:_coreHandle->task_id().c_str()];
}

-(void)setTaskId:(NSString *)taskId {
  _coreHandle->set_task_id([taskId UTF8String]);
}

-(NSString *)title {
  return [NSString stringWithUTF8String:_coreHandle->title().c_str()];
}

-(void)setTitle:(NSString *)title {
  _coreHandle->set_title([title UTF8String]);
}

-(NSString *)listId {
  return [NSString stringWithUTF8String:_coreHandle->list_id().c_str()];
}

-(void)setListId:(NSString *)listId {
  _coreHandle->set_list_id([listId UTF8String]);
}

-(NSString *)projectId {
  return [NSString stringWithUTF8String:_coreHandle->project_id().c_str()];
}

-(void)setProjectId:(NSString *)projectId {
  _coreHandle->set_project_id([projectId UTF8String]);
}

-(NSTimeInterval)createdAt {
  return (NSTimeInterval)_coreHandle->created_at();
}

-(void)setCreatedAt:(NSTimeInterval)createdAt {
  _coreHandle->set_created_at((NSTimeInterval)created_at);
}

-(NSString *)createdBy {
  return [NSString stringWithUTF8String:_coreHandle->created_by().c_str()];
}

-(void)setCreatedBy:(NSString *)createdBy {
  _coreHandle->set_created_by([createdBy UTF8String]);
}

-(NSTimeInterval)lastUpdatedAt {
  return (NSTimeInterval)_coreHandle->last_updated_at();
}

-(void)setLastUpdatedAt:(NSTimeInterval)lastUpdatedAt {
  _coreHandle->set_last_updated_at((NSTimeInterval)last_updated_at);
}

-(NSInteger)position {
  return (NSInteger)_coreHandle->position();
}

-(void)setPosition:(NSInteger)position {
  _coreHandle->set_position((NSInteger)position);
}

-(NSString *)taskNumber {
  return [NSString stringWithUTF8String:_coreHandle->task_number().c_str()];
}

-(void)setTaskNumber:(NSString *)taskNumber {
  _coreHandle->set_task_number([taskNumber UTF8String]);
}

-(BOOL)isArchived {
  return _coreHandle->is_archived();
}

-(void)setArchived:(BOOL)archived {
  _coreHandle->set_archived((BOOL)archived);
}

-(BOOL)isCompleted {
  return _coreHandle->is_completed();
}

-(void)setCompleted:(BOOL)completed {
  _coreHandle->set_completed((BOOL)completed);
}

-(BOOL)isDeleted {
  return _coreHandle->is_deleted();
}

-(void)setDeleted:(BOOL)deleted {
  _coreHandle->set_deleted((BOOL)deleted);
}

-(NSInteger)permission {
  return (NSInteger)_coreHandle->permission();
}

-(void)setPermission:(NSInteger)permission {
  _coreHandle->set_permission((NSInteger)permission);
}

-(NSInteger)numComments {
  return (NSInteger)_coreHandle->num_comments();
}

-(void)setNumComments:(NSInteger)numComments {
  _coreHandle->set_num_comments((NSInteger)num_comments);
}

-(NSInteger)numAttachments {
  return (NSInteger)_coreHandle->num_attachments();
}

-(void)setNumAttachments:(NSInteger)numAttachments {
  _coreHandle->set_num_attachments((NSInteger)num_attachments);
}

-(NSInteger)numChildTasks {
  return (NSInteger)_coreHandle->num_child_tasks();
}

-(void)setNumChildTasks:(NSInteger)numChildTasks {
  _coreHandle->set_num_child_tasks((NSInteger)num_child_tasks);
}

-(NSInteger)numCompletedChildTasks {
  return (NSInteger)_coreHandle->num_completed_child_tasks();
}

-(void)setNumCompletedChildTasks:(NSInteger)numCompletedChildTasks {
  _coreHandle->set_num_completed_child_tasks((NSInteger)num_completed_child_tasks);
}

-(NSInteger)numLike {
  return (NSInteger)_coreHandle->num_like();
}

-(void)setNumLike:(NSInteger)numLike {
  _coreHandle->set_num_like((NSInteger)num_like);
}

-(NSString *)assignedTo {
  return [NSString stringWithUTF8String:_coreHandle->assigned_to().c_str()];
}

-(void)setAssignedTo:(NSString *)assignedTo {
  _coreHandle->set_assigned_to([assignedTo UTF8String]);
}

-(NSString *)assignedBy {
  return [NSString stringWithUTF8String:_coreHandle->assigned_by().c_str()];
}

-(void)setAssignedBy:(NSString *)assignedBy {
  _coreHandle->set_assigned_by([assignedBy UTF8String]);
}

-(NSTimeInterval)due {
  return (NSTimeInterval)_coreHandle->due();
}

-(void)setDue:(NSTimeInterval)due {
  _coreHandle->set_due((NSTimeInterval)due);
}

-(BOOL)isWithTime {
  return _coreHandle->is_with_time();
}

-(void)setWithTime:(BOOL)withTime {
  _coreHandle->set_with_time((BOOL)with_time);
}

-(NSString<NSString *> *)tags {
  return [LCCObjcAdapter objcArrayOfNSStringFromStringVector:_coreHandle->tags()];
}

-(void)setTags:(NSArray<NSString *> *)tags {
  _coreHandle->set_tags([LCCObjcAdapter stringVectorsFromArrayOfNSString:tags];);
}

-(NSString<NSString *> *)watchers {
  return [LCCObjcAdapter objcArrayOfNSStringFromStringVector:_coreHandle->watchers()];
}

-(void)setWatchers:(NSArray<NSString *> *)watchers {
  _coreHandle->set_watchers([LCCObjcAdapter stringVectorsFromArrayOfNSString:watchers];);
}

-(NSString<NSString *> *)comments {
  return [LCCObjcAdapter objcArrayOfNSStringFromStringVector:_coreHandle->comments()];
}

-(void)setComments:(NSArray<NSString *> *)comments {
  _coreHandle->set_comments([LCCObjcAdapter stringVectorsFromArrayOfNSString:comments];);
}

-(NSString<NSString *> *)likes {
  return [LCCObjcAdapter objcArrayOfNSStringFromStringVector:_coreHandle->likes()];
}

-(void)setLikes:(NSArray<NSString *> *)likes {
  _coreHandle->set_likes([LCCObjcAdapter stringVectorsFromArrayOfNSString:likes];);
}

#pragma mark - Core Addition

+ (instancetype)taskWithCoreTask:(const lesschat::Task&)coreTask {
  LCCTask *task = [[LCCTask alloc] init];
  task->_coreHandle = coreTask.Clone();
  return task;
}

@end
