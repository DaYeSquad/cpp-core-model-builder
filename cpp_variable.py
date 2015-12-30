from enum import Enum
from copy import copy
import string
import re
from skr_logger import skr_log_warning


class VarType(Enum):
    cpp_bool = 1
    cpp_int = 2
    cpp_string = 3
    cpp_enum = 4
    cpp_string_array = 5

    def __init__(self, value):
        self.enum_class_name = ''

    def set_enum_class_name(self, enum_class_name):
        if enum_class_name is None:
            enum_class_name = ''

        self.enum_class_name = enum_class_name

        # check input
        if self.value == 4 and enum_class_name == '':
            skr_log_warning('Enum value should declare its enum class name via "enum"')

    def to_getter_string(self):
        if self.value == 1:
            return 'bool'
        elif self.value == 2:
            return 'int'
        elif self.value == 3:
            return 'std::string'
        elif self.value == 4:
            return self.cpp_enum_type_string()
        elif self.value == 5:
            return 'std::vector<std::string>'

    def to_setter_string(self):
        if self.value == 1:
            return 'bool'
        elif self.value == 2:
            return 'int'
        elif self.value == 3:
            return 'const std::string&'
        elif self.value == 4:
            return self.cpp_enum_type_string()
        elif self.value == 5:
            return 'const std::vector<std::string>&'

    @classmethod
    def type_from_string(cls, var_type_string):
        if var_type_string == 'bool':
            return 1
        elif var_type_string == 'int':
            return 2
        elif var_type_string == 'string':
            return 3
        elif var_type_string == 'enum':
            return 4
        elif var_type_string == 'string_array':
            return 5

    def cpp_enum_type_string(self):
        if self.value != 4 and self.enum_class_name is None or self.enum_class_name == '':
            return ''

        enum_paths = re.split('\.', self.enum_class_name)
        cpp_enum = ''
        for enum_path in enum_paths:
            cpp_enum += enum_path
            cpp_enum += '::'
        cpp_enum = cpp_enum[:-2]  # remove last 2 chars
        return cpp_enum

    def to_json_value_type(self):
        if self.value == 1:
            return 'bool_value()'
        elif self.value == 2:
            return 'int_value()'
        elif self.value == 3:
            return 'string_value()'
        elif self.value == 4:
            return 'int_value()'
        elif self.value == 5:
            return ''

    def to_sqlite_value_type(self):
        if self.value == 1:
            return 'sql::type_bool'
        elif self.value == 2:
            return 'sql::type_int'
        elif self.value == 3:
            return 'sql::type_text'
        elif self.value == 4:
            return 'sql::type_int'
        elif self.value == 5:
            return 'sql::type_text'

    def to_set_sqlite_value_string(self):
        if self.value == 1:
            return 'setBool'
        elif self.value == 2:
            return 'setInteger'
        elif self.value == 3:
            return 'setString'
        elif self.value == 4:
            return 'setInteger'
        elif self.value == 5:
            return 'setString'

    def to_get_sqlite_value_string(self):
        if self.value == 1:
            return 'asBool'
        elif self.value == 2:
            return 'asInteger'
        elif self.value == 3:
            return 'asString'
        elif self.value == 4:
            return 'asInteger'
        elif self.value == 5:
            return 'asString'


