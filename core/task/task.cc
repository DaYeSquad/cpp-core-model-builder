#include "task.h"

#include "json11/json11.hpp"

using std::string;
using std::unique_ptr;
using std::vector;

NS_LCC_BEGIN

////////////////////////////////////////////////////////////////////////////////
// Task, public:

// Creation and lifetime --------------------------------------------------------

Task::Task() {}

Task::~Task() {}

void Task::Init(const std::string& task_id, const std::string& title, const std::string& list_id, const std::string& project_id, time_t created_at, const std::string& created_by, time_t last_updated_at, int position, const std::string& task_number, bool archived, bool completed, bool deleted, int permission, int num_comments, int num_attachments, int num_child_tasks, int num_completed_child_tasks, int num_like, const std::string& assigned_to, const std::string& assigned_by, time_t due, const std::vector<std::string>& tags, const std::vector<std::string>& watchers, const std::vector<std::string>& comments, const std::vector<std::string>& likes) {
  task_id_ = task_id;
  title_ = title;
  list_id_ = list_id;
  project_id_ = project_id;
  created_at_ = created_at;
  created_by_ = created_by;
  last_updated_at_ = last_updated_at;
  position_ = position;
  task_number_ = task_number;
  archived_ = archived;
  completed_ = completed;
  deleted_ = deleted;
  permission_ = permission;
  num_comments_ = num_comments;
  num_attachments_ = num_attachments;
  num_child_tasks_ = num_child_tasks;
  num_completed_child_tasks_ = num_completed_child_tasks;
  num_like_ = num_like;
  assigned_to_ = assigned_to;
  assigned_by_ = assigned_by;
  due_ = due;
  tags_ = tags;
  watchers_ = watchers;
  comments_ = comments;
  likes_ = likes;
}

std::unique_ptr<Task> Task::Clone() const {
  std::unique_ptr<Task> task(new Task());
  task->Init(task_id_, title_, list_id_, project_id_, created_at_, created_by_, last_updated_at_, position_, task_number_, archived_, completed_, deleted_, permission_, num_comments_, num_attachments_, num_child_tasks_, num_completed_child_tasks_, num_like_, assigned_to_, assigned_by_, due_, tags_, watchers_, comments_, likes_);
  return task;
}

// Coding interface --------------------------------------------------------

bool Task::InitWithJsonOrDie(const std::string& json) {
  string error;
  json11::Json json_obj = json11::Json::parse(json, error);

  if (!error.empty()) {
    sakura::log_error("Task InitWithJson died");
    return false;
  }

  task_id_ = json_obj["_id"].string_value();
  title_ = json_obj["title"].string_value();
  list_id_ = json_obj["entry"].string_value();
  project_id_ = json_obj["project"]["_id"].string_value();
  created_at_ = json_obj["created_at"].int_value();
  created_by_ = json_obj["created_by"].string_value();
  last_updated_at_ = json_obj["updated_at"].int_value();
  position_ = json_obj["position"].int_value();
  task_number_ = json_obj["identifier"].string_value();
  archived_ = json_obj["is_archived"].bool_value();
  completed_ = json_obj["completion"]["is_completed"].bool_value();
  deleted_ = json_obj["is_deleted"].bool_value();
  permission_ = json_obj["permission"].int_value();
  num_comments_ = json_obj["comment_count"].int_value();
  num_attachments_ = json_obj["attachment_count"].int_value();
  num_child_tasks_ = json_obj["children_count"].int_value();
  num_completed_child_tasks_ = json_obj["completed_children_count"].int_value();
  num_like_ = json_obj["like_count"].int_value();
  assigned_to_ = json_obj["asignee"]["uid"].string_value();
  assigned_by_ = json_obj["assigner"]["uid"].string_value();
  due_ = json_obj["due_date"]["date"].int_value();
  tags_.clear();
  vector<json11::Json> tags_json = json_obj["tags"].array_items();
  for (auto it = tags_json.begin(); it != tags_json.end(); ++it) {
    tags_.push_back((*it)["uid"].string_value());
  }

  watchers_.clear();
  vector<json11::Json> watchers_json = json_obj["watchers"].array_items();
  for (auto it = watchers_json.begin(); it != watchers_json.end(); ++it) {
    watchers_.push_back((*it)["uid"].string_value());
  }

  comments_.clear();
  vector<json11::Json> comments_json = json_obj["comments"].array_items();
  for (auto it = comments_json.begin(); it != comments_json.end(); ++it) {
    comments_.push_back((*it)["uid"].string_value());
  }

  likes_.clear();
  vector<json11::Json> likes_json = json_obj["likes"].array_items();
  for (auto it = likes_json.begin(); it != likes_json.end(); ++it) {
    likes_.push_back((*it)["uid"].string_value());
  }


  return true;
}

NS_LCC_END

