#include "permission.h"

#include "json11/json11.hpp"

using std::string;
using std::unique_ptr;
using std::vector;

NS_LCC_BEGIN

////////////////////////////////////////////////////////////////////////////////
// Permission, public:

// Creation and lifetime --------------------------------------------------------

Permission::Permission() {}

Permission::~Permission() {}

void Permission::Init(Permission::Type type, const std::string& identifier, int value) {
  type_ = type;
  identifier_ = identifier;
  value_ = value;
}

std::unique_ptr<Permission> Permission::Clone() const {
  std::unique_ptr<Permission> permission(new Permission());
  permission->Init(type_, identifier_, value_);
  return permission;
}

// Coding interface --------------------------------------------------------

bool Permission::InitWithJsonOrDie(const std::string& json) {
  string error;
  json11::Json json_obj = json11::Json::parse(json, error);

  if (!error.empty()) {
    sakura::log_error("Permission InitWithJson died");
    return false;
  }

  
  
  value_ = json_obj["permission"].int_value();

  return true;
}

NS_LCC_END

