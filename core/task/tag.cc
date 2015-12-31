#include "tag.h"

#include "json11/json11.hpp"

using std::string;
using std::unique_ptr;
using std::vector;

NS_LCC_BEGIN

////////////////////////////////////////////////////////////////////////////////
// Tag, public:

// Creation and lifetime --------------------------------------------------------

Tag::Tag() {}

Tag::~Tag() {}

void Tag::Init(const std::string& tag_id, Tag::Type type, const std::string& color, const std::string& name) {
  tag_id_ = tag_id;
  type_ = type;
  color_ = color;
  name_ = name;
}

std::unique_ptr<Tag> Tag::Clone() const {
  std::unique_ptr<Tag> tag(new Tag());
  tag->Init(tag_id_, type_, color_, name_);
  return tag;
}

// Coding interface --------------------------------------------------------

bool Tag::InitWithJsonOrDie(const std::string& json) {
  string error;
  json11::Json json_obj = json11::Json::parse(json, error);

  if (!error.empty()) {
    sakura::log_error("Tag InitWithJson died");
    return false;
  }

  tag_id_ = json_obj["_id"].string_value();
  type_ = static_cast<Tag::Type>(json_obj["type"].int_value());
  color_ = json_obj["color"].string_value();
  name_ = json_obj["name"].string_value();

  return true;
}

NS_LCC_END

