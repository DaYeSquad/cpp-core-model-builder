#!/usr/bin/env python
# -*- coding: utf-8 -*-
# cpp_enum.py
#
# Copyright (c) 2016 - Frank Lin

"""
Parse and store C++ class info.
"""

_CPP_BR = '\n\n'
_CPP_SPACE = '  '


class CppEnum:
    """Describes the C++ enumeration.
    """

    def __init__(self, enum_class_name):
        self.__enum_class_name = enum_class_name
        self.__int_alias_tuple_list = []

    def append(self, int_value, alias):
        self.__int_alias_tuple_list.append((int_value, alias))

    def generate_cpp_enum(self, pre_spaces):
        """Gets C++ enum source code.

        Args:
            pre_spaces: The count of spaces in front of source code.

        Returns:
            A string which is C++ enum source code. For example:

            enum class Type {
              NONE = 1,
              ALL = 2,
            };
        """
        cpp_enum = ''
        cpp_enum += '{0}enum class {1} {{\n'.format(pre_spaces, self.__enum_class_name)
        for int_alias_tuple in self.__int_alias_tuple_list:
            cpp_enum += _CPP_SPACE + '{0}{1} = {2},\n'.format(pre_spaces,
                                                              int_alias_tuple[1],
                                                              int_alias_tuple[0])
        cpp_enum += '{0}}};\n'.format(pre_spaces)
        return cpp_enum
