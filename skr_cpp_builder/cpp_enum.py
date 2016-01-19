# -*- coding: utf-8 -*-
#!/usr/bin/env python
# cpp_enum.py
#
# Copyright (c) 2016 - Frank Lin

"""
Parse and store C++ class info.
"""

_CPP_BR = '\n\n'
_CPP_SPACE = '  '


class CppEnum:

    def __init__(self, enum_class_name):
        self.enum_class_name = enum_class_name
        self.int_alias_tuple_list = []

    def append(self, int_value, alias):
        self.int_alias_tuple_list.append((int_value, alias))

    def generate_cpp_enum(self, pre_spaces):
        cpp_enum = ''
        cpp_enum += '{0}enum class {1} {{\n'.format(pre_spaces, self.enum_class_name)
        for int_alias_tuple in self.int_alias_tuple_list:
            cpp_enum += _CPP_SPACE + '{0}{1} = {2},\n'.format(pre_spaces,
                                                              int_alias_tuple[1],
                                                              int_alias_tuple[0])
        cpp_enum += '{0}}};\n'.format(pre_spaces)
        return cpp_enum
