#include "like.h"

#include "json11/json11.hpp"

using std::string;
using std::unique_ptr;
using std::vector;

NS_LCC_BEGIN

////////////////////////////////////////////////////////////////////////////////
// Like, public:

// Creation and lifetime --------------------------------------------------------

Like::Like() {}

Like::~Like() {}

void Like::Init(const std::string& like_id, ApplicationType type, const std::string& application_id, const std::string& created_by, time_t created_at) {
  like_id_ = like_id;
  type_ = type;
  application_id_ = application_id;
  created_by_ = created_by;
  created_at_ = created_at;
}

std::unique_ptr<Like> Like::Clone() const {
  std::unique_ptr<Like> like(new Like());
  like->Init(like_id_, type_, application_id_, created_by_, created_at_);
  return like;
}

// Coding interface --------------------------------------------------------

bool Like::InitWithJsonOrDie(const std::string& json) {
  string error;
  json11::Json json_obj = json11::Json::parse(json, error);

  if (!error.empty()) {
    sakura::log_error("Like InitWithJson died");
    return false;
  }

  like_id_ = json_obj["_id"].string_value();
  type_ = static_cast<ApplicationType>(json_obj["type"].int_value());
  
  created_by_ = json_obj["created_by"].string_value();
  created_at_ = json_obj["created_at"].int_value();

  return true;
}

NS_LCC_END

