#!/usr/bin/env python

import re
import string

"""String Utils.
"""


def first_char_to_lower(string):
    """Converts first letter to lower case.

    Args:
        string: A string.

    Returns:
        A string whose first letter is lower case. For example:

        "UserGroup" to "userGroup"
    """
    if len(string) == 0:
        return string
    else:
        return string[0].lower() + string[1:]


def first_char_to_upper(string):
    """Converts first letter to upper case

    Args:
        string: A string.

    Returns:
        A string whose first letter to upper case. For example:

        "userGroup" to "UserGroup"
    """
    if len(string) == 0:
        return string
    else:
        return string[0].upper() + string[1:]


def cpp_class_name_to_cpp_file_name(class_name):
    """Converts C++ class name to file name.

    Args:
        class_name: A string which is C++ class name.

    Returns:
        A string which is C++ file name. For example:

        "UserGroup" to "user_group"
    """
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', class_name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def cpp_group_name_to_objc_group_name(cpp_group_name):
    """Wrapper of <first_char_to_upper>.

    Args:
        cpp_group_name: A string of C++ group name.

    Returns:
        A string which is Objective-C group name. For example:

        "userGroup" to "UserGroup"
    """
    return first_char_to_upper(cpp_group_name)


def to_title_style_name(name):
    """Converts from "user_group" to "UserGroup".

    Args:
        name: A string which is liked "user_group".

    Returns:
        A string which is liked UserGroup". For example:

        "user_group" to "UserGroup"
    """
    name_with_underscore = name
    step_1 = name_with_underscore.replace('_', ' ')
    step_2 = string.capwords(step_1)
    step_3 = step_2.replace(' ', '')
    return step_3


def to_objc_property_name(name):
    """ "user_group" to "userGroup"

    Args:
        name: A string which is liked "user_group".

    Returns:
        "user_group" to "userGroup"
    """
    step_1 = to_title_style_name(name)
    step_2 = first_char_to_lower(step_1)
    return step_2


def cpp_enum_class_name_to_objc_enum_class_name(name):
    """ "USER_GROUP" to "LCCUserGroup"

    Args:
        name: A string which is C++ enum name.

    Returns:
        A string which is Objective-C style name that may has LCC prefix.
    """
    return '{0}'.format(to_title_style_name(name.lower()))


def indent(num_spaces):
    """Gets spaces.

    Args:
        num_spaces: An int describes number of spaces.

    Returns:
        A string contains num_spaces spaces.
    """
    num = num_spaces
    spaces = ''
    while num > 0:
        spaces += ' '
        num -= 1
    return spaces


def strings_or_none_in_brackets(string):
    """Returns a string found in brackets or none if not found.

    Args:
        string: An input string.

    Returns:
        A string found in brackets or none if not found. For example:

        input : hello [{window}],
        output : {window}
    """
    result_or_none = re.findall(r"\[([A-Za-z0-9_]+)\]", string)
    if result_or_none is not None:
        return result_or_none
    else:
        return None
