#ifndef LESSCHATCORE_CORE_TASK_LIST_H_
#define LESSCHATCORE_CORE_TASK_LIST_H_

#include <string>
#include <memory>
#include <vector>

#include "base/base.h"

NS_LCC_BEGIN

class LCC_DLL List : public CodingInterface {
public:

  // Creation and lifetime --------------------------------------------------------

  List();

  virtual ~List();

  void Init(const std::string& list_id, const std::string& name, int position, const std::string& project_id);

  std::unique_ptr<List> Clone() const;

  // Coding interface --------------------------------------------------------

  virtual bool InitWithJsonOrDie(const std::string& json) OVERRIDE;

  // Getter/Setter --------------------------------------------------------

  std::string list_id() const { return list_id_; }
  void set_list_id(const std::string& list_id) { list_id_ = list_id; }

  std::string name() const { return name_; }
  void set_name(const std::string& name) { name_ = name; }

  int position() const { return position_; }
  void set_position(int position) { position_ = position; }

  std::string project_id() const { return project_id_; }
  void set_project_id(const std::string& project_id) { project_id_ = project_id; }

private:

  // Variable --------------------------------------------------------

  std::string list_id_;
  std::string name_;
  int position_;
  std::string project_id_;


  DISALLOW_COPY_AND_ASSIGN(List);
};

NS_LCC_END

#endif /* defined(LESSCHATCORE_CORE_TASK_LIST_H_) */

