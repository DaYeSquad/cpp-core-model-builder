#ifndef LESSCHATCORE_CORE_USER_MEMBERSHIP_H_
#define LESSCHATCORE_CORE_USER_MEMBERSHIP_H_

#include <string>
#include <memory>
#include <vector>

#include "base/base.h"

NS_LCC_BEGIN

class LCC_DLL Membership : public CodingInterface {
public:

  enum class Type {
    USER_GROUP = 0,
    PROJECT = 1,
  };

  // Creation and lifetime --------------------------------------------------------

  Membership();

  virtual ~Membership();

  void Init(const std::string& membership_id, const std::string& uid, const std::string& identifier, Membership::Type type);

  std::unique_ptr<Membership> Clone() const;

  // Coding interface --------------------------------------------------------

  virtual bool InitWithJsonOrDie(const std::string& json) OVERRIDE;

  // Getter/Setter --------------------------------------------------------

  std::string membership_id() const { return membership_id_; }
  void set_membership_id(const std::string& membership_id) { membership_id_ = membership_id; }

  std::string uid() const { return uid_; }
  void set_uid(const std::string& uid) { uid_ = uid; }

  std::string identifier() const { return identifier_; }
  void set_identifier(const std::string& identifier) { identifier_ = identifier; }

  Membership::Type type() const { return type_; }
  void set_type(Membership::Type type) { type_ = type; }

private:

  // Variable --------------------------------------------------------

  std::string membership_id_;
  std::string uid_;
  std::string identifier_;
  Membership::Type type_;


  DISALLOW_COPY_AND_ASSIGN(Membership);
};

NS_LCC_END

#endif /* defined(LESSCHATCORE_CORE_USER_MEMBERSHIP_H_) */

