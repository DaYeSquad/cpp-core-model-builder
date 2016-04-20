#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - Frank Lin


from skrutil import io_utils
from skrutil.string_utils import cpp_class_name_to_cpp_file_name


_CPP_BR = '\n\n'
_CPP_SPACE = '  '
_CPP_LIFECYCLE_SPLIT = '// Creation and lifetime --------------------------------------------------------'
_CPP_CODING_INTERFACE_SPLIT = '// Coding interface --------------------------------------------------------'
_CPP_INIT_WITH_JSON_DECLARATION = 'virtual bool InitWithJsonOrDie(const std::string& json) OVERRIDE;'
_CPP_PUBLIC = 'public:'
_CPP_PRIVATE = 'private:'
_CPP_PERSISTENT_STORE_SPLIT = '// Persisent store --------------------------------------------------------'
_CPP_UTILS_SPLIT = '// Utils --------------------------------------------------------'
_CPP_HTTP_SPLIT = '// HTTP --------------------------------------------------------'


class CppClass:
    """The main C++ parser and generator, contains all information to generating C++ source code.
    """
    def __init__(self, group_name, class_name, cpp_variable_list, cpp_enum_list, cpp_manager_or_none,
                 cpp_replacement_list, class_comment):
        """Init Cpp Class.

        Args:
            group_name: A string which is C++ folder name, should be all lower case with underscore. (eg: task_manager)
            class_name: A string which is C++ class name, should be capitalized. (eg: Task)
            cpp_variable_list: A list contains <CppVariable>, declares all fields in C++.
            cpp_enum_list: A list contains <CppEnum>, declares all enum types in this C++ class.
            cpp_manager_or_none: A <CppManager> object if user wants to generate manager code or none while not.
            cpp_replacement_list: A list of <CppReplacement>, useful when you want to use some code that not supported.
            class_comment: A string that is class comment, not supported yet.
        """
        self.__group_name = group_name
        self.__class_name = class_name
        self.__cpp_var_list = cpp_variable_list
        self.__cpp_enum_list = cpp_enum_list
        self.__cpp_manager_or_none = cpp_manager_or_none
        self.__cpp_replacement_list = cpp_replacement_list
        self.__class_comment = class_comment

        if self.__cpp_manager_or_none is not None:
            self.__cpp_manager_or_none.set_object_name(class_name, class_name + 's')
            self.__cpp_manager_or_none.set_cpp_variable_list(cpp_variable_list)
            self.__cpp_manager_or_none.set_replacement_list(cpp_replacement_list)

        self.__config = None

    def set_config(self, config):
        """Sets config for generating source code. We use this feature since 6.0 to generate worktilecore & lesschatcore.

        Args:
            config: A <Config> object describes C++ configuration.
        """
        self.__config = config

    def generate_header(self):
        """Generates C++ Object header file.
        """
        file_path = io_utils.cpp_object_header_path(self.__group_name, self.__class_name)
        output_header = open(file_path, 'w')

        def_guard = '#ifndef {2}_{0}_{1}_H_\n#define {2}_{0}_{1}_H_'.format(
                self.__group_name.upper().replace('/', '_'),
                cpp_class_name_to_cpp_file_name(self.__class_name).upper(),
                self.__config.cpp_module_name)
        end_def_guard = '#endif /* defined({2}_{0}_{1}_H_) */'.format(
                self.__group_name.upper().replace('/', '_'),
                cpp_class_name_to_cpp_file_name(self.__class_name).upper(),
                self.__config.cpp_module_name)
        cpp_include = '#include <string>\n#include <memory>\n#include <vector>\n\n#include "base/base.h"'
        cpp_class_begin = 'class LCC_DLL {0} : public CodingInterface {{'.format(self.__class_name)
        cpp_class_end = '};'
        cpp_constructor = '{0}();'.format(self.__class_name)
        cpp_deconstructor = 'virtual ~{0}();'.format(self.__class_name)
        cpp_init_method = self.__generate_init_method_declarasion()
        cpp_clone = 'std::unique_ptr<{0}> Clone() const;'.format(self.__class_name)
        cpp_getter_setter_split = '// Getter/Setter --------------------------------------------------------'
        cpp_variable_split = '// Variable --------------------------------------------------------'
        cpp_disallow_copy_and_assign = 'DISALLOW_COPY_AND_ASSIGN({0});'.format(self.__class_name)

        output_header.write(def_guard + _CPP_BR)
        output_header.write(cpp_include + _CPP_BR)
        output_header.write(self.__config.cpp_ns_begin + _CPP_BR)

        if self.__class_comment is not None:
            comment = self.__find_replacement_by_define_name(self.__class_comment)
            output_header.write('{0}'.format(comment))

        output_header.write(cpp_class_begin + '\n')
        output_header.write(_CPP_PUBLIC + _CPP_BR)

        for cpp_enum in self.__cpp_enum_list:
            output_header.write(cpp_enum.generate_cpp_enum(_CPP_SPACE) + '\n')

        output_header.write(_CPP_SPACE + _CPP_LIFECYCLE_SPLIT + _CPP_BR)
        output_header.write(_CPP_SPACE + cpp_constructor + _CPP_BR)
        output_header.write(_CPP_SPACE + cpp_deconstructor + _CPP_BR)
        output_header.write(_CPP_SPACE + cpp_init_method + _CPP_BR)
        output_header.write(_CPP_SPACE + cpp_clone + _CPP_BR)

        output_header.write(_CPP_SPACE + _CPP_CODING_INTERFACE_SPLIT + _CPP_BR)
        output_header.write(_CPP_SPACE + _CPP_INIT_WITH_JSON_DECLARATION + _CPP_BR)

        output_header.write(_CPP_SPACE + cpp_getter_setter_split + _CPP_BR)

        for cpp_var in self.__cpp_var_list:
            output_header.write(_CPP_SPACE + cpp_var.getter() + '\n')
            output_header.write(_CPP_SPACE + cpp_var.setter() + _CPP_BR)

        output_header.write(_CPP_PRIVATE + _CPP_BR)
        output_header.write(_CPP_SPACE + cpp_variable_split + _CPP_BR)

        for cpp_var in self.__cpp_var_list:
            output_header.write(_CPP_SPACE + cpp_var.private_var() + '\n')
        output_header.write(_CPP_BR)

        output_header.write(_CPP_SPACE + cpp_disallow_copy_and_assign + '\n')
        output_header.write(cpp_class_end + _CPP_BR)
        output_header.write(self.__config.cpp_ns_end + _CPP_BR)
        output_header.write(end_def_guard + _CPP_BR)

    def generate_implementation(self):
        """Generates C++ Object implementation.
        """
        file_path = io_utils.cpp_object_implementation_path(self.__group_name, self.__class_name)
        output_cc = open(file_path, 'w')

        cpp_include = '#include "{0}.h"\n\n#include "json11/json11.hpp"'.format(self.__header_file_name())
        cpp_using = 'using std::string;\nusing std::unique_ptr;\nusing std::vector;'
        cpp_public_mark = '////////////////////////////////////////////////////////////////////////////////\n// ' \
                          '{0}, public:'.format(self.__class_name)

        output_cc.write(cpp_include + _CPP_BR)
        output_cc.write(cpp_using + _CPP_BR)
        output_cc.write(self.__config.cpp_ns_begin + _CPP_BR)
        output_cc.write(cpp_public_mark + _CPP_BR)

        output_cc.write(_CPP_LIFECYCLE_SPLIT + _CPP_BR)
        output_cc.write(self.__constructor_implementation() + _CPP_BR)
        output_cc.write(self.__deconstructor_implementation() + _CPP_BR)
        output_cc.write(self.__init_method_implementation() + _CPP_BR)
        output_cc.write(self.__clone_implementation() + _CPP_BR)

        output_cc.write(_CPP_CODING_INTERFACE_SPLIT + _CPP_BR)
        output_cc.write(self.__init_with_json_implementation() + _CPP_BR)

        output_cc.write(self.__config.cpp_ns_end + _CPP_BR)

    def generate_manager_header(self):
        """Generates C++ Object Manager header.
        """
        if self.__cpp_manager_or_none is None:
            return

        cpp_manager = self.__cpp_manager_or_none
        file_path = io_utils.cpp_object_header_path(self.__group_name, cpp_manager.class_name())
        output_header = open(file_path, 'w')

        def_guard = '#ifndef {2}_{0}_{1}_H_\n#define {2}_{0}_{1}_H_'.format(
                self.__group_name.upper().replace('/', '_'),
                cpp_class_name_to_cpp_file_name(cpp_manager.class_name()).upper(),
                self.__config.cpp_module_name)
        end_def_guard = '#endif /* defined({2}_{0}_{1}_H_) */'.format(
                self.__group_name.upper().replace('/', '_'),
                cpp_class_name_to_cpp_file_name(cpp_manager.class_name()).upper(),
                self.__config.cpp_module_name)
        cpp_include = '#include <string>\n' \
                      '#include <memory>\n' \
                      '#include <vector>\n' \
                      '#include <functional>\n\n' \
                      '#include "easySQLite/easySQLite.h"\n\n' \
                      '#include "base/base.h"\n#include "director/object_manager.h"\n#include "api/web_api.h"\n\n'
        cpp_include += '#include "{0}/{1}.h"'.format(self.__group_name.replace('core/', ''),
                                                     cpp_class_name_to_cpp_file_name(self.__class_name))
        cpp_class_begin = 'class LCC_DLL {0} : public ObjectManager {{'.format(cpp_manager.class_name())
        cpp_class_end = '};'
        cpp_constructor = 'explicit {0}(Director* director);'.format(cpp_manager.class_name())
        cpp_deconstructor = 'virtual ~{0}();'.format(cpp_manager.class_name())
        cpp_init_method = 'bool InitOrDie();'
        cpp_default_manager = 'static const {0}* DefaultManager();'.format(cpp_manager.class_name())
        cpp_manager_save_methods = cpp_manager.generate_save_declarations(_CPP_SPACE)
        cpp_manager_fetch_methods = cpp_manager.generate_fetch_declarations(_CPP_SPACE)
        cpp_manager_delete_methods = cpp_manager.generate_delete_declarations(_CPP_SPACE)
        cpp_disallow_copy_and_assign = 'DISALLOW_COPY_AND_ASSIGN({0});'.format(cpp_manager.class_name())
        cpp_manager_http_methods = cpp_manager.generate_manager_http_declarations(_CPP_SPACE)

        output_header.write(def_guard + _CPP_BR)
        output_header.write(cpp_include + _CPP_BR)
        output_header.write(self.__config.cpp_ns_begin + _CPP_BR)
        output_header.write(cpp_class_begin + '\n')
        output_header.write(_CPP_PUBLIC + _CPP_BR)

        output_header.write(_CPP_SPACE + _CPP_LIFECYCLE_SPLIT + _CPP_BR)
        output_header.write(_CPP_SPACE + cpp_constructor + _CPP_BR)
        output_header.write(_CPP_SPACE + cpp_deconstructor + _CPP_BR)
        output_header.write(_CPP_SPACE + cpp_init_method + _CPP_BR)
        output_header.write(_CPP_SPACE + cpp_default_manager + _CPP_BR)

        output_header.write(_CPP_SPACE + _CPP_HTTP_SPLIT + _CPP_BR)
        output_header.write(cpp_manager_http_methods)

        output_header.write(_CPP_SPACE + _CPP_PERSISTENT_STORE_SPLIT + _CPP_BR)
        output_header.write(cpp_manager_save_methods)
        output_header.write(cpp_manager_fetch_methods)
        output_header.write(cpp_manager_delete_methods)

        output_header.write(_CPP_PRIVATE + '\n')
        output_header.write(_CPP_SPACE + cpp_manager.sqlite_table_var() + _CPP_BR)
        for table_name in cpp_manager.table_name_list:
            output_header.write(_CPP_SPACE + cpp_manager.sqlite_table_var(table_name) + _CPP_BR)

        output_header.write(_CPP_SPACE + _CPP_UTILS_SPLIT + _CPP_BR)
        output_header.write(_CPP_SPACE + cpp_manager.sqlite_record_by_object_declaration() + _CPP_BR)
        for table_name in cpp_manager.table_name_list:
            output_header.write(_CPP_SPACE + cpp_manager.sqlite_record_by_object_declaration(table_name) + _CPP_BR)

        output_header.write(cpp_manager.unsafe_save_declaration(_CPP_SPACE))
        for table_name in cpp_manager.table_name_list:
            output_header.write(cpp_manager.unsafe_save_declaration(_CPP_SPACE, table_name))

        output_header.write(_CPP_SPACE + cpp_manager.sqlite_object_from_record_declaration() + _CPP_BR)

        output_header.write('\n' + _CPP_SPACE + cpp_disallow_copy_and_assign + '\n')

        output_header.write(cpp_class_end + _CPP_BR)
        output_header.write(self.__config.cpp_ns_end + _CPP_BR)
        output_header.write(end_def_guard + _CPP_BR)

    def generate_manager_implementation(self):
        """Generates C++ Object Manager implementation.
        """
        if self.__cpp_manager_or_none is None:
            return

        cpp_manager = self.__cpp_manager_or_none

        header_file_name = cpp_class_name_to_cpp_file_name(self.__class_name) + '_manager.h'
        file_path = io_utils.cpp_object_implementation_path(self.__group_name, cpp_manager.class_name())
        output_cc = open(file_path, 'w')

        cpp_include = '#include "{0}"\n'.format(header_file_name)
        cpp_include += '#include "director/director.h"'
        cpp_using = 'using std::string;\nusing std::unique_ptr;\nusing std::vector;\n\nusing sakura::FileUtils;\n'
        cpp_public_mark = '////////////////////////////////////////////////////////////////////////////////\n// ' \
                          '{0}, public:'.format(cpp_manager.class_name())
        cpp_private_mark = '////////////////////////////////////////////////////////////////////////////////\n// ' \
                           '{0}, private:'.format(cpp_manager.class_name())
        cpp_sqlite_schema_split = '// SQLite schema --------------------------------------------------------\n'

        output_cc.write(cpp_include + _CPP_BR)
        output_cc.write(cpp_using + _CPP_BR)
        output_cc.write(self.__config.cpp_ns_begin + _CPP_BR)

        output_cc.write(cpp_sqlite_schema_split + '\n')
        output_cc.write(cpp_manager.sqlite_key_declaration() + '\n')
        output_cc.write(cpp_manager.easy_sqlite_field_declaration() + _CPP_BR)

        output_cc.write(cpp_public_mark + _CPP_BR)

        output_cc.write(_CPP_LIFECYCLE_SPLIT + _CPP_BR)
        output_cc.write(cpp_manager.generate_constructor_implementation() + _CPP_BR)
        output_cc.write(cpp_manager.generate_deconstructor_implementation() + _CPP_BR)
        output_cc.write(cpp_manager.generate_init_or_die_implementation() + _CPP_BR)
        output_cc.write(cpp_manager.generate_default_manager_implementation() + _CPP_BR)

        output_cc.write(_CPP_HTTP_SPLIT + _CPP_BR)
        output_cc.write(cpp_manager.generate_manager_http_implementation())

        output_cc.write(_CPP_PERSISTENT_STORE_SPLIT + _CPP_BR)
        output_cc.write(cpp_manager.generate_save_implementations())
        output_cc.write(cpp_manager.generate_fetch_implementations())
        output_cc.write(cpp_manager.generate_delete_implementations())

        output_cc.write(cpp_private_mark + _CPP_BR)

        output_cc.write(_CPP_UTILS_SPLIT + _CPP_BR)
        output_cc.write(cpp_manager.unsafe_save_implementation() + _CPP_BR)
        for table_name in cpp_manager.table_name_list:
            output_cc.write(cpp_manager.unsafe_save_implementation(table_name) + _CPP_BR)

        output_cc.write(cpp_manager.sqlite_record_by_object_implementation() + _CPP_BR)
        for table_name in cpp_manager.table_name_list:
            output_cc.write(cpp_manager.sqlite_record_by_object_implementation(table_name) + _CPP_BR)

        output_cc.write(cpp_manager.sqlite_object_from_record_implementation() + _CPP_BR)

        output_cc.write(self.__config.cpp_ns_end + _CPP_BR)

    def generate_web_api_header(self):
        """Generates C++ WebApi header, user should copy all code into WebApi.h manually.
        """
        if self.__cpp_manager_or_none is None:
            return

        cpp_manager = self.__cpp_manager_or_none

        header_file_name = 'web_api_{0}.h'.format(cpp_class_name_to_cpp_file_name(self.__class_name))
        file_path = 'build/core/api/{0}'.format(header_file_name)
        output_header = open(file_path, 'w')

        output_header.write(cpp_manager.generate_wep_api_declarations())

    def generate_web_api_implementation(self):
        """Generates C++ WebApi implementation.
        """
        if self.__cpp_manager_or_none is None:
            return

        cpp_manager = self.__cpp_manager_or_none

        output_cc = 'web_api_{0}.cc'.format(cpp_class_name_to_cpp_file_name(self.__class_name))
        file_path = 'build/core/api/{0}'.format(output_cc)
        output_cc = open(file_path, 'w')

        output_cc.write(cpp_manager.generate_web_api_implementation())

    def __generate_init_method_declarasion(self):
        parameters = ''
        for cpp_var in self.__cpp_var_list:
            parameters += cpp_var.initializer()
            parameters += ', '
        parameters = parameters[:-2]  # remove last 2 chars
        init_method = 'void Init({0});'.format(parameters)
        return init_method

    def __header_file_name(self):
        return cpp_class_name_to_cpp_file_name(self.__class_name)

    def __constructor_implementation(self):
        return '{0}::{0}() {{}}'.format(self.__class_name)

    def __deconstructor_implementation(self):
        return '{0}::~{0}() {{}}'.format(self.__class_name)

    def __init_method_implementation(self):
        parameters = ''
        for cpp_var in self.__cpp_var_list:
            parameters += cpp_var.initializer()
            parameters += ', '
        parameters = parameters[:-2]  # remove last char
        init_implementation = 'void {0}::Init({1}) {{\n'.format(self.__class_name, parameters)
        for cpp_var in self.__cpp_var_list:
            init_implementation += _CPP_SPACE
            init_implementation += cpp_var.initializer_implementation()
            init_implementation += '\n'
        init_implementation += '}'
        return init_implementation

    def __init_with_json_implementation(self):
        impl = 'bool {0}::InitWithJsonOrDie(const std::string& json) {{\n'.format(self.__class_name)
        impl += '{0}string error;\n'.format(_CPP_SPACE)
        impl += '{0}json11::Json json_obj = json11::Json::parse(json, error);\n\n'.format(_CPP_SPACE)
        impl += '{0}if (!error.empty()) {{\n'.format(_CPP_SPACE)
        impl += '{0}{0}sakura::log_error("{1} InitWithJson died");\n'.format(_CPP_SPACE, self.__class_name)
        impl += '{0}{0}return false;\n'.format(_CPP_SPACE)
        impl += '{0}}}\n\n'.format(_CPP_SPACE)

        for cpp_var in self.__cpp_var_list:
            impl += _CPP_SPACE
            impl += cpp_var.parse_json()
            impl += '\n'

        impl += '\n{0}return true;\n'.format(_CPP_SPACE)
        impl += '}'
        return impl

    def __clone_implementation(self):
        impl = 'std::unique_ptr<{0}> {0}::Clone() const {{\n'.format(self.__class_name)
        impl += _CPP_SPACE + 'std::unique_ptr<{0}> {1}(new {0}());\n'.format(self.__class_name, self.__class_name.lower())
        impl += _CPP_SPACE + '{0}->Init('.format(self.__class_name.lower())

        for cpp_var in self.__cpp_var_list:
            impl += cpp_var.private_var_without_type()
            impl += ', '

        impl = impl[:-2]  # remove last 2 chars
        impl += ');\n'

        impl += _CPP_SPACE + 'return {0};\n'.format(self.__class_name.lower())
        impl += '}'
        return impl

    def __find_replacement_by_define_name(self, define_name):
        """Returns replacement description by name
        """
        search_name = define_name[1:]
        for replacement in self.__cpp_replacement_list:
            if replacement.search == search_name:
                return replacement.replace
        return ''
