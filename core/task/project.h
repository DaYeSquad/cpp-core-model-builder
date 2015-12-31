#ifndef LESSCHATCORE_CORE_TASK_PROJECT_H_
#define LESSCHATCORE_CORE_TASK_PROJECT_H_

#include <string>
#include <memory>
#include <vector>

#include "base/base.h"

NS_LCC_BEGIN

class LCC_DLL Project : public CodingInterface {
public:

  enum class Visibility {
    PUBLIC = 0,
    PRIVATE = 1,
    PERSONAL = 2,
  };

  // Creation and lifetime --------------------------------------------------------

  Project();

  virtual ~Project();

  void Init(const std::string& project_id, Project::Visibility visibility, const std::string& color, const std::string& name);

  std::unique_ptr<Project> Clone() const;

  // Coding interface --------------------------------------------------------

  virtual bool InitWithJsonOrDie(const std::string& json) OVERRIDE;

  // Getter/Setter --------------------------------------------------------

  std::string project_id() const { return project_id_; }
  void set_project_id(const std::string& project_id) { project_id_ = project_id; }

  Project::Visibility visibility() const { return visibility_; }
  void set_visibility(Project::Visibility visibility) { visibility_ = visibility; }

  std::string color() const { return color_; }
  void set_color(const std::string& color) { color_ = color; }

  std::string name() const { return name_; }
  void set_name(const std::string& name) { name_ = name; }

private:

  // Variable --------------------------------------------------------

  std::string project_id_;
  Project::Visibility visibility_;
  std::string color_;
  std::string name_;


  DISALLOW_COPY_AND_ASSIGN(Project);
};

NS_LCC_END

#endif /* defined(LESSCHATCORE_CORE_TASK_PROJECT_H_) */

