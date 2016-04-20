#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - Frank Lin

from skr_cpp_builder.cpp_variable import VarType
from skrutil.string_utils import indent
from skrutil.string_utils import to_title_style_name
from skrutil.string_utils import to_objc_property_name
from skrutil.string_utils import first_char_to_lower


_JAVA_BR = '\n\n'
_JAVA_SPACE = '    '


class JavaVariable:
    """Represents Java fields with Java type and name with three read-only properties : var_type, name_str (eg: uid),
    get_set_name_str(eg: Uid)
    """

    def __init__(self, name, var_type_string):
        """Init JavaVariable with name and type string declares in VarType.

        Args:
            name: A string descries Variable name.
            var_type_string: A string declares in VarType.
        """
        var_type = VarType.instance_from_string(var_type_string)

        self.__name_str = to_objc_property_name(name)
        self.__title_style_name = to_title_style_name(name)
        self.__var_type = var_type
        self.__java_enum = ''

    def set_enum_class_name(self, enum_class_name):
        """Sets the enum name only the variable is enum.

        Args:
            enum_class_name: A string which is enum name.
        """
        self.__var_type.set_enum_class_name(enum_class_name)
        self.__java_enum = self.__var_type.java_enum_type_string()

    def private_field_name(self):
        """Gets Android style Java field name.

        Returns:
            A string which is Java field name. For example:

            private String mTeamName;
        """
        return 'private final {0} m{1};'.format(self.__var_type.to_java_getter_setter_string_v2(),
                                                self.__title_style_name)

    def input_parameter_name(self):
        """Gets Android style Java input parameter name.

        Returns:
            A string which is Java input parameter name. For example:

            String teamName
        """
        return '{0} {1}'.format(self.__var_type.to_java_getter_setter_string_v2(),
                                first_char_to_lower(self.__title_style_name))

    def assignment(self):
        """Gets assignment implementation.

        Returns:
            A string which is assignment. For example:

            mTaskId = taskId;
        """
        return 'm{0} = {1};'.format(self.__title_style_name, first_char_to_lower(self.__title_style_name))

    def getter_v2(self, num_pre_spaces=4):
        """Getter method using Android style implementation.

        Args:
            num_pre_spaces: A int describes the count spaces in front of the string.

        Returns:
            Java getter method. For example:

            public int getPosition() {
                return mPosition;
            }
        """
        function_str = ''
        if self.__var_type == VarType.cpp_bool:
            function_str += indent(num_pre_spaces) + 'public {0} is{1}() {{\n' \
                .format(self.__var_type.to_java_getter_setter_string(), self.__title_style_name)
            function_str += indent(num_pre_spaces + 4) + 'return m{0};\n'.format(self.__title_style_name)
            function_str += indent(num_pre_spaces) + '}'
        elif self.__var_type == VarType.cpp_string_array:
            function_str += indent(num_pre_spaces) + 'public String[] get{0}() {{\n'.format(self.__title_style_name)
            function_str += indent(num_pre_spaces + 4) + 'return m{0};\n'.format(self.__title_style_name)
            function_str += indent(num_pre_spaces) + "}"
        elif self.__var_type == VarType.cpp_enum:
            function_str += indent(num_pre_spaces) + '@{0}\n'.format(self.__java_enum)
            function_str += indent(num_pre_spaces) + 'public int get{0}() {{\n'.format(self.__title_style_name)
            function_str += indent(num_pre_spaces + 4) + 'return m{0};\n'.format(self.__title_style_name)
            function_str += indent(num_pre_spaces) + '}'
        else:
            function_str += indent(num_pre_spaces) + 'public {0} get{1}() {{\n'. \
                format(self.__var_type.to_java_getter_setter_string(), self.__title_style_name)
            function_str += indent(num_pre_spaces + 4) + 'return m{0};\n'.format(self.__title_style_name)
            function_str += indent(num_pre_spaces) + '}'
        return function_str

    def getter(self):
        """Getter method using JNI.

        New development should use <getter_v2>.

        Returns:
            Java getter method using JNI. For example:

            public int getPosition() {
                return nativeGetPosition(mNativeHandler);
            }
        """
        function_str = ''
        if self.__var_type == VarType.cpp_bool:
            function_str += indent(1) + 'public {0} is{1}() {{\n'\
                .format(self.__var_type.to_java_getter_setter_string(), self.__title_style_name)
            function_str += indent(2) + 'return nativeIs{0}(mNativeHandler);\n'.format(self.__title_style_name)
            function_str += indent(1) + '}'
        elif self.__var_type == VarType.cpp_string_array:
            function_str += self.__to_get_list_of_string_implementation()
        elif self.__var_type == VarType.cpp_enum:
            function_str += indent(1) + 'public {0} get{1}() {{\n'.format(self.__java_enum, self.__title_style_name)
            function_str += indent(2) + 'return {0}.get{0}ByValue(nativeGet{1}(mNativeHandler));\n'\
                .format(self.__java_enum, self.__title_style_name)
            function_str += indent(1) + '}'
        else:
            function_str += indent(1) + 'public {0} get{1}() {{\n'.\
                format(self.__var_type.to_java_getter_setter_string(), self.__title_style_name)
            function_str += indent(2) + 'return nativeGet{0}(mNativeHandler);\n'.format(self.__title_style_name)
            function_str += indent(1) + '}'
        return function_str

    def native_getter(self):
        """Gets Java native getter.

        Returns:
            Java native getter. For example:

            private native String nativeGetTaskId(long handler);
        """
        if self.__var_type == VarType.cpp_bool:
            return indent(1) + 'private native {0} nativeIs{1}(long handler);'.format(
                self.__var_type.to_java_getter_setter_string(), self.__title_style_name)
        elif self.__var_type == VarType.cpp_string_array:
            return indent(1) + 'private native String[] nativeGet{0}(long handler);'.format(self.__title_style_name)
        elif self.__var_type == VarType.cpp_enum:
            return indent(1) + 'private native int nativeGet{0}(long handler);'.format(self.__title_style_name)
        else:
            return indent(1) + 'private native {0} nativeGet{1}(long handler);'.format(
                self.__var_type.to_java_getter_setter_string(),self.__title_style_name)

    def __to_get_list_of_string_implementation(self):
        function = indent(1) + 'public List<String> get{0}() {{\n'.format(self.__title_style_name)
        function += indent(2) + 'String[] strs = nativeGet{0}(mNativeHandler);\n'.format(self.__title_style_name)
        function += indent(2) + 'if (strs == null) {\n'
        function += indent(3) + 'return new ArrayList<String>();\n'
        function += indent(2) + '}\n'
        function += indent(2) + 'List<String> list = new ArrayList<String>(Arrays.asList(strs));\n'
        function += indent(2) + 'return list;\n'
        function += indent(1) + "}"
        return function

    @property
    def var_type(self):
        return self.__var_type

    @property
    def name_str(self):
        return self.__name_str

    @property
    def get_set_name_str(self):
        return self.__title_style_name
