#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - Frank Lin

import re
from java_variable import VarType
from skrutil.skr_logger import skr_log_warning
from skrutil import string_utils
from skrutil.string_utils import indent

_JAVA_BR = '\n\n'
_JAVA_SPACE = '    '


class JavaManagerFetchCommand:
    """Used for Java FetchObject(s)FromCache method.

    Attributes:
        is_plural: A bool describes method target is singular or plural.
        where: A string value represents SQL where syntax.
        alias: A string value tells manager to use another name.
    """

    def __init__(self, is_plural, where, alias):
        """Init fetch method necessary info.

        Args:
            is_plural: A bool describes method target is singular or plural.
            where: A string value represents SQL where syntax.
            alias: A string value tells manager to use another name.
        """
        self.is_plural = is_plural

        if where is not None:
            self.where = where
        else:
            self.where = ''

        if alias is not None:
            self.alias = alias
        else:
            self.alias = ''


class JavaApiDescription:
    """Used for giving manager necessary info for generating WebAPI description.

    Attributes:
            function_name: A string describes the function name used in WebApi.
            input_var_list: A list of <JavaVariable> describes the input variables.
            output_var_list: A list of <JavaVariable> describes the output variables.
    """
    def __init__(self, function_name, input_var_list, output_var_list):
        """Init API description with necessary parameters.

        Args:
            function_name: A string describes the function name used in WebApi.
            input_var_list: A list of <JavaVariable> describes the input variables.
            output_var_list: A list of <JavaVariable> describes the output variables.
        """
        self.function_name = function_name
        self.input_var_list = input_var_list
        self.output_var_list = output_var_list


