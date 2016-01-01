#include "project.h"

#include "json11/json11.hpp"

using std::string;
using std::unique_ptr;
using std::vector;

NS_LCC_BEGIN

////////////////////////////////////////////////////////////////////////////////
// Project, public:

// Creation and lifetime --------------------------------------------------------

Project::Project() {}

Project::~Project() {}

void Project::Init(const std::string& project_id, Project::Visibility visibility, const std::string& color, const std::string& name, const std::string& group_id) {
  project_id_ = project_id;
  visibility_ = visibility;
  color_ = color;
  name_ = name;
  group_id_ = group_id;
}

std::unique_ptr<Project> Project::Clone() const {
  std::unique_ptr<Project> project(new Project());
  project->Init(project_id_, visibility_, color_, name_, group_id_);
  return project;
}

// Coding interface --------------------------------------------------------

bool Project::InitWithJsonOrDie(const std::string& json) {
  string error;
  json11::Json json_obj = json11::Json::parse(json, error);

  if (!error.empty()) {
    sakura::log_error("Project InitWithJson died");
    return false;
  }

  project_id_ = json_obj["_id"].string_value();
  visibility_ = static_cast<Project::Visibility>(json_obj["visibility"].int_value());
  color_ = json_obj["color"].string_value();
  name_ = json_obj["name"].string_value();
  group_id_ = json_obj["group"].string_value();

  return true;
}

NS_LCC_END

