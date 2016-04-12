from copy import copy
import string
import re

from skrutil.skr_logger import skr_log_warning
from skrutil.deprecate_util import deprecated
from skrutil import string_utils


class VarType:
    """Describes C++ type in model xml file. Supports following types:
    bool, int, std::string, enum, std::vector<std::string>, time_t, std::vector<std::unique_ptr<Object>>,
    std::unique_ptr<Object>.
    """
    cpp_bool = 1
    cpp_int = 2
    cpp_string = 3
    cpp_enum = 4
    cpp_string_array = 5
    cpp_time = 6
    cpp_object_array = 7
    cpp_object = 8

    def __init__(self, value, object_class_name=''):
        """
        VarType constructor.

        Args:
            value: An integer represents enum integer value.
            object_class_name: A string only when value is 7 or 8, it means the object in array or itself.
        """
        self.value = value
        self.enum_class_name = ''
        self.json_search_path = ''
        self.object_class_name = object_class_name

    def __eq__(self, other):
        return self.value == other

    def set_enum_class_name(self, enum_class_name):
        if enum_class_name is None:
            enum_class_name = ''

        self.enum_class_name = enum_class_name

        # check input
        if self.value == 4 and enum_class_name == '':
            skr_log_warning('Enum value should declare its enum class name via "enum"')

    def set_json_search_path_for_string_array(self, search_path):
        self.json_search_path = search_path

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
        elif self.value == 6:
            return 'time_t'
        elif self.value == 7:
            return 'std::vector<std::unique_ptr<{0}>>'.format(self.object_class_name)
        elif self.value == 8:
            return 'std::unique_ptr<{0}>'.format(self.object_class_name)
        else:
            print 'Unsupported value'

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
        elif self.value == 6:
            return 'time_t'
        elif self.value == 7:
            return 'const std::vector<std::unique_ptr<{0}>>&'.format(self.object_class_name)
        elif self.value == 8:
            return 'const {0}&'.format(self.object_class_name)
        else:
            print 'Unsupported value'

    def to_objc_getter_string(self):
        if self.value == 1:
            return 'BOOL'
        elif self.value == 2:
            return 'NSInteger'
        elif self.value == 3:
            return 'NSString *'
        elif self.value == 4:
            return self.objc_enum_type_string()
        elif self.value == 5:
            return 'NSArray<NSString *> *'
        elif self.value == 6:
            return 'NSTimeInterval'
        elif self.value == 7:
            return 'NSArray<LCC{0} *> *'.format(self.object_class_name)
        elif self.value == 8:
            return 'LCC{0} *'.format(self.object_class_name)
        else:
            print 'Unsupported value'

    def to_jni_getter_string(self):
        if self.value == 1:
            return 'jboolean'
        elif self.value == 2:
            return 'jint'
        elif self.value == 3:
            return 'jstring'
        elif self.value == 4:
            return 'jint'
        elif self.value == 5:
            return 'jobjectArray'
        elif self.value == 6:
            return 'jlong'
        else:
            print 'Unsupported value'

    def to_jni_sign_getter_string(self):
        if self.value == 1:
            return 'Z'
        elif self.value == 2:
            return 'I'
        elif self.value == 3:
            return 'Ljava/lang/String;'
        elif self.value == 4:
            return 'I'
        elif self.value == 5:
            return '[Ljava/lang/String;'
        elif self.value == 6:
            return 'J'
        else:
            print 'Unsupported value'

    def to_java_getter_setter_string(self):
        if self.value == 1:
            return 'boolean'
        elif self.value == 2:
            return 'int'
        elif self.value == 3:
            return 'String'
        elif self.value == 4:
            return self.java_enum_type_string()
        elif self.value == 5:
            return 'List<String>'
        elif self.value == 6:
            return 'long'
        elif self.value == 7:
            return 'List<{0}>'.format(self.object_class_name)
        elif self.value == 8:
            return self.object_class_name
        else:
            print 'Unsupported value'

    def to_java_getter_setter_string_v2(self):
        if self.value == 1:
            return 'boolean'
        elif self.value == 2:
            return 'int'
        elif self.value == 3:
            return 'String'
        elif self.value == 4:
            return '@{0} int'.format(self.enum_class_name)
        elif self.value == 5:
            return 'String[]'
        elif self.value == 6:
            return 'long'
        elif self.value == 7:
            return '{0}[]'.format(self.object_class_name)
        elif self.value == 8:
            return self.object_class_name
        else:
            print 'Unsupported value'

    @classmethod
    @deprecated  # use instance_from_string to adapt to new development
    def type_from_string(cls, var_type_string):
        if var_type_string == 'bool':
            return 1
        elif var_type_string == 'int':
            return 2
        elif var_type_string == 'string':
            return 3
        elif var_type_string == 'enum':
            return 4
        elif var_type_string == '[string]':
            return 5
        elif var_type_string == 'time':
            return 6
        else:
            print 'Unsupported value'

    @classmethod
    def instance_from_string(cls, var_type_string):
        if var_type_string == 'bool':
            return VarType(1)
        elif var_type_string == 'int':
            return VarType(2)
        elif var_type_string == 'string':
            return VarType(3)
        elif var_type_string == 'enum':
            return VarType(4)
        elif var_type_string == '[string]':
            return VarType(5)
        elif var_type_string == 'time':
            return VarType(6)
        elif var_type_string[0] == '[':
            if var_type_string[1] == '{':  # object array
                class_name = var_type_string[2:-2]
                print 'class name is {0}'.format(class_name)
                return VarType(7, class_name)
            else:
                print 'Unsupported array'
                assert False
        elif var_type_string[0] == '{':  # object
            class_name = var_type_string[1:-1]
            print 'class name is {0}'.format(class_name)
            return VarType(8, class_name)
        else:
            print 'Unsupported value'

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

    def objc_enum_type_string(self):
        if self.value != 4 and self.enum_class_name is None or self.enum_class_name == '':
            return ''

        enum_paths = re.split('\.', self.enum_class_name)
        objc_enum = 'LCC'
        for enum_path in enum_paths:
            objc_enum += enum_path
        return objc_enum

    def java_enum_type_string(self):
        if self.value != 4 and self.enum_class_name is None or self.enum_class_name == '':
            return ''
        enum_paths = re.split('\.', self.enum_class_name)
        java_enum = enum_paths[len(enum_paths) - 1]
        return java_enum

    def cpp_json11_array_it_search_string(self):
        paths = re.split('\.', self.json_search_path)
        cpp_str = ''
        for path in paths:
            cpp_str += '["{0}"]'.format(path)
        return cpp_str

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
            return 'array_items()'
        elif self.value == 6:
            return 'int_value()'
        else:
            print 'Unsupported value'

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
        elif self.value == 6:
            return 'sql::type_int'
        else:
            print 'Unsupported value'

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
        elif self.value == 6:
            return 'setInteger'
        else:
            print 'Unsupported value'

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
        elif self.value == 6:
            return 'asInteger'
        else:
            print 'Unsupported value'

    def to_null_value(self):
        if self.value == 1:
            return 'false'
        elif self.value == 2:
            return '0'
        elif self.value == 3:
            return '""'
        elif self.value == 4:
            return '0'
        elif self.value == 5:
            return '{}'
        elif self.value == 6:
            return '0'
        elif self.value == 7:
            return '{}'
        elif self.value == 8:
            return 'nullptr'
        else:
            print 'Unsupported value'


