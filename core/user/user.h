#ifndef LESSCHATCORE_CORE_USER_USER_H_
#define LESSCHATCORE_CORE_USER_USER_H_

#include <string>
#include <memory>
#include <vector>

#include "base/base.h"

NS_LCC_BEGIN

class LCC_DLL User : public CodingInterface {
public:

  enum class Role {
    MEMBER = 1,
    ADMIN = 2,
    GUEST = 3,
    OWNER = 4,
    ROBOT = 5,
  };

  enum class Status {
    OFFLINE = 0,
    ONLINE = 1,
    BUSY = 2,
    AWAY = 3,
  };

  enum class State {
    ALL = 0,
    NORMAL = 1,
    DISABLED = 2,
    INVITED = 3,
    PENDING = 4,
  };

  // Creation and lifetime --------------------------------------------------------

  User();

  virtual ~User();

  void Init(const std::string& uid, const std::string& username, const std::string& display_name, const std::string& pinyin, const std::string& header_uri, bool deleted, User::Status role, User::Status state, User::Status status, const std::string& phone_number, const std::string& job_title, const std::string& department, const std::string& email);

  std::unique_ptr<User> Clone() const;

  // Coding interface --------------------------------------------------------

  virtual bool InitWithJsonOrDie(const std::string& json) OVERRIDE;

  // Getter/Setter --------------------------------------------------------

  std::string uid() const { return uid_; }
  void set_uid(const std::string& uid) { uid_ = uid; }

  std::string username() const { return username_; }
  void set_username(const std::string& username) { username_ = username; }

  std::string display_name() const { return display_name_; }
  void set_display_name(const std::string& display_name) { display_name_ = display_name; }

  std::string pinyin() const { return pinyin_; }
  void set_pinyin(const std::string& pinyin) { pinyin_ = pinyin; }

  std::string header_uri() const { return header_uri_; }
  void set_header_uri(const std::string& header_uri) { header_uri_ = header_uri; }

  bool is_deleted() const { return deleted_; }
  void set_deleted(bool deleted) { deleted_ = deleted; }

  User::Status role() const { return role_; }
  void set_role(User::Status role) { role_ = role; }

  User::Status state() const { return state_; }
  void set_state(User::Status state) { state_ = state; }

  User::Status status() const { return status_; }
  void set_status(User::Status status) { status_ = status; }

  std::string phone_number() const { return phone_number_; }
  void set_phone_number(const std::string& phone_number) { phone_number_ = phone_number; }

  std::string job_title() const { return job_title_; }
  void set_job_title(const std::string& job_title) { job_title_ = job_title; }

  std::string department() const { return department_; }
  void set_department(const std::string& department) { department_ = department; }

  std::string email() const { return email_; }
  void set_email(const std::string& email) { email_ = email; }

private:

  // Variable --------------------------------------------------------

  std::string uid_;
  std::string username_;
  std::string display_name_;
  std::string pinyin_;
  std::string header_uri_;
  bool deleted_;
  User::Status role_;
  User::Status state_;
  User::Status status_;
  std::string phone_number_;
  std::string job_title_;
  std::string department_;
  std::string email_;


  DISALLOW_COPY_AND_ASSIGN(User);
};

NS_LCC_END

#endif /* defined(LESSCHATCORE_CORE_USER_USER_H_) */

