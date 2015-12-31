#ifndef LESSCHATCORE_CORE_TASK_TASK_H_
#define LESSCHATCORE_CORE_TASK_TASK_H_

#include <string>
#include <memory>
#include <vector>

#include "base/base.h"

NS_LCC_BEGIN

class LCC_DLL Task : public CodingInterface {
public:

  enum class Type {
    NORMAL = 0,
    TEMPLATE = 1,
  };

  enum class Priority {
    LOW = 1,
    NORMAL = 2,
    HIGH = 3,
  };

  enum class Visibility {
    PUBLIC = 0,
    PRIVATE = 1,
    PERSONAL = 2,
  };

  // Creation and lifetime --------------------------------------------------------

  Task();

  virtual ~Task();

  void Init(const std::string& task_id, const std::string& title, const std::string& list_id, const std::string& project_id, time_t created_at, const std::string& created_by, time_t last_updated_at, int position, const std::string& task_number, bool archived, bool completed, bool deleted, int permission, int num_comments, int num_attachments, int num_child_tasks, int num_completed_child_tasks, int num_like, const std::string& assigned_to, const std::string& assigned_by, time_t due, const std::vector<std::string>& tags, const std::vector<std::string>& watchers, const std::vector<std::string>& comments, const std::vector<std::string>& likes);

  std::unique_ptr<Task> Clone() const;

  // Coding interface --------------------------------------------------------

  virtual bool InitWithJsonOrDie(const std::string& json) OVERRIDE;

  // Getter/Setter --------------------------------------------------------

  std::string task_id() const { return task_id_; }
  void set_task_id(const std::string& task_id) { task_id_ = task_id; }

  std::string title() const { return title_; }
  void set_title(const std::string& title) { title_ = title; }

  std::string list_id() const { return list_id_; }
  void set_list_id(const std::string& list_id) { list_id_ = list_id; }

  std::string project_id() const { return project_id_; }
  void set_project_id(const std::string& project_id) { project_id_ = project_id; }

  time_t created_at() const { return created_at_; }
  void set_created_at(time_t created_at) { created_at_ = created_at; }

  std::string created_by() const { return created_by_; }
  void set_created_by(const std::string& created_by) { created_by_ = created_by; }

  time_t last_updated_at() const { return last_updated_at_; }
  void set_last_updated_at(time_t last_updated_at) { last_updated_at_ = last_updated_at; }

  int position() const { return position_; }
  void set_position(int position) { position_ = position; }

  std::string task_number() const { return task_number_; }
  void set_task_number(const std::string& task_number) { task_number_ = task_number; }

  bool is_archived() const { return archived_; }
  void set_archived(bool archived) { archived_ = archived; }

  bool is_completed() const { return completed_; }
  void set_completed(bool completed) { completed_ = completed; }

  bool is_deleted() const { return deleted_; }
  void set_deleted(bool deleted) { deleted_ = deleted; }

  int permission() const { return permission_; }
  void set_permission(int permission) { permission_ = permission; }

  int num_comments() const { return num_comments_; }
  void set_num_comments(int num_comments) { num_comments_ = num_comments; }

  int num_attachments() const { return num_attachments_; }
  void set_num_attachments(int num_attachments) { num_attachments_ = num_attachments; }

  int num_child_tasks() const { return num_child_tasks_; }
  void set_num_child_tasks(int num_child_tasks) { num_child_tasks_ = num_child_tasks; }

  int num_completed_child_tasks() const { return num_completed_child_tasks_; }
  void set_num_completed_child_tasks(int num_completed_child_tasks) { num_completed_child_tasks_ = num_completed_child_tasks; }

  int num_like() const { return num_like_; }
  void set_num_like(int num_like) { num_like_ = num_like; }

  std::string assigned_to() const { return assigned_to_; }
  void set_assigned_to(const std::string& assigned_to) { assigned_to_ = assigned_to; }

  std::string assigned_by() const { return assigned_by_; }
  void set_assigned_by(const std::string& assigned_by) { assigned_by_ = assigned_by; }

  time_t due() const { return due_; }
  void set_due(time_t due) { due_ = due; }

  std::vector<std::string> tags() const { return tags_; }
  void set_tags(const std::vector<std::string>& tags) { tags_ = tags; }

  std::vector<std::string> watchers() const { return watchers_; }
  void set_watchers(const std::vector<std::string>& watchers) { watchers_ = watchers; }

  std::vector<std::string> comments() const { return comments_; }
  void set_comments(const std::vector<std::string>& comments) { comments_ = comments; }

  std::vector<std::string> likes() const { return likes_; }
  void set_likes(const std::vector<std::string>& likes) { likes_ = likes; }

private:

  // Variable --------------------------------------------------------

  std::string task_id_;
  std::string title_;
  std::string list_id_;
  std::string project_id_;
  time_t created_at_;
  std::string created_by_;
  time_t last_updated_at_;
  int position_;
  std::string task_number_;
  bool archived_;
  bool completed_;
  bool deleted_;
  int permission_;
  int num_comments_;
  int num_attachments_;
  int num_child_tasks_;
  int num_completed_child_tasks_;
  int num_like_;
  std::string assigned_to_;
  std::string assigned_by_;
  time_t due_;
  std::vector<std::string> tags_;
  std::vector<std::string> watchers_;
  std::vector<std::string> comments_;
  std::vector<std::string> likes_;


  DISALLOW_COPY_AND_ASSIGN(Task);
};

NS_LCC_END

#endif /* defined(LESSCHATCORE_CORE_TASK_TASK_H_) */