class CppVariable:

    def __init__(self, name, var_type_string, json_path, sql_flag_or_none, cache_desc='', capture=False, is_read_only=False):
        self.name = name
        self.var_type = VarType.instance_from_string(var_type_string)
        self.json_path = json_path
        self.sql_flag_or_none = sql_flag_or_none
        self.cache_desc = cache_desc
        self.capture = capture
        self.is_read_only = is_read_only

        self.override_sql_key = None

    def set_enum_class_name(self, enum_class_name):
        self.var_type.set_enum_class_name(enum_class_name)

    def set_json_search_path(self, json_search_path):
        if json_search_path is None:
            json_search_path = ''
        self.var_type.set_json_search_path_for_string_array(json_search_path)

    def set_override_sql_key(self, key):
        self.override_sql_key = key

    def getter(self):
        if self.var_type == VarType.cpp_bool:
            return '{0} is_{1}() const {{ return {1}_; }}'.format(self.var_type.to_getter_string(), self.name)
        else:
            return '{0} {1}() const {{ return {1}_; }}'.format(self.var_type.to_getter_string(), self.name)

    def setter(self):
        # ignores getter if read-only
        if self.is_read_only:
            return ''

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

    def parse_json(self, indent=0):
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
            parse += '  vector<json11::Json> {0}_json = json_obj{1}.array_items();\n'.format(self.name, cpp_json_paths)
            parse += '  for (auto it = {0}_json.begin(); it != {0}_json.end(); ++it) {{\n'.format(self.name)
            parse += '    {0}_.push_back((*it){1}.string_value());\n'.format(self.name, self.var_type.cpp_json11_array_it_search_string())
            parse += '  }\n'
            return parse
        elif self.var_type == VarType.cpp_bool:  # bool value should compact with int_value == 1
            parse = 'json11::Json {0}_json = json_obj{1};\n'.format(self.name, cpp_json_paths)
            parse += '  if ({0}_json.type() == json11::Json::Type::BOOL) {{\n'.format(self.name)
            parse += '    {0}_ = {0}_json.bool_value();\n'.format(self.name)
            parse += '  } else {\n'
            parse += '    {0}_ = ({0}_json.int_value() == 1);\n'.format(self.name)
            parse += '  }\n'
            return parse
        elif self.var_type == VarType.cpp_object:  # C++ object
            parse = string_utils.indent(indent) + 'unique_ptr<{0}> {1}(new {0}());\n'.format(self.var_type.object_class_name, self.name)
            parse += string_utils.indent(indent) + '{0}->InitWithJsonOrDie(json_obj{1}.dump());\n'.format(self.name, cpp_json_paths)
            return parse
        elif self.var_type == VarType.cpp_object_array:  # C++ objects
            parse = string_utils.indent(indent) + 'vector<unique_ptr<{0}>> {1};\n'.format(self.var_type.object_class_name, self.name)
            parse += string_utils.indent(indent) + 'vector<json11::Json> {0}_jsons = json_obj{1}.array_items();\n'.format(self.name, cpp_json_paths)
            parse += string_utils.indent(indent) + 'for (auto json : {0}_jsons) {{\n'.format(self.name)
            parse += string_utils.indent(indent + 2) + 'unique_ptr<{0}> obj(new {0}());\n'.format(self.var_type.object_class_name)
            parse += string_utils.indent(indent + 2) + 'obj->InitWithJsonOrDie(json.dump());\n'
            parse += string_utils.indent(indent + 2) + '{0}.push_back(std::move(obj));\n'.format(self.name)
            parse += string_utils.indent(indent) + '}\n'
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
        elif self.var_type == VarType.cpp_bool:
            set_sql_str = 'record.{0}({1}, {2}.is_{3}());\n'\
                .format(self.var_type.to_set_sqlite_value_string(), self.to_sql_key(), object_name, self.name)
            return set_sql_str
        else:
            set_sql_str = 'record.{0}({1}, {2}.{3}());\n'\
                .format(self.var_type.to_set_sqlite_value_string(), self.to_sql_key(), object_name, self.name)
            return set_sql_str

    # returns 'string uid = record->getValue(kUid)->asString();'
    def to_get_sql_value_string(self):
        if self.var_type == VarType.cpp_enum:
            get_sql_str = '{0} {1} = static_cast<{4}>(record->getValue({2})->{3}());\n'\
                .format(self.var_type.to_getter_string(), self.name, self.to_sql_key(),
                        self.var_type.to_get_sqlite_value_string(), self.var_type.to_setter_string())
            return get_sql_str
        elif self.var_type == VarType.cpp_string_array:
            get_sql_str = '{0} {1} = sakura::string_split(record->getValue({2})->{3}(), ",");\n'\
                .format(self.var_type.to_getter_string(), self.name, self.to_sql_key(), self.var_type.to_get_sqlite_value_string())
            return get_sql_str
        elif self.var_type == VarType.cpp_int or self.var_type == VarType.cpp_time:
            get_sql_str = '{0} {1} = static_cast<{0}>(record->getValue({2})->{3}());\n'\
                .format(self.var_type.to_getter_string(), self.name, self.to_sql_key(), self.var_type.to_get_sqlite_value_string())
            return get_sql_str
        else:
            get_sql_str = '{0} {1} = record->getValue({2})->{3}();\n'\
                .format(self.var_type.to_getter_string(), self.name, self.to_sql_key(), self.var_type.to_get_sqlite_value_string())
            return get_sql_str

    # returns 'uid = uid'
    def to_where_equal_sql(self):
        if self.var_type == VarType.cpp_string:
            return '{0} + "=\'" + {1} + "\'"'.format(self.to_sql_key(), self.name)
        elif self.var_type == VarType.cpp_string_array:
            skr_log_warning('SQLite where does not support array as filter')
            return ''
        elif self.var_type == VarType.cpp_enum:
            return '{0} + "=" + std::to_string(static_cast<int>({1}))'.format(self.to_sql_key(), self.name)
        else:
            return '{0} + "=" + std::to_string({1})'.format(self.to_sql_key(), self.name)

    # returns 'bool success'
    def to_get_description_string(self):
        return '{0} {1}'.format(self.var_type.to_setter_string(), self.name)

    # returns 'std::unique_ptr<Tasks> tasks'
    def to_set_description_string(self):
        return '{0} {1}'.format(self.var_type.to_getter_string(), self.name)

    # returns 'std::to_string(int_var)' or 'project_id' or 'std::to_string(static_cast<int>(enum))'
    def to_convert_to_string_description(self):
        if self.var_type == VarType.cpp_string:
            return self.name
        elif self.var_type == VarType.cpp_bool or self.var_type == VarType.cpp_int or self.var_type == VarType.cpp_time:
            return 'std::to_string({0})'.format(self.name)
        elif self.var_type == VarType.cpp_enum:
            return 'std::to_string(static_cast<int>({0}))'.format(self.name)
        else:
            print 'Unsupported to_string type'
            assert False

    # returns original string or 'std::move(tasks)'
    def to_move_string(self):
        if self.var_type == VarType.cpp_object or self.var_type == VarType.cpp_object_array:
            return 'std::move({0})'.format(self.name)
        else:
            return self.name

    # returns 'nullptr' or '{}' or '""' or '0' or 'false'
    def to_null_string(self):
        return self.var_type.to_null_value()

    # returns 'static_cast<int>(i)'
    def to_json11_type(self):
        if self.var_type == VarType.cpp_int or self.var_type == VarType.cpp_string:
            return self.name
        elif self.var_type == VarType.cpp_bool:
            return '{0} ? 1 : 0'.format(self.name)
        elif self.var_type == VarType.cpp_enum or self.var_type == VarType.cpp_time:
            return 'static_cast<int>({0})'.format(self.name)
        elif self.var_type == VarType.cpp_string_array:
            return 'json11_array_from_strings({0})'.format(self.name)
        else:
            print 'Unsupported types'
            assert False

