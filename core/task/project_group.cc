#include "project_group.h"

#include "json11/json11.hpp"

using std::string;
using std::unique_ptr;
using std::vector;

NS_LCC_BEGIN

////////////////////////////////////////////////////////////////////////////////
// ProjectGroup, public:

// Creation and lifetime --------------------------------------------------------

ProjectGroup::ProjectGroup() {}

ProjectGroup::~ProjectGroup() {}

void ProjectGroup::Init(const std::string& group_id, const std::string& team_id, const std::string& owner, const std::string& name, int position) {
  group_id_ = group_id;
  team_id_ = team_id;
  owner_ = owner;
  name_ = name;
  position_ = position;
}

std::unique_ptr<ProjectGroup> ProjectGroup::Clone() const {
  std::unique_ptr<ProjectGroup> projectgroup(new ProjectGroup());
  projectgroup->Init(group_id_, team_id_, owner_, name_, position_);
  return projectgroup;
}

// Coding interface --------------------------------------------------------

bool ProjectGroup::InitWithJsonOrDie(const std::string& json) {
  string error;
  json11::Json json_obj = json11::Json::parse(json, error);

  if (!error.empty()) {
    sakura::log_error("ProjectGroup InitWithJson died");
    return false;
  }

  group_id_ = json_obj["_id"].string_value();
  team_id_ = json_obj["team"].string_value();
  owner_ = json_obj["owner"].string_value();
  name_ = json_obj["name"].string_value();
  position_ = json_obj["position"].int_value();

  return true;
}

NS_LCC_END

