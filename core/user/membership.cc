#include "membership.h"

#include "json11/json11.hpp"

using std::string;
using std::unique_ptr;
using std::vector;

NS_LCC_BEGIN

////////////////////////////////////////////////////////////////////////////////
// Membership, public:

// Creation and lifetime --------------------------------------------------------

Membership::Membership() {}

Membership::~Membership() {}

void Membership::Init(const std::string& membership_id, const std::string& uid, const std::string& identifier, Membership::Type type) {
  membership_id_ = membership_id;
  uid_ = uid;
  identifier_ = identifier;
  type_ = type;
}

std::unique_ptr<Membership> Membership::Clone() const {
  std::unique_ptr<Membership> membership(new Membership());
  membership->Init(membership_id_, uid_, identifier_, type_);
  return membership;
}

// Coding interface --------------------------------------------------------

bool Membership::InitWithJsonOrDie(const std::string& json) {
  string error;
  json11::Json json_obj = json11::Json::parse(json, error);

  if (!error.empty()) {
    sakura::log_error("Membership InitWithJson died");
    return false;
  }

  
  uid_ = json_obj["uid"].string_value();
  
  

  return true;
}

NS_LCC_END

