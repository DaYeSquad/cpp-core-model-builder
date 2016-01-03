#ifndef LESSCHATCORE_CORE_APPLICATION_TAG_H_
#define LESSCHATCORE_CORE_APPLICATION_TAG_H_

#include <string>
#include <memory>
#include <vector>

#include "base/base.h"

NS_LCC_BEGIN

class LCC_DLL Tag : public CodingInterface {
public:

  // Creation and lifetime --------------------------------------------------------

  Tag();

  virtual ~Tag();

  void Init(const std::string& tag_id, ApplicationType type, const std::string& color, const std::string& name);

  std::unique_ptr<Tag> Clone() const;

  // Coding interface --------------------------------------------------------

  virtual bool InitWithJsonOrDie(const std::string& json) OVERRIDE;

  // Getter/Setter --------------------------------------------------------

  std::string tag_id() const { return tag_id_; }
  void set_tag_id(const std::string& tag_id) { tag_id_ = tag_id; }

  ApplicationType type() const { return type_; }
  void set_type(ApplicationType type) { type_ = type; }

  std::string color() const { return color_; }
  void set_color(const std::string& color) { color_ = color; }

  std::string name() const { return name_; }
  void set_name(const std::string& name) { name_ = name; }

private:

  // Variable --------------------------------------------------------

  std::string tag_id_;
  ApplicationType type_;
  std::string color_;
  std::string name_;


  DISALLOW_COPY_AND_ASSIGN(Tag);
};

NS_LCC_END

#endif /* defined(LESSCHATCORE_CORE_APPLICATION_TAG_H_) */

