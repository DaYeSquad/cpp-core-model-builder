from enum import Enum
import re
from skrutil.skr_logger import skr_log_warning
from skr_cpp_builder.cpp_variable import VarType


_JAVA_BR = '\n\n'
_JAVA_SPACE = '    '


def function_space(count):
    space = ''
    for i in range(1, count + 1):
        space += _JAVA_SPACE
    return space


# class VarType(Enum):
#     java_bool = 1
#     java_int = 2
#     java_string = 3
#     java_enum = 4
#     java_string_array = 5
#     java_time = 6
#
#     def __init__(self, value):
#         self.enum_class_name = ''
#
#     def set_enum_class_name(self, enum_class_name):
#         if enum_class_name is None:
#             enum_class_name = ''
#
#         self.enum_class_name = enum_class_name
#
#         # check input
#         if self.value == 4 and enum_class_name == '':
#             skr_log_warning('Enum value should declare its enum class name via "enum"')
#
#     def to_getter_setter_string(self):
#         if self.value == 1:
#             return 'boolean'
#         elif self.value == 2:
#             return 'int'
#         elif self.value == 3:
#             return 'String'
#         elif self.value == 4:
#             return self.java_enum_type_string()
#         elif self.value == 5:
#             return 'List<String>'
#         elif self.value == 6:
#             return 'long'
#
#     @classmethod
#     def type_from_string(cls, var_type_string):
#         if var_type_string == 'bool':
#             return 1
#         elif var_type_string == 'int':
#             return 2
#         elif var_type_string == 'string':
#             return 3
#         elif var_type_string == 'enum':
#             return 4
#         elif var_type_string == '[string]':
#             return 5
#         elif var_type_string == 'time':
#             return 6
#
#     def java_enum_type_string(self):
#         if self.value != 4 and self.enum_class_name is None or self.enum_class_name == '':
#             return ''
#         enum_paths = re.split('\.', self.enum_class_name)
#         java_enum = enum_paths[len(enum_paths) - 1]
#         return java_enum


class JavaVariable:
    def __init__(self, name, var_type_string):
        var_type = VarType.instance_from_string(var_type_string)

        var_name_str = ''
        get_set_name = ''
        name_splits = re.split('_', name)
        index = 1
        for name_split in name_splits:
            if index == 1:
                var_name_str += name_split
            else:
                var_name_str += name_split.capitalize()
            get_set_name += name_split.capitalize()
            index += 1

        self.name_str = var_name_str
        self.get_set_name_str = get_set_name
        self.var_type = VarType(var_type)
        self.java_enum = ''

    def set_enum_class_name(self, enum_class_name):
        self.var_type.set_enum_class_name(enum_class_name)
        self.java_enum = self.var_type.java_enum_type_string()

    def getter(self):
        function_str = ''
        if self.var_type == VarType.cpp_bool:
            function_str += function_space(1) + 'public {0} is{1}() {{\n'\
                .format(self.var_type.to_java_getter_setter_string(), self.get_set_name_str)
            function_str += function_space(2) + 'return nativeIs{0}(mNativeHandler);\n'.format(self.get_set_name_str)
            function_str += function_space(1) + '}'
        elif self.var_type == VarType.cpp_string_array:
            function_str += self.to_get_string_array_string()
        elif self.var_type == VarType.cpp_enum:
            function_str += function_space(1) + 'public {0} get{1}() {{\n'.format(self.java_enum, self.get_set_name_str)
            function_str += function_space(2) + 'return {0}.get{0}ByValue(nativeGet{1}(mNativeHandler));\n'\
                .format(self.java_enum, self.get_set_name_str)
            function_str += function_space(1) + '}'
        else:
            function_str += function_space(1) + 'public {0} get{1}() {{\n'.\
                format(self.var_type.to_java_getter_setter_string(), self.get_set_name_str)
            function_str += function_space(2) + 'return nativeGet{0}(mNativeHandler);\n'.format(self.get_set_name_str)
            function_str += function_space(1) + '}'
        return function_str

    def setter(self):
        if self.var_type == VarType.cpp_string_array:
            return self.to_set_string_array_string()
        elif self.var_type == VarType.cpp_enum:
            return function_space(1) + 'public void set{0}({2} {1}) {{ nativeSet{0}(mNativeHandler, {1}.getValue()); }}'.format(self.get_set_name_str,
                                                                                                                               self.name_str,
                                                                                                                               self.java_enum)
        else:
            return function_space(1) + 'public void set{0}({2} {1}) {{ nativeSet{0}(mNativeHandler, {1}); }}'.format(self.get_set_name_str,
                                                                                                                     self.name_str,
                                                                                                                     self.var_type.to_getter_setter_string())

    def native_getter(self):
        if self.var_type == VarType.cpp_bool:
            return function_space(1) + 'private native {0} nativeIs{1}(long handler);'.format(self.var_type.to_java_getter_setter_string(), self.get_set_name_str)
        elif self.var_type == VarType.cpp_string_array:
            return function_space(1) + 'private native String[] nativeGet{0}(long handler);'.format(self.get_set_name_str)
        elif self.var_type == VarType.cpp_enum:
            return function_space(1) + 'private native int nativeGet{0}(long handler);'.format(self.get_set_name_str)
        else:
            return function_space(1) + 'private native {0} nativeGet{1}(long handler);'.format(self.var_type.to_java_getter_setter_string(),
                                                                                               self.get_set_name_str)

    def native_setter(self):
        if self.var_type == VarType.cpp_string_array:
            return function_space(1) + 'private native void nativeSet{0}(long handler, String[] {1});'.format(self.get_set_name_str,
                                                                                                             self.name_str)
        elif self.var_type == VarType.cpp_enum:
            return function_space(1) + 'private native void nativeSet{0}(long handler, {1} {2});'.format(self.get_set_name_str,
                                                                                                        'int',
                                                                                                        self.name_str)
        else:
            return function_space(1) + 'private native void nativeSet{0}(long handler, {1} {2});'.format(self.get_set_name_str,
                                                                                                        self.var_type.to_getter_setter_string(),
                                                                                                        self.name_str)

    def to_get_string_array_string(self):
        function = function_space(1) + 'public List<String> get{0}() {{\n'.format(self.get_set_name_str)
        function += function_space(2) + 'String[] strs = nativeGet{0}(mNativeHandler);\n'.format(self.get_set_name_str)
        function += function_space(2) + 'if (strs == null) {\n'
        function += function_space(3) + 'return new ArrayList<String>();\n'
        function += function_space(2) + '}\n'
        function += function_space(2) + 'List<String> list = new ArrayList<String>(Arrays.asList(strs));\n'
        function += function_space(2) + 'return list;\n'
        function += function_space(1) + "}"
        return function

    def to_set_string_array_string(self):
        function = function_space(1) + 'public void set{0}(List<String> strs) {{\n'.format(self.get_set_name_str)
        function += function_space(2) + 'String[] {0} = new String[strs.size()];\n'.format(self.name_str)
        function += function_space(2) + 'strs.toArray({0});\n'.format(self.name_str)
        function += function_space(2) + 'nativeSet{0}(mNativeHandler, {1});\n'.format(self.get_set_name_str, self.name_str)
        function += function_space(1) + '}\n'
        return function
