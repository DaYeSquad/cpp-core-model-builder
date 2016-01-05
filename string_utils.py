import re
import string


# "UserGroup" to "userGroup"
def first_char_to_lower(string):
    if len(string) == 0:
        return string
    else:
        return string[0].lower() + string[1:]


# "userGroup" to "UserGroup"
def first_char_to_upper(string):
    if len(string) == 0:
        return string
    else:
        return string[0].upper() + string[1:]


# "UserGroup" to "user_group"
def cpp_class_name_to_cpp_file_name(class_name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', class_name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


# "userGroup" to "UserGroup"
def cpp_group_name_to_objc_group_name(cpp_group_name):
    return first_char_to_upper(cpp_group_name)


# "user_group" to "UserGroup"
def to_title_style_name(name):
    name_with_underscore = name
    step_1 = name_with_underscore.replace('_', ' ')
    step_2 = string.capwords(step_1)
    step_3 = step_2.replace(' ', '')
    return step_3


# "user_group" to "userGroup"
def to_objc_property_name(name):
    step_1 = to_title_style_name(name)
    step_2 = first_char_to_lower(step_1)
    return step_2


# "USER_GROUP" to "LCCUserGroup"
def cpp_enum_class_name_to_objc_enum_class_name(name):
    return '{0}'.format(to_title_style_name(name.lower()))


# returns spaces
def indent(num_spaces):
    num = num_spaces
    spaces = ''
    while num > 0:
        spaces += ' '
        num -= 1
    return spaces
