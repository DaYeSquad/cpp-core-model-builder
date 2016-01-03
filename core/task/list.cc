#include "list.h"

#include "json11/json11.hpp"

using std::string;
using std::unique_ptr;
using std::vector;

NS_LCC_BEGIN

////////////////////////////////////////////////////////////////////////////////
// List, public:

// Creation and lifetime --------------------------------------------------------

List::List() {}

List::~List() {}

void List::Init(const std::string& list_id, const std::string& name, int position, const std::string& project_id) {
  list_id_ = list_id;
  name_ = name;
  position_ = position;
  project_id_ = project_id;
}

std::unique_ptr<List> List::Clone() const {
  std::unique_ptr<List> list(new List());
  list->Init(list_id_, name_, position_, project_id_);
  return list;
}

// Coding interface --------------------------------------------------------

bool List::InitWithJsonOrDie(const std::string& json) {
  string error;
  json11::Json json_obj = json11::Json::parse(json, error);

  if (!error.empty()) {
    sakura::log_error("List InitWithJson died");
    return false;
  }

  list_id_ = json_obj["_id"].string_value();
  name_ = json_obj["name"].string_value();
  position_ = json_obj["position"].int_value();
  

  return true;
}

NS_LCC_END