class CppVariable:

    def __init__(self, name, var_type_string, json_path, sql_flag_or_none):
        var_type = VarType.type_from_string(var_type_string)

        self.name = name
        self.var_type = VarType(var_type)
        self.json_path = json_path
        self.sql_flag_or_none = sql_flag_or_none

    def set_enum_class_name(self, enum_class_name):
        self.var_type.set_enum_class_name(enum_class_name)

    def getter(self):
        if self.var_type == VarType.cpp_bool:
            return '{0} is_{1}() const {{ return {1}_; }}'.format(self.var_type.to_getter_string(), self.name)
        else:
            return '{0} {1}() const {{ return {1}_; }}'.format(self.var_type.to_getter_string(), self.name)

    def setter(self):
        return 'void set_{0}({1} {0}) {{ {0}_ = {0}; }}'.format(self.name, self.var_type.to_setter_string())

    def private_var(self):
        return '{0} {1}_;'.format(self.var_type.to_getter_string(), self.name)

    def private_var_without_type(self):
        return '{0}_'.format(self.name)

    def initializer(self):
        return '{0} {1}'.format(self.var_type.to_setter_string(), self.name)

    def initializer_implementation(self):
        return '{0}_ = {0};'.format(self.name)

    # from 'display_name' to 'DisplayName'
    def to_title_style_name(self):
        name_with_underscore = copy(self.name)
        step_1 = name_with_underscore.replace('_', ' ')
        step_2 = string.capwords(step_1)
        step_3 = step_2.replace(' ', '')
        return step_3

    # returns 'kDisplayName'
    def to_sql_key(self):
        return 'k{0}'.format(self.to_title_style_name())

    # returns 'sql::type_text'
    def to_easy_sqlite_value_type(self):
        return self.var_type.to_sqlite_value_type()

    # returns '' or 'sql::flag_not_null' or 'sql::flag_primary_key'
    def sql_flag_string(self):
        if self.sql_flag_or_none is None:
            return 'sql::flag_not_null'
        elif self.sql_flag_or_none == 'primary_key':
            return 'sql::flag_primary_key'
        else:
            return ''

    def parse_json(self):
        if self.json_path == '':
            return ''

        json_paths = re.split('/', self.json_path)
        cpp_json_paths = ''
        for json_path in json_paths:
            cpp_json_paths += '["{0}"]'.format(json_path)

        if self.var_type == VarType.cpp_enum:  # need cast
            return '{0}_ = static_cast<{3}>(json_obj{1}.{2});'.format(self.name,
                                                                      cpp_json_paths,
                                                                      self.var_type.to_json_value_type(),
                                                                      self.var_type.cpp_enum_type_string())
        elif self.var_type == VarType.cpp_string_array:  # array_items use another parse style
            parse = '{0}_.clear();\n'.format(self.name)
            parse += '  vector<json11::Json> {0}_json = json_obj[{1}].array_items();\n'.format(self.name, cpp_json_paths)
            parse += '  for (auto it = {0}_json.begin(); it != {0}_json.end(); ++it) {{\n'.format(self.name)
            parse += '    {0}_.push_back((*it).string_value());\n'.format(self.name)
            parse += '  }\n'
            return parse
        else:
            return '{0}_ = json_obj{1}.{2};'.format(self.name, cpp_json_paths, self.var_type.to_json_value_type())

    # returns 'record.setString(kUid, user.uid());'
    def to_set_sql_string(self, object_name):
        if self.var_type == VarType.cpp_enum:
            set_sql_str = 'record.{0}({1}, static_cast<int>({2}.{3}()));\n'\
                .format(self.var_type.to_set_sqlite_value_string(), self.to_sql_key(), object_name, self.name)
            return set_sql_str
        elif self.var_type == VarType.cpp_string_array:
            set_sql_str = 'record.{0}({1}, sakura::string_vector_join({2}.{3}(), ","));\n'\
                .format(self.var_type.to_set_sqlite_value_string(), self.to_sql_key(), object_name, self.name)
            return set_sql_str
        else:
            set_sql_str = 'record.{0}({1}, {2}.{3}());\n'\
                .format(self.var_type.to_set_sqlite_value_string(), self.to_sql_key(), object_name, self.name)
            return set_sql_str

    # returns 'string uid = record->getValue(kUid)->asString();'
    def to_get_sql_value_string(self):
        if self.var_type == VarType.cpp_enum:
            get_sql_str = '{0} {1} = record->getValue({2})->{3}();\n'\
                .format(self.var_type.to_getter_string(), self.name, self.to_sql_key(), self.var_type.to_get_sqlite_value_string())
            return get_sql_str
        if self.var_type == VarType.cpp_string_array:
            get_sql_str = '{0} {1} = sakura::string_split(record->getValue({2})->{3}(), ",");\n'\
                .format(self.var_type.to_getter_string(), self.name, self.to_sql_key(), self.var_type.to_get_sqlite_value_string())
            return get_sql_str
        else:
            get_sql_str = '{0} {1} = static_cast<{4}>(record->getValue({2})->{3}());\n'\
                .format(self.var_type.to_getter_string(), self.name, self.to_sql_key(),
                        self.var_type.to_get_sqlite_value_string(), self.var_type.to_setter_string())
            return get_sql_str

    # returns 'uid = uid'
    def to_where_equal_sql(self):
        if self.var_type == VarType.cpp_string:
            return '{0} + "=\'" + {1} + "\'"'.format(self.to_sql_key(), self.name)
        elif self.var_type == VarType.cpp_string_array:
            skr_log_warning('SQLite where does not support array as filter')
            return ''
        else:
            return '{0} + "=" + {1}'.format(self.to_sql_key(), self.name)

