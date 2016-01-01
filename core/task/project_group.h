#ifndef LESSCHATCORE_CORE_TASK_PROJECT_GROUP_H_
#define LESSCHATCORE_CORE_TASK_PROJECT_GROUP_H_

#include <string>
#include <memory>
#include <vector>

#include "base/base.h"

NS_LCC_BEGIN

class LCC_DLL ProjectGroup : public CodingInterface {
public:

  // Creation and lifetime --------------------------------------------------------

  ProjectGroup();

  virtual ~ProjectGroup();

  void Init(const std::string& group_id, const std::string& team_id, const std::string& owner, const std::string& name, int position);

  std::unique_ptr<ProjectGroup> Clone() const;

  // Coding interface --------------------------------------------------------

  virtual bool InitWithJsonOrDie(const std::string& json) OVERRIDE;

  // Getter/Setter --------------------------------------------------------

  std::string group_id() const { return group_id_; }
  void set_group_id(const std::string& group_id) { group_id_ = group_id; }

  std::string team_id() const { return team_id_; }
  void set_team_id(const std::string& team_id) { team_id_ = team_id; }

  std::string owner() const { return owner_; }
  void set_owner(const std::string& owner) { owner_ = owner; }

  std::string name() const { return name_; }
  void set_name(const std::string& name) { name_ = name; }

  int position() const { return position_; }
  void set_position(int position) { position_ = position; }

private:

  // Variable --------------------------------------------------------

  std::string group_id_;
  std::string team_id_;
  std::string owner_;
  std::string name_;
  int position_;


  DISALLOW_COPY_AND_ASSIGN(ProjectGroup);
};

NS_LCC_END

#endif /* defined(LESSCHATCORE_CORE_TASK_PROJECT_GROUP_H_) */

