#include "task.h"

#include "json11/json11.hpp"

using std::string;
using std::unique_ptr;

NS_LCC_BEGIN

////////////////////////////////////////////////////////////////////////////////
// Task, public:

// Creation and lifetime --------------------------------------------------------

Task::Task() {}

Task::~Task() {}

void Task::Init(const std::string& task_id, const std::string& title, const std::string& project_id, bool archived, bool completed, bool deleted, int permission, int position, int created_at, const std::string& phone_number, const std::string& created_by, const std::vector<std::string>& tags) {
  task_id_ = task_id;
  title_ = title;
  project_id_ = project_id;
  archived_ = archived;
  completed_ = completed;
  deleted_ = deleted;
  permission_ = permission;
  position_ = position;
  created_at_ = created_at;
  phone_number_ = phone_number;
  created_by_ = created_by;
  tags_ = tags;
}

std::unique_ptr<Task> Task::Clone() const {
  std::unique_ptr<Task> task(new Task());
  task->Init(task_id_, title_, project_id_, archived_, completed_, deleted_, permission_, position_, created_at_, phone_number_, created_by_, tags_);
  return task;
}

// Coding interface --------------------------------------------------------

bool Task::InitWithJsonOrDie(const std::string& json) {
  string error;
  json11::Json json_obj = json11::Json::parse(json, error);

  if (!error.empty()) {
    log_error("Task InitWithJson died");
    return false;
  }

  task_id_ = json_obj["task_id"].string_value();
  title_ = json_obj["title"].string_value();
  project_id_ = json_obj["project"]["project_id"].string_value();
  archived_ = json_obj["is_archived"].bool_value();
  completed_ = json_obj["is_completed"].bool_value();
  deleted_ = json_obj["is_deleted"].bool_value();
  permission_ = json_obj["permission"].int_value();
  position_ = json_obj["position"].int_value();
  created_at_ = json_obj["created_at"].int_value();
  phone_number_ = json_obj["mobile"].string_value();
  created_by_ = json_obj["created_by"].string_value();
  tags_.clear();
  vector<json11::Json> tags_json = json_obj[["tags"]].array_items();
  for (auto it = tags_json.begin(); it != tags_json.end(); ++it) {
    tags_.push_back((*it).string_value());
  }


  return true;
}

NS_LCC_END

