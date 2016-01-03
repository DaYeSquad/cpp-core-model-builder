#ifndef LESSCHATCORE_CORE_APPLICATION_LIKE_H_
#define LESSCHATCORE_CORE_APPLICATION_LIKE_H_

#include <string>
#include <memory>
#include <vector>

#include "base/base.h"

NS_LCC_BEGIN

/// Decribes like in Worktile Pro applications.
///
/// @since 2.1
/// @author Frank Lin
class LCC_DLL Like : public CodingInterface {
public:

  // Creation and lifetime --------------------------------------------------------

  Like();

  virtual ~Like();

  void Init(const std::string& like_id, ApplicationType type, const std::string& application_id, const std::string& created_by, time_t created_at);

  std::unique_ptr<Like> Clone() const;

  // Coding interface --------------------------------------------------------

  virtual bool InitWithJsonOrDie(const std::string& json) OVERRIDE;

  // Getter/Setter --------------------------------------------------------

  std::string like_id() const { return like_id_; }
  void set_like_id(const std::string& like_id) { like_id_ = like_id; }

  ApplicationType type() const { return type_; }
  void set_type(ApplicationType type) { type_ = type; }

  std::string application_id() const { return application_id_; }
  void set_application_id(const std::string& application_id) { application_id_ = application_id; }

  std::string created_by() const { return created_by_; }
  void set_created_by(const std::string& created_by) { created_by_ = created_by; }

  time_t created_at() const { return created_at_; }
  void set_created_at(time_t created_at) { created_at_ = created_at; }

private:

  // Variable --------------------------------------------------------

  std::string like_id_;
  ApplicationType type_;
  std::string application_id_;
  std::string created_by_;
  time_t created_at_;


  DISALLOW_COPY_AND_ASSIGN(Like);
};

NS_LCC_END

#endif /* defined(LESSCHATCORE_CORE_APPLICATION_LIKE_H_) */

