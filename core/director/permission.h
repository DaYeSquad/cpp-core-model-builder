#ifndef LESSCHATCORE_CORE_DIRECTOR_PERMISSION_H_
#define LESSCHATCORE_CORE_DIRECTOR_PERMISSION_H_

#include <string>
#include <memory>
#include <vector>

#include "base/base.h"

NS_LCC_BEGIN

class LCC_DLL Permission : public CodingInterface {
public:

  enum class Type {
    UNKNOWN = 0,
    PROJECT = 1,
  };

  // Creation and lifetime --------------------------------------------------------

  Permission();

  virtual ~Permission();

  void Init(Permission::Type type, const std::string& identifier, int value);

  std::unique_ptr<Permission> Clone() const;

  // Coding interface --------------------------------------------------------

  virtual bool InitWithJsonOrDie(const std::string& json) OVERRIDE;

  // Getter/Setter --------------------------------------------------------

  Permission::Type type() const { return type_; }
  void set_type(Permission::Type type) { type_ = type; }

  std::string identifier() const { return identifier_; }
  void set_identifier(const std::string& identifier) { identifier_ = identifier; }

  int value() const { return value_; }
  void set_value(int value) { value_ = value; }

private:

  // Variable --------------------------------------------------------

  Permission::Type type_;
  std::string identifier_;
  int value_;


  DISALLOW_COPY_AND_ASSIGN(Permission);
};

NS_LCC_END

#endif /* defined(LESSCHATCORE_CORE_DIRECTOR_PERMISSION_H_) */

