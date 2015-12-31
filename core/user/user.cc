#include "user.h"

#include "json11/json11.hpp"

using std::string;
using std::unique_ptr;
using std::vector;

NS_LCC_BEGIN

////////////////////////////////////////////////////////////////////////////////
// User, public:

// Creation and lifetime --------------------------------------------------------

User::User() {}

User::~User() {}

void User::Init(const std::string& uid, const std::string& username, const std::string& display_name, const std::string& pinyin, const std::string& header_uri, bool deleted, User::Status role, User::Status state, User::Status status, const std::string& phone_number, const std::string& job_title, const std::string& department, const std::string& email) {
  uid_ = uid;
  username_ = username;
  display_name_ = display_name;
  pinyin_ = pinyin;
  header_uri_ = header_uri;
  deleted_ = deleted;
  role_ = role;
  state_ = state;
  status_ = status;
  phone_number_ = phone_number;
  job_title_ = job_title;
  department_ = department;
  email_ = email;
}

std::unique_ptr<User> User::Clone() const {
  std::unique_ptr<User> user(new User());
  user->Init(uid_, username_, display_name_, pinyin_, header_uri_, deleted_, role_, state_, status_, phone_number_, job_title_, department_, email_);
  return user;
}

// Coding interface --------------------------------------------------------

bool User::InitWithJsonOrDie(const std::string& json) {
  string error;
  json11::Json json_obj = json11::Json::parse(json, error);

  if (!error.empty()) {
    sakura::log_error("User InitWithJson died");
    return false;
  }

  uid_ = json_obj["uid"].string_value();
  username_ = json_obj["name"].string_value();
  display_name_ = json_obj["display_name"].string_value();
  pinyin_ = json_obj["display_name_pinyin"].string_value();
  header_uri_ = json_obj["avatar"].string_value();
  deleted_ = json_obj["is_deleted"].bool_value();
  role_ = static_cast<User::Status>(json_obj["role"].int_value());
  state_ = static_cast<User::Status>(json_obj["status"].int_value());
  status_ = static_cast<User::Status>(json_obj["state"].int_value());
  phone_number_ = json_obj["mobile"].string_value();
  job_title_ = json_obj["title"].string_value();
  department_ = json_obj["department"].string_value();
  email_ = json_obj["email"].string_value();

  return true;
}

NS_LCC_END