class JavaManager:
    """Used for generating Java manager implementation code.

    Attributes:
        manager_name: A string describes the manager's name.
        apis: List of <JavaApiDescription> describes manager's APIs.
    """

    def __init__(self, manager_name):
        """Init with manager class name.

        Args:
            manager_name: The manager class name.
        """
        self.__manager_name = manager_name
        self.__object_name = ''
        self.__plural_object_name = ''
        self.__java_variable_list = []
        self.__fetch_commands = []
        self.__apis = []

    def set_object_name(self, class_name, plural_class_name):
        """Sets the object name and plural class name for manager.

        Args:
            class_name: A string which is the object class name (eg: User).
            plural_class_name: A string which is the object class name in plural case (eg: Butterflies).
        """
        self.__object_name = class_name
        self.__plural_object_name = plural_class_name

    def set_java_variable_list(self, java_variable_list):
        self.__java_variable_list = java_variable_list

    def add_fetch_command(self, fetch_command):
        """Adds fetch command.

        Args:
            fetch_command: A <JavaFetchCommand> object has the necessary info for generating fetch method.
        """
        self.__fetch_commands.append(fetch_command)

    def add_api_description(self, api_description):
        """Adds API description.

        Args:
            api_description: A <JavaApiDescription> object that has necessary info for generating WebApi methods.
        """
        self.__apis.append(api_description)

    def generate_fetch_v2(self):
        """Gets fetch method implementation code. Paris with <generate_fetch_native_v2>.

        Returns:
            A string describes Java fetch method implementation code.
        """
        fetch_function = ''
        for fetch_command in self.__fetch_commands:
            by_list = []
            if fetch_command.where != '':
                by_list = re.split(',', fetch_command.where)

            if fetch_command.alias != '':
                fetch_fun_name = string_utils.first_char_to_lower(fetch_command.alias)
                fetch_fun_name_native = fetch_command.alias
            elif not fetch_command.is_plural:
                fetch_fun_name = 'fetch{0}FromCache'.format(self.__java_object_name())
                fetch_fun_name_native = 'Fetch{0}FromCache'.format(self.__object_name)
            else:
                fetch_fun_name = 'fetch{0}FromCache'.format(self.__plural_object_name)
                fetch_fun_name_native = 'Fetch{0}FromCache'.format(self.__plural_object_name)

            if not fetch_command.is_plural:  # singular implementation
                if len(by_list) == 0:
                    skr_log_warning('Singular often comes with at least one by parameter')
                fetch_function += indent(4) + '@Nullable\n'
                fetch_function += indent(4) + 'public {0} '.format(self.__java_object_name())
                fetch_function += fetch_fun_name + self.__convert_bys_to_string(by_list, False, False) + '{\n'

                parameters = self.__convert_bys_to_input_parameters(by_list)
                parameters_with_type = self.__convert_bys_to_string(by_list, False, False)
                parameters_for_func = re.sub('\([^]]*\)', parameters, parameters_with_type)
                fetch_function += indent(8) + 'return native{0}{1};\n'.format(fetch_fun_name_native,
                                                                              parameters_for_func)
                fetch_function += indent(4) + '}' + _JAVA_BR
            else:  # regular implementation
                fetch_function += indent(4) + 'public {0}[] '.format(self.__java_object_name())
                fetch_function += fetch_fun_name + self.__convert_bys_to_string(by_list, False, False) + ' {\n'

                parameters = self.__convert_bys_to_input_parameters(by_list)
                parameters_with_type = self.__convert_bys_to_string(by_list, False, False)
                parameters_for_func = re.sub('\([^]]*\)', parameters, parameters_with_type)
                fetch_function += indent(8) + 'return native{0}{1};\n'.format(fetch_fun_name_native,
                                                                              parameters_for_func)
                fetch_function += indent(4) + '}' + _JAVA_BR
        return fetch_function

    def generate_fetch(self):
        """Gets fetch method implementation code. Paris with <generate_fetch_native>.

        New development should use <generate_fetch_v2>.

        Returns:
            A string describes Java fetch method implementation code.
        """
        fetch_function = ''
        for fetch_command in self.__fetch_commands:
            by_list = []
            if fetch_command.where != '':
                by_list = re.split(',', fetch_command.where)

            if fetch_command.alias != '':
                fetch_fun_name = string_utils.first_char_to_lower(fetch_command.alias)
                fetch_fun_name_native = fetch_command.alias
            elif not fetch_command.is_plural:
                fetch_fun_name = 'fetch{0}FromCache'.format(self.__java_object_name())
                fetch_fun_name_native = 'Fetch{0}FromCache'.format(self.__object_name)
            else:
                fetch_fun_name = 'fetch{0}FromCache'.format(self.__plural_object_name)
                fetch_fun_name_native = 'Fetch{0}FromCache'.format(self.__plural_object_name)

            if not fetch_command.is_plural:
                if len(by_list) == 0:
                    skr_log_warning('Singular often comes with at least one by parameter')
                fetch_function += indent(4) + 'public {0} '.format(self.__java_object_name())
                fetch_function += fetch_fun_name + self.__convert_bys_to_string(by_list, False, False) + '{\n'

                fetch_function += indent(8) + 'long handler = native' + fetch_fun_name_native
                fetch_function += self.__convert_bys_to_string(by_list, False, True) + ';\n\n'

                fetch_function += indent(8) + 'if (handler == JniHelper.sNullPointer) {\n'
                fetch_function += indent(12) + 'return null;\n'
                fetch_function += indent(8) + '}\n\n'
                fetch_function += indent(8) + 'return new {0}(handler);\n'.format(self.__java_object_name())
                fetch_function += indent(4) + '}' + _JAVA_BR
            else:
                fetch_function += indent(4) + 'public List<{0}> '.format(self.__java_object_name())
                fetch_function += fetch_fun_name + self.__convert_bys_to_string(by_list, False, False) + ' {\n'

                fetch_function += indent(8) + 'long[] handlers = native' + fetch_fun_name_native
                fetch_function += self.__convert_bys_to_string(by_list, False, True) + ';\n\n'

                fetch_function += indent(8) + 'List<{0}> {1} = new ArrayList<>();\n'\
                    .format(self.__java_object_name(), self.__to_object_name_java_style() + 's')
                fetch_function += indent(8) + 'for (long handler: handlers) {\n'
                fetch_function += indent(12) + '{0}.add(new {1}(handler));\n'\
                    .format(self.__to_object_name_java_style() + 's', self.__java_object_name())
                fetch_function += indent(8) + '}\n\n'
                fetch_function += indent(8) + 'return {0};\n'\
                    .format(self.__to_object_name_java_style() + 's')
                fetch_function += indent(4) + '}' + _JAVA_BR
        return fetch_function

    def generate_fetch_native_v2(self):
        """Gets fetch method JNI part implementation code. Paris with <generate_fetch_v2>.

        Returns:
            Implementation of JNI part of fetch methods.
        """
        fetch_function = ''
        for fetch_command in self.__fetch_commands:
            by_list = []
            if fetch_command.where != '':
                by_list = re.split(',', fetch_command.where)

            if fetch_command.alias != '':
                fetch_fun_name_native = fetch_command.alias
            elif not fetch_command.is_plural:
                fetch_fun_name_native = 'Fetch{0}FromCache'.format(self.__object_name)
            else:
                fetch_fun_name_native = 'Fetch{0}FromCache'.format(self.__plural_object_name)

            if not fetch_command.is_plural:
                if len(by_list) == 0:
                    skr_log_warning('Singular often comes with at least one by parameter')
                fetch_function += indent(4) + 'private native @Nullable {0} native'.format(self.__object_name)
                fetch_function += fetch_fun_name_native
                fetch_function += self.__convert_bys_to_string(by_list, True, False) + ';' + _JAVA_BR
            else:
                fetch_function += indent(4) + 'private native {0}[] native'.format(self.__object_name)
                fetch_function += fetch_fun_name_native
                fetch_function += self.__convert_bys_to_string(by_list, True, False) + ';' + _JAVA_BR
        return fetch_function

    def generate_fetch_native(self):
        """Gets fetch method JNI part implementation code. Paris with <generate_fetch>.

        Returns:
            Implementation of JNI part of fetch methods.
        """
        fetch_function = ''
        for fetch_command in self.__fetch_commands:
            by_list = []
            if fetch_command.where != '':
                by_list = re.split(',', fetch_command.where)

            if fetch_command.alias != '':
                fetch_fun_name_native = fetch_command.alias
            elif not fetch_command.is_plural:
                fetch_fun_name_native = 'Fetch{0}FromCache'.format(self.__object_name)
            else:
                fetch_fun_name_native = 'Fetch{0}FromCache'.format(self.__plural_object_name)

            if not fetch_command.is_plural:
                if len(by_list) == 0:
                    skr_log_warning('Singular often comes with at least one by parameter')
                fetch_function += indent(4) + 'private native long native' + fetch_fun_name_native
                fetch_function += self.__convert_bys_to_string(by_list, True, False) + ';' + _JAVA_BR
            else:
                fetch_function += indent(4) + 'private native long[] native' + fetch_fun_name_native
                fetch_function += self.__convert_bys_to_string(by_list, True, False) + ';' + _JAVA_BR
        return fetch_function

    def generate_http_variables(self):
        """Gets HTTP response fields implementation.

        Returns:
            A string that describes HTTP response fields. For example:

            private WebApiWithListResponse mGetTasksAssignedToMeResponse;
        """
        api_response_variable = ''
        for api in self.__apis:
            variable_name = 'm{0}Response'.format(api.function_name)
            variable_type = self.__variable_type_from_var_list(api.output_var_list)
            api_response_variable += indent(4) + 'private ' + variable_type + variable_name + ';\n'
        return api_response_variable

    def generate_http_function(self, version):
        """Gets HTTP request and response implementation code.

        Args:
            version: An int represents java builder version number.

        Returns:
            HTTP request and response implementation code.
        """
        http_function = ''
        for api in self.__apis:
            if version < 6.0:
                http_function += self.__http_function(api) + '\n\n' + self.__http_function_response(api) + '\n\n'
            else:
                http_function += self.__http_function(api) + '\n\n' + self.__http_function_response_v2(api) + '\n\n'
        return http_function

    def generate_http_function_native(self):
        """Gets HTTP request native code.

        Returns:
            HTTP request native code.
        """
        http_native_function = ''
        for api in self.__apis:
            http_native_function += indent(4) + 'private native void native{0}(long handler{1});\n\n' \
                .format(api.function_name, self.__input_variable_declarations_native(api.input_var_list))
        return http_native_function

    def __http_function(self, api):
        http_function = indent(4) + 'public void ' + string_utils.first_char_to_lower(api.function_name)
        input_variable = self.__input_variable_declarations(api.input_var_list)
        http_function += '({0}{1}response){{\n'\
            .format(input_variable, self.__variable_type_from_var_list(api.output_var_list))
        http_function += indent(8) + 'm{0}Response'.format(api.function_name) + ' = response;\n'
        for variable in api.input_var_list:
            if variable.var_type == VarType.cpp_enum:
                http_function += indent(8) + 'int {0} = {1}.getValue();\n'\
                    .format(variable.name_str + "_int", variable.name_str)
            if variable.var_type == VarType.cpp_object:
                http_function += indent(8) + 'long {0} = {1}.getNativeHandler();\n'\
                    .format(variable.name_str + '_handler', variable.name_str)
            if variable.var_type == VarType.cpp_object_array:
                http_function += indent(8) + 'long[] {0} = new long[{1}.size()];\n'\
                    .format(variable.name_str + '_handler', variable.name_str)
                http_function += indent(8) + 'for (int i = 0; i < {0}.size(); i++){{\n'.format(variable.name_str)
                http_function += indent(12) + '{0}[i] = {1}.get(i).getNativeHandler();\n'\
                    .format(variable.name_str + '_handler', variable.name_str)
                http_function += indent(8) + '}'
        input_variable_call = self.__input_variable_call(api.input_var_list)
        http_function += indent(8) + 'native{0}(mNativeHandler{1});\n'\
            .format(api.function_name, input_variable_call)
        http_function += indent(4) + "}"
        return http_function

    def __http_function_response_v2(self, api):
        http_function_response = indent(4) + 'public void on{0}(boolean success, String error{1}){{\n' \
            .format(api.function_name, self.__output_variable_declaration_v2(api.output_var_list))
        http_function_response += indent(8) + 'if (m{0}Response == null){{\n'.format(api.function_name)
        http_function_response += indent(12) + 'return;\n'
        http_function_response += indent(8) + '}\n'
        http_function_response += indent(8) + 'if (success){\n'
        http_function_response += indent(12) + 'm{0}Response.onSuccess({1});\n' \
            .format(api.function_name, self.__output_variable_call(api.output_var_list))
        http_function_response += indent(8) + '} else {\n'
        http_function_response += indent(12) + 'm{0}Response.onFailure(error);\n'.format(api.function_name)
        http_function_response += indent(8) + '}\n'
        http_function_response += indent(4) + '}'
        return http_function_response

    def __http_function_response(self, api):
        http_function_response = indent(4) + 'public void on{0}(boolean success, String error{1}){{\n'\
            .format(api.function_name, self.__output_variable_declaration(api.output_var_list))
        http_function_response += indent(8) + 'if (m{0}Response == null){{\n'.format(api.function_name)
        http_function_response += indent(12) + 'return;\n'
        http_function_response += indent(8) + '}\n'
        http_function_response += indent(8) + 'if (success){\n'
        for variable in api.output_var_list:
            if variable.var_type == VarType.cpp_enum:
                http_function_response += indent(12) + '{0}.{1} {2} = {0}.{1}.get{1}ByValue({3});\n'\
                    .format(self.__object_name, variable.var_type.to_java_getter_setter_string(), variable.name_str,
                            variable.name_str + '_int')
            if variable.var_type == VarType.cpp_object:
                http_function_response += indent(12) + '{0} {1} = new {0}({1}_handler);\n'\
                    .format(variable.var_type.to_java_getter_setter_string(), variable.name_str)
            if variable.var_type == VarType.cpp_object_array:
                http_function_response += indent(12) + 'ArrayList<CoreObject> {0} = new ArrayList<>();\n'\
                    .format(variable.name_str)
                http_function_response += indent(12) + 'for (long handler : {0}_handler){{\n'\
                    .format(variable.name_str)
                http_function_response += indent(16) + '{0}.add(new {1}(handler));\n'\
                    .format(variable.name_str, variable.var_type.object_class_name)
                http_function_response += indent(12) + '}\n'

        http_function_response += indent(12) + 'm{0}Response.onSuccess({1});\n'\
            .format(api.function_name, self.__output_variable_call(api.output_var_list))
        http_function_response += indent(8) + '} else {\n'
        http_function_response += indent(12) + 'm{0}Response.onFailure(error);\n'.format(api.function_name)
        http_function_response += indent(8) + '}\n'
        http_function_response += indent(4) + '}'
        return http_function_response

    def __variable_type_from_var_list(self, var_list):
        if len(var_list) == 0:
            variable_type = '@Nullable WebApiResponse '
        elif len(var_list) == 1:
            if var_list[0].var_type == VarType.cpp_object:
                variable_type = '@Nullable WebApiWithCoreObjectResponse '
            elif var_list[0].var_type == VarType.cpp_object_array:
                variable_type = '@Nullable WebApiWithListResponse '
            else:
                variable_type = '/*TODO .....*/@Nullable WebApiResponse '
        else:
            variable_type = '/*TODO .....*/@Nullable WebApiResponse '
        return variable_type

    def __input_variable_call(self, var_list):
        vars_declarations = ''
        for var in var_list:
            if var.var_type == VarType.cpp_enum:
                vars_declarations += ', ' + var.name_str + '_int'
            elif var.var_type == VarType.cpp_object:
                vars_declarations += ', ' + var.name_str + '_handler'
            elif var.var_type == VarType.cpp_object_array:
                vars_declarations += ', ' + var.name_str + '_handler'
            else:
                vars_declarations += ', ' + var.name_str
        return vars_declarations

    def __input_variable_declarations(self, var_list):
        vars_declarations = ''
        for var in var_list:
            if var.var_type == VarType.cpp_enum:
                vars_declarations += var.var_type.to_java_getter_setter_string()\
                                     + ' ' + var.name_str + ', '
            else:
                vars_declarations += var.var_type.to_java_getter_setter_string() + ' ' + var.name_str + ', '
        return vars_declarations

    def __output_variable_declaration_v2(self, var_list):
        vars_declarations = ''
        for var in var_list:
            if var.var_type == VarType.cpp_enum:
                vars_declarations += ', int ' + var.name_str + '_int'
            elif var.var_type == VarType.cpp_object:
                vars_declarations += ', Object ' + var.name_str
            elif var.var_type == VarType.cpp_object_array:
                vars_declarations += ', Object[] ' + var.name_str
            else:
                vars_declarations += ', ' + var.var_type + ' ' + var.name_str
        return vars_declarations

    def __output_variable_declaration(self, var_list):
        vars_declarations = ''
        for var in var_list:
            if var.var_type == VarType.cpp_enum:
                vars_declarations += ', int ' + var.name_str + '_int'
            elif var.var_type == VarType.cpp_object:
                vars_declarations += ', long ' + var.name_str + '_handler'
            elif var.var_type == VarType.cpp_object_array:
                vars_declarations += ', long[] ' + var.name_str + '_handler'
            else:
                vars_declarations += ', ' + var.var_type + ' ' + var.name_str
        return vars_declarations

    def __output_variable_call(self, var_list):
        vars_declarations = ''
        for var in var_list:
            vars_declarations += var.name_str + ', '
        return vars_declarations[:-2]

    def __input_variable_declarations_native(self, var_list):
        vars_declarations = ''
        for var in var_list:
            if var.var_type == VarType.cpp_enum:
                vars_declarations += ', int ' + var.name_str + '_int'
            elif var.var_type == VarType.cpp_object:
                vars_declarations += ', long ' + var.name_str + '_handler'
            elif var.var_type == VarType.cpp_object_array:
                vars_declarations += ', long[] ' + var.name_str + '_handler'
            else:
                vars_declarations += ', ' + var.var_type.to_java_getter_setter_string() + ' ' + var.name_str
        return vars_declarations

    def __convert_bys_to_input_parameters(self, by_list):
        """Returns (taskId, username, displayName).

        Args:
            by_list: Where bys.

        Returns:
            A string which is like (taskId, username, displayName).
        """
        list = []
        list.append('mNativeHandler')
        for by in by_list:
            by = string_utils.to_objc_property_name(by)
            list.append(by)
        parameters = ', '.join(list)
        parameters = '({0})'.format(parameters)
        return parameters

    def __convert_bys_to_string(self, by_string_list, is_native_declaration, is_native_call):
        """Returns "ById(String id)" or "(String id, String username)" or "()".

        Args:
            by_string_list: List of string represents where components.
            is_native_declaration: A bool value indicates it is used in JNI.
            is_native_call: A bool value indicates it is used in JNI.

        Returns:
            "ById(String id)" or "(String id, String username)" or "()"
        """
        if len(by_string_list) == 0:  # ()
            if is_native_declaration:
                return '(long handler)'
            elif is_native_call:
                return '(mNativeHandler)'
            return '()'
        elif len(by_string_list) == 1:  # "ById(String id)"
            by_string = by_string_list[0]
            java_var = self.__java_var_by_name(by_string)
            if java_var is not None:
                if is_native_declaration:
                    if java_var.var_type == VarType.cpp_enum:
                        return 'By{0}(long handler, {1} {2})'.format(java_var.get_set_name_str, 'int',
                                                                     java_var.name_str)
                    elif java_var.var_type == VarType.cpp_string_array:
                        return 'By{0}(long handler, {1} {2})'.format(java_var.get_set_name_str, 'String[]',
                                                                     java_var.name_str)
                    return 'By{0}(long handler, {1} {2})'.format(java_var.get_set_name_str,
                                                                 java_var.var_type.to_java_getter_setter_string(),
                                                                 java_var.name_str)
                elif is_native_call:
                    if java_var.var_type == VarType.cpp_enum:
                        return 'By{0}(mNativeHandler, {1}.getValue())'.format(java_var.get_set_name_str, java_var.name_str)
                    elif java_var.var_type == VarType.cpp_string_array:
                        return 'By{0}(mNativeHandler, new String[{1}.size()])'.format(java_var.get_set_name_str, java_var.name_str)
                    return 'By{0}(mNativeHandler, {1})'.format(java_var.get_set_name_str, java_var.name_str)
                else:
                    if java_var.var_type == VarType.cpp_enum:
                        return 'By{0}({1} {2})'.format(java_var.get_set_name_str, java_var.java_enum, java_var.name_str)
                    return 'By{0}({1} {2})'.format(java_var.get_set_name_str,
                                                   java_var.var_type.to_java_getter_setter_string(), java_var.name_str)
            else:
                print('Unknown "{0}" in "by"'.format(by_string))
                return ''
        else:  # "(String id, String username)"
            bys_string = '('
            index = 0
            for by_string in by_string_list:
                java_var = self.__java_var_by_name(by_string)
                if java_var is not None:
                    if is_native_declaration:
                        if index == 0:
                            bys_string += 'long handler, '
                        if java_var.var_type == VarType.cpp_enum:
                            bys_string += '{0} {1}, '.format('int', java_var.name_str)
                        elif java_var.var_type == VarType.cpp_string_array:
                            bys_string += '{0} {1}, '.format('String[]', java_var.name_str)
                        else:
                            bys_string += '{0} {1}, '.format(java_var.var_type.to_java_getter_setter_string(),
                                                             java_var.name_str)
                    elif is_native_call:
                        if index == 0:
                            bys_string += 'mNativeHandler, '
                        if java_var.var_type == VarType.cpp_enum:
                            bys_string += '{0}.getValue(), '.format(java_var.name_str)
                        elif java_var.var_type == VarType.cpp_string_array:
                            bys_string += 'new String[{0}.size()], '.format(java_var.name_str)
                        else:
                            bys_string += '{0}, '.format(java_var.name_str)
                    else:
                        if java_var.var_type == VarType.cpp_enum:
                            bys_string += '{0} {1}, '.format(java_var.java_enum, java_var.name_str)
                        else:
                            bys_string += '{0} {1}, '.format(java_var.var_type.to_java_getter_setter_string(),
                                                             java_var.name_str)
                else:
                    print('Unknown "{0}" in "by"'.format(by_string))
                    return ''
                index += 1
            bys_string = bys_string[:-2]  # remove last 2 chars
            bys_string += ')'
            return bys_string

    # returns None if not found
    def __java_var_by_name(self, name_string):
        for java_var in self.__java_variable_list:
            if java_var.name_str == self.__by_string_to_java_field_style(name_string):
                return java_var
        return None

    def __by_string_to_java_field_style(self, by_string):
        name_splits = re.split('_', by_string)
        var_name_str = ''
        for index in (1, len(name_splits)):
            if index == 1:
                var_name_str = name_splits[index - 1]
            else:
                var_name_str += name_splits[index - 1].capitalize()
        return var_name_str

    def __java_object_name(self):
        """Since List is a built-in type in Java, use full name instead.

        Returns:
            A string represents Java object name.
        """
        new_object_name = ''
        if self.__object_name == 'List':
            new_object_name = 'com.lesschat.core.task.List'
        else:
            new_object_name = self.__object_name
        return new_object_name

    def __to_object_name_java_style(self):
        new_object_name = ''
        new_object_name = self.__object_name[0].lower() + self.__object_name[1:]
        return new_object_name

    @property
    def manager_name(self):
        return self.__manager_name

    @property
    def apis(self):
        return self.__apis
