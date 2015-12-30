#ifndef LESSCHATCORE_CORE_CORE/TASK_TASK_H_
#define LESSCHATCORE_CORE_CORE/TASK_TASK_H_

#include <string>
#include <memory>
#include <vector>

#include "base/base.h"

NS_LCC_BEGIN

class LCC_DLL Task : public CodingInterface {
public:

  // Creation and lifetime --------------------------------------------------------

  Task();

  virtual ~Task();

  void Init(const std::string& task_id, const std::string& title, const std::string& project_id, bool archived, bool completed, bool deleted, int permission, int position, int created_at, const std::string& phone_number, const std::string& created_by, const std::vector<std::string>& tags);

  std::unqiue_ptr<Task> Clone() const;

  // Coding interface --------------------------------------------------------

  virtual bool InitWithJsonOrDie(const std::string& json) OVERRIDE;

  // Getter/Setter --------------------------------------------------------

  std::string task_id() const { return task_id_; }
  void set_task_id(const std::string& task_id) { task_id_ = task_id; }

  std::string title() const { return title_; }
  void set_title(const std::string& title) { title_ = title; }

  std::string project_id() const { return project_id_; }
  void set_project_id(const std::string& project_id) { project_id_ = project_id; }

  bool is_archived() const { return archived_; }
  void set_archived(bool archived) { archived_ = archived; }

  bool is_completed() const { return completed_; }
  void set_completed(bool completed) { completed_ = completed; }

  bool is_deleted() const { return deleted_; }
  void set_deleted(bool deleted) { deleted_ = deleted; }

  int permission() const { return permission_; }
  void set_permission(int permission) { permission_ = permission; }

  int position() const { return position_; }
  void set_position(int position) { position_ = position; }

  int created_at() const { return created_at_; }
  void set_created_at(int created_at) { created_at_ = created_at; }

  std::string phone_number() const { return phone_number_; }
  void set_phone_number(const std::string& phone_number) { phone_number_ = phone_number; }

  std::string created_by() const { return created_by_; }
  void set_created_by(const std::string& created_by) { created_by_ = created_by; }

  std::vector<std::string> tags() const { return tags_; }
  void set_tags(const std::vector<std::string>& tags) { tags_ = tags; }

private:

  // Variable --------------------------------------------------------

  std::string task_id_;
  std::string title_;
  std::string project_id_;
  bool archived_;
  bool completed_;
  bool deleted_;
  int permission_;
  int position_;
  int created_at_;
  std::string phone_number_;
  std::string created_by_;
  std::vector<std::string> tags_;


  DISALLOW_COPY_AND_ASSIGN(Task);
};

NS_LCC_END

#endif /* defined(LESSCHATCORE_CORE_CORE/TASK_TASK_H_) */

