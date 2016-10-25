#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - Frank Lin

import re
from skrutil.skr_logger import skr_log_warning
from skrutil import string_utils


_OBJC_BR = '\n\n'
_OBJC_SPACE = '  '


class ObjcManager:

    def __init__(self, manager_name):
        self.manager_name = manager_name
        self.save_commands = []
        self.delete_commands = []
        self.fetch_commands = []
        self.apis = []

        self.object_name = ''
        self.plural_object_name = ''

        self.objc_variable_list = []

    def set_object_name(self, class_name, plural_class_name):
        self.object_name = class_name
        self.plural_object_name = plural_class_name

    def set_objc_variable_list(self, objc_variable_list):
        self.objc_variable_list = objc_variable_list

    def add_save_command(self, save_command):
        self.save_commands.append(save_command)

    def add_fetch_command(self, fetch_command):
        self.fetch_commands.append(fetch_command)

    def add_delete_command(self, delete_command):
        self.delete_commands.append(delete_command)

    def add_api_description(self, api_description):
        self.apis.append(api_description)

    def class_name(self):
        return self.manager_name

    def generate_fetch_declarations(self, config):
        """Generates Objective-C++ fetch declarations.

        Args:
            config: A <Config> object represents user-defined info.

        Returns:
            A string which is Objective-C++ fetch declarations.
        """
        declaration = ''
        for fetch_command in self.fetch_commands:
            by_list = []
            if fetch_command.where != '':
                by_list = re.split(',', fetch_command.where)

            if not fetch_command.is_plural:
                if len(by_list) == 0:
                    skr_log_warning('Singular often comes with at least one by parameter')
                declaration += '- (nullable {2}{0} *)fetch{0}FromCache{1};\n\n'\
                    .format(self.object_name, self.__convert_bys_to_string(by_list), config.objc_prefix)
            else:
                declaration += '- (NSArray<LCC{0} *> *)fetch{1}FromCache{2};\n\n'\
                    .format(self.object_name, self.plural_object_name, self.__convert_bys_to_string(by_list))
        return declaration

    def generate_fetch_implementations(self, config):
        """Generates Objective-C++ fetch implementations.

        Args:
            config: A <Config> object represents user-defined info.

        Returns:
            Objective-C++ fetch implementations.
        """
        impl = ''
        for fetch_command in self.fetch_commands:
            impl += self.__fetch_implementation(fetch_command, config)
            impl += _OBJC_BR
        return impl

    def generate_web_api_declarations(self, config):
        """Generates Objective-C++ web api declarations.

        Args:
            config: A <Config> object represents user-defined info.

        Returns:
            A string which is Objective-C++ web api declarations.
        """
        declaration = ''
        for api in self.apis:
            declaration += self.__web_api_declaration(api, config)
            declaration += ';'
            declaration += _OBJC_BR

        return declaration

    def generate_web_api_implementations(self, config):
        """Generates Objective-C++ web api implementations.

        Args:
            config: A <Config> object represents user-defined info.

        Returns:
            A string which is Objective-C++ web api implementations.
        """
        impl = ''
        for api in self.apis:
            impl += self.__web_api_declaration(api, config)
            impl += ' {\n'
            impl += string_utils.indent(2)
            impl += '_coreManagerHandler->\n'
            impl += string_utils.indent(2)
            impl += api.alias + '('
            for input_var in api.input_var_list:
                impl += input_var.cast_to_cpp_parameter()
                impl += ', '
            impl += '[successBlock, failureBlock](bool success, const std::string& errorUTF8String'
            for output_var in api.output_var_list:
                impl += ', {0}'.format(output_var.objc_wrapper_from_cpp_parameter(config))
            impl += ') {\n'
            impl += string_utils.indent(4)
            impl += 'if (success) {\n'
            for output_var in api.output_var_list:
                impl += output_var.objc_form_cpp_parameter(6, config)
                impl += _OBJC_BR

            impl += string_utils.indent(6)
            impl += 'successBlock('

            for i, output_var in enumerate(api.output_var_list):
                if i != 0:
                    impl += ', '
                impl += string_utils.to_objc_property_name(output_var.name)

            impl += ');\n'
            impl += string_utils.indent(4)
            impl += '} else {\n'
            impl += string_utils.indent(6)
            impl += 'NSString *error = [NSString stringWithUTF8String:errorUTF8String.c_str()];\n'
            impl += string_utils.indent(6)
            impl += 'failureBlock({0}(error));\n'.format(config.objc_error_method)
            impl += string_utils.indent(4)
            impl += '}\n'
            impl += string_utils.indent(2)
            impl += '});\n}'
            impl += _OBJC_BR
        return impl

    def generate_constructor_implementation(self, config):
        """Generates Objective-C++ init method.

        Args:
            config: A <Config> object represents user-defined info.

        Returns:
            Objective-C++ init method.
        """
        impl = '- (instancetype)init {\n'
        impl += string_utils.indent(2)
        impl += 'if (self = [super init]) {\n'
        impl += string_utils.indent(4)
        impl += '_coreManagerHandler = {1}::{0}Manager::DefaultManager();\n'.format(self.object_name,
                                                                                    config.cpp_namespace)
        impl += string_utils.indent(2)
        impl += '}\n'
        impl += string_utils.indent(2)
        impl += 'return self;\n'
        impl += '}'
        return impl

    def generate_default_manager_implementation(self, config):
        """Generates Objective-C++ default manager method.

        Args:
            config: A <Config> object represents user-defined info.

        Returns:
            Objective-C++ default manager method.
        """
        impl = '+ (instancetype)defaultManager {\n'
        impl += _OBJC_SPACE
        impl += 'return [{1}Director defaultDirector].{0}Manager;\n'.format(
            string_utils.first_char_to_lower(self.object_name), config.objc_prefix)
        impl += '}'
        return impl

    def __convert_bys_to_string(self, by_string_list):
        """Returns "ById:(NSString *)id name:(NSString *)name" or ""
        """
        if len(by_string_list) == 0:  # empty string
            return ''
        else:  # "(const std::string& id, const std::string& username)"
            bys_string = 'By'
            it = 0
            for by_string in by_string_list:
                objc_var = self.__objc_var_by_name(by_string)
                if objc_var is not None:
                    if it == 0:
                        bys_string += string_utils.first_char_to_upper(objc_var.parameter()) + ' '
                    else:
                        bys_string += objc_var.parameter() + ' '
                    it += 1
                else:
                    print 'Unknown "{0}" in "by"'.format(by_string)
                    return ''
            bys_string = bys_string[:-1]
            return bys_string

    def __objc_var_by_name(self, name_string):
        """Returns None if not found.
        """
        for objc_var in self.objc_variable_list:
            if objc_var.name == name_string:
                return objc_var
        return None

    def __fetch_implementation(self, fetch_command, config):
        """Generates Objective-C++ fetch implementation.

        Args:
            fetch_command: A <FetchCommand> object represents necessary info for generating fetch implementation.
            config: A <Config> object represents user-defined info.

        Returns:
            A string which is Objective-C++ fetch implementation.
        """
        by_list = []
        if fetch_command.where != '':
            by_list = re.split(',', fetch_command.where)

        if not fetch_command.is_plural:
            impl = '- (nullable {2}{0} *)fetch{0}FromCache{1} {{\n'\
                    .format(self.object_name, self.__convert_bys_to_string(by_list), config.objc_prefix)
            impl += string_utils.indent(2)
            impl += 'std::unique_ptr<{2}::{0}> core{0} = _coreManagerHandler->{1};\n'\
                .format(self.object_name, self.__cpp_fetch_method_name(fetch_command), config.cpp_namespace)
            impl += string_utils.indent(2)
            impl += 'if (core{0}) {{\n'.format(self.object_name)
            impl += string_utils.indent(4)
            impl += 'return [{2}{0} {1}WithCore{0}:*core{0}];\n'\
                .format(self.object_name, string_utils.first_char_to_lower(self.object_name), config.objc_prefix)
            impl += string_utils.indent(2)
            impl += '}\n'
            impl += string_utils.indent(2)
            impl += 'return nil;\n'
            impl += '}'
            return impl
        else:
            impl = '- (NSArray<LCC{0} *> *)fetch{1}FromCache{2} {{\n'\
                    .format(self.object_name, self.plural_object_name, self.__convert_bys_to_string(by_list))
            impl += string_utils.indent(2)
            impl += 'NSMutableArray *{0} = [NSMutableArray array];\n'.format(string_utils.first_char_to_lower(self.plural_object_name))
            impl += string_utils.indent(2)
            impl += 'std::vector<std::unique_ptr<{3}::{0}>> core{1} = _coreManagerHandler->{2};\n'\
                .format(self.object_name,
                        self.plural_object_name,
                        self.__cpp_fetch_method_name(fetch_command),
                        config.objc_prefix)
            impl += string_utils.indent(2)
            impl += 'for (auto it = core{0}.begin(); it != core{0}.end(); ++it) {{\n'.format(self.plural_object_name)
            impl += string_utils.indent(4)
            impl += '[{0} addObject:[LCC{1} {2}WithCore{1}:(**it)]];\n'\
                .format(string_utils.first_char_to_lower(self.plural_object_name),
                        self.object_name,
                        string_utils.first_char_to_lower(self.object_name))
            impl += string_utils.indent(2)
            impl += '}\n'
            impl += string_utils.indent(2)
            impl += 'return [{0} copy];\n'.format(string_utils.first_char_to_lower(self.plural_object_name))
            impl += '}\n'
            self.impl = impl
            return self.impl

    def __cpp_fetch_method_name(self, fetch_command):
        by_list = []
        if fetch_command.where != '':
            by_list = re.split(',', fetch_command.where)

        if not fetch_command.is_plural:
            if len(by_list) == 0:
                skr_log_warning('Singular often comes with at least one by parameter')
            return 'Fetch{0}FromCache{1}'\
                .format(self.object_name, self.__convert_bys_to_cpp_string(by_list))
        else:
            return 'Fetch{0}FromCache{1}'\
                .format(self.plural_object_name, self.__convert_bys_to_cpp_string(by_list))

    def __convert_bys_to_cpp_string(self, by_string_list):
        """Returns "ById([id UTF8String])" or "([id UTF8String], [username UTF8String])" or "()".
        """
        if len(by_string_list) == 0:  # ()
            return '()'
        elif len(by_string_list) == 1:  # "ById(const std::string& id)"
            by_string = by_string_list[0]
            objc_var = self.__objc_var_by_name(by_string)
            if objc_var is not None:
                return 'By{0}({1})'.format(objc_var.to_title_style_name(), objc_var.cast_to_cpp_parameter())
            else:
                print 'Unknown "{0}" in "by"'.format(by_string)
                return ''
        else:  # "([id UTF8String], [username UTF8String])"
            bys_string = '('
            for by_string in by_string_list:
                objc_var = self.__objc_var_by_name(by_string)
                if objc_var is not None:
                    bys_string += objc_var.cast_to_cpp_parameter() + ', '
                else:
                    print 'Unknown "{0}" in "by"'.format(by_string)
                    return ''
            bys_string = bys_string[:-2]  # remove last 2 chars
            bys_string += ')'
            return bys_string

    def __web_api_declaration(self, api, config):
        declaration = ''
        declaration += '- (void){0}'.format(string_utils.first_char_to_lower(api.alias))
        if len(api.input_var_list) > 0:
                if len(api.input_var_list) == 1:
                    declaration += 'By'
                else:
                    declaration += 'With'
                for i, input_var in enumerate(api.input_var_list):
                    input_name = string_utils.to_objc_property_name(input_var.name)
                    if i == 0:
                        input_name = string_utils.first_char_to_upper(input_name)
                    declaration += '{0}:({1}){2} '.format(input_name,
                                                          input_var.var_type.to_objc_getter_string(config),
                                                          string_utils.first_char_to_lower(input_name))
                declaration += 'success:(void (^)('
        else:
            declaration += 'Success:(void (^)('
        if len(api.output_var_list) > 0:
            for i, output_var in enumerate(api.output_var_list):
                declaration += output_var.var_type.to_objc_getter_string(config)
                declaration += string_utils.to_objc_property_name(output_var.name)
                if i != len(api.output_var_list) - 1:
                    declaration += ', '
        declaration += '))successBlock failure:(void (^)(NSError *error))failureBlock'
        return declaration
