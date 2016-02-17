import re
from java_variable import VarType
from skrutil.skr_logger import skr_log_warning
from skrutil import string_utils

_JAVA_BR = '\n\n'
_JAVA_SPACE = '    '


def function_space(count):
    space = ''
    for i in range(1, count + 1):
        space += _JAVA_SPACE
    return space


class JavaManagerFetchCommand:
    def __init__(self, is_plural, where, alias):
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

    def __init__(self, function_name, input_var_list, output_var_list):
        self.function_name = function_name
        self.input_var_list = input_var_list
        self.output_var_list = output_var_list


class JavaManager:
    def __init__(self, manager_name):
        self.manager_name = manager_name
        self.object_name = ''
        self.plural_object_name = ''
        self.java_variable_list = []
        self.fetch_commands = []
        self.apis = []

    def set_object_name(self, class_name, plural_class_name):
        self.object_name = class_name
        self.plural_object_name = plural_class_name

    def set_java_variable_list(self, java_variable_list):
        self.java_variable_list = java_variable_list

    def add_fetch_command(self, fetch_command):
        self.fetch_commands.append(fetch_command)

    def add_api_description(self, api_description):
        self.apis.append(api_description)

    def generate_fetch(self):
        fetch_function = ''
        for fetch_command in self.fetch_commands:
            by_list = []
            if fetch_command.where != '':
                by_list = re.split(',', fetch_command.where)

            if fetch_command.alias != '':
                fetch_fun_name = string_utils.first_char_to_lower(fetch_command.alias)
                fetch_fun_name_native = fetch_command.alias
            elif not fetch_command.is_plural:
                fetch_fun_name = 'fetch{0}FromCache'.format(self.__rename_object_name_if_list())
                fetch_fun_name_native = 'Fetch{0}FromCache'.format(self.object_name)
            else:
                fetch_fun_name = 'fetch{0}FromCache'.format(self.plural_object_name)
                fetch_fun_name_native = 'Fetch{0}FromCache'.format(self.plural_object_name)

            if not fetch_command.is_plural:
                if len(by_list) == 0:
                    skr_log_warning('Singular often comes with at least one by parameter')
                fetch_function += function_space(1) + 'public {0} '.format(self.__rename_object_name_if_list())
                fetch_function += fetch_fun_name + self.__convert_bys_to_string(by_list, False, False) + '{\n'

                fetch_function += function_space(2) + 'long handler = native' + fetch_fun_name_native
                fetch_function += self.__convert_bys_to_string(by_list, False, True) + ';\n\n'

                fetch_function += function_space(2) + 'if (handler == JniHelper.sNullPointer) {\n'
                fetch_function += function_space(3) + 'return null;\n'
                fetch_function += function_space(2) + '}\n\n'
                fetch_function += function_space(2) + 'return new {0}(handler);\n'.format(self.__rename_object_name_if_list())
                fetch_function += function_space(1) + '}' + _JAVA_BR
            else:
                fetch_function += function_space(1) + 'public List<{0}> '.format(self.__rename_object_name_if_list())
                fetch_function += fetch_fun_name + self.__convert_bys_to_string(by_list, False, False) + ' {\n'

                fetch_function += function_space(2) + 'long[] handlers = native' + fetch_fun_name_native
                fetch_function += self.__convert_bys_to_string(by_list, False, True) + ';\n\n'

                fetch_function += function_space(2) + 'List<{0}> {1} = new ArrayList<>();\n'\
                    .format(self.__rename_object_name_if_list(), self.__to_object_name_java_style() + 's')
                fetch_function += function_space(2) + 'for (long handler: handlers) {\n'
                fetch_function += function_space(3) + '{0}.add(new {1}(handler));\n'\
                    .format(self.__to_object_name_java_style() + 's', self.__rename_object_name_if_list())
                fetch_function += function_space(2) + '}\n\n'
                fetch_function += function_space(2) + 'return {0};\n'\
                    .format(self.__to_object_name_java_style() + 's')
                fetch_function += function_space(1) + '}' + _JAVA_BR
        return fetch_function

    def generate_fetch_native(self):
        fetch_function = ''
        for fetch_command in self.fetch_commands:
            by_list = []
            if fetch_command.where != '':
                by_list = re.split(',', fetch_command.where)

            if fetch_command.alias != '':
                fetch_fun_name_native = fetch_command.alias
            elif not fetch_command.is_plural:
                fetch_fun_name_native = 'Fetch{0}FromCache'.format(self.object_name)
            else:
                fetch_fun_name_native = 'Fetch{0}FromCache'.format(self.plural_object_name)

            if not fetch_command.is_plural:
                if len(by_list) == 0:
                    skr_log_warning('Singular often comes with at least one by parameter')
                fetch_function += function_space(1) + 'private native long native' + fetch_fun_name_native
                fetch_function += self.__convert_bys_to_string(by_list, True, False) + ';' + _JAVA_BR
            else:
                fetch_function += function_space(1) + 'private native long[] native' + fetch_fun_name_native
                fetch_function += self.__convert_bys_to_string(by_list, True, False) + ';' + _JAVA_BR
        return fetch_function

    def generate_http_variable(self):
        api_response_variable = ''
        for api in self.apis:
            variable_name = 'm{0}Response'.format(api.function_name)
            variable_type = self.__variable_type_from_var_list(api.output_var_list)
            api_response_variable += function_space(1) + 'private ' + variable_type + variable_name + ';\n'
        return api_response_variable

    def generate_http_function(self):
        http_function = ''
        for api in self.apis:
            http_function += self.__http_function(api) + '\n\n' + self.__http_function_response(api) + '\n\n'
        return http_function

    def __http_function(self, api):
        http_function = function_space(1) + 'public void ' + string_utils.first_char_to_lower(api.function_name)
        input_variable = self.__input_variable_declarations(api.input_var_list)
        http_function += '({0}{1}response){{\n'\
            .format(input_variable, self.__variable_type_from_var_list(api.output_var_list))
        http_function += function_space(2) + 'm{0}Response'.format(api.function_name) + ' = response;\n'
        for variable in api.input_var_list:
            if variable.var_type == VarType.cpp_enum:
                http_function += function_space(2) + 'int {0} = {1}.getValue();\n'\
                    .format(variable.name_str + "_int", variable.name_str)
            if variable.var_type == VarType.cpp_object:
                http_function += function_space(2) + 'long {0} = {1}.getNativeHandler();\n'\
                    .format(variable.name_str + '_handler', variable.name_str)
            if variable.var_type == VarType.cpp_object_array:
                http_function += function_space(2) + 'long[] {0} = new long[{1}.size()];\n'\
                    .format(variable.name_str + '_handler', variable.name_str)
                http_function += function_space(2) + 'for (int i = 0; i < {0}.size(); i++){{\n'.format(variable.name_str)
                http_function += function_space(3) + '{0}[i] = {1}.get(i).getNativeHandler();\n'\
                    .format(variable.name_str + '_handler', variable.name_str)
                http_function += function_space(2) + '}'
        input_variable_call = self.__input_variable_call(api.input_var_list)
        http_function += function_space(2) + 'native{0}(mNativeHandler{1});\n'\
            .format(api.function_name, input_variable_call)
        http_function += function_space(1) + "}"
        return http_function

    def __http_function_response(self, api):
        http_function_response = function_space(1) + 'public void on{0}(boolean success, String error{1}){{\n'\
            .format(api.function_name, self.__output_variable_declaration(api.output_var_list))
        http_function_response += function_space(2) + 'if (m{0}Response == null){{\n'.format(api.function_name)
        http_function_response += function_space(3) + 'return;\n'
        http_function_response += function_space(2) + '}\n'
        http_function_response += function_space(2) + 'if (success){\n'
        for variable in api.output_var_list:
            if variable.var_type == VarType.cpp_enum:
                http_function_response += function_space(2) + '{0}.{1} {2} = {0}.{1}.get{1}ByValue({3});\n'\
                    .format(self.object_name, variable.var_type.to_java_getter_setter_string(), variable.name_str,
                            variable.name_str + '_int')
            if variable.var_type == VarType.cpp_object:
                http_function_response += function_space(2) + '{0} {1} = new {0}({1}_handler);\n'\
                    .format(variable.var_type, variable.name_str)
            if variable.var_type == VarType.cpp_object_array:
                http_function_response += function_space(2) + 'List<{0}> {1} = new ArrayList<>();\n'\
                    .format(variable.var_type, variable.name_str)
                http_function_response += function_space(2) + 'for (long handler : {0}_handler){{\n'\
                    .format(variable.name_str)
                http_function_response += function_space(3) + '{0}.add(new {1}(handler));\n'\
                    .format(variable.name_str, self.object_name)
                http_function_response += function_space(2) + '}\n'

        http_function_response += function_space(3) + 'm{0}Response.onSuccess({1});\n'\
            .format(api.function_name, self.__output_variable_call(api.output_var_list))
        http_function_response += function_space(2) + '} else {\n'
        http_function_response += function_space(3) + 'm{0}Response.onFailure(error);\n'.format(api.function_name)
        http_function_response += function_space(2) + '}\n'
        http_function_response += function_space(1) + '}'

        return http_function_response

    def generate_http_function_native(self):
        http_native_function = ''
        for api in self.apis:
            http_native_function += function_space(1) + 'private native void native{0}(long handler, {1});\n\n'\
                .format(api.function_name, self.__input_variable_declarations_native(api.input_var_list)[:-2])
        return http_native_function

    def __variable_type_from_var_list(self, var_list):
        if len(var_list) == 0:
            variable_type = 'WebApiResponse '
        elif len(var_list) == 1:
            if var_list[0].var_type == VarType.cpp_object:
                variable_type = 'WebApiWithCoreObjectResponse '
            elif var_list[0].var_type == VarType.cpp_object_array:
                variable_type = 'WebApiWithListResponse '
            else:
                variable_type = '/*TODO .....*/WebApiResponse '
        else:
            variable_type = '/*TODO .....*/WebApiResponse '
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
                vars_declarations += self.object_name + '.' + var.var_type.to_java_getter_setter_string()\
                                     + ' ' + var.name_str + ', '
            else:
                vars_declarations += var.var_type.to_java_getter_setter_string() + ' ' + var.name_str + ', '
        return vars_declarations

    def __output_variable_declaration(self, var_list):
        vars_declarations = ''
        for var in var_list:
            if var.var_type == VarType.cpp_enum:
                vars_declarations += ', int ' + var.name_str + '_int'
            elif var.var_type == VarType.cpp_object:
                vars_declarations += ', long' + var.name_str + '_handler'
            elif var.var_type == VarType.cpp_object_array:
                vars_declarations += ', long[]' + var.name_str + '_handler'
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
                vars_declarations += 'int ' + var.name_str + '_int, '
            elif var.var_type == VarType.cpp_object:
                vars_declarations += 'long ' + var.name_str + '_handler, '
            elif var.var_type == VarType.cpp_object_array:
                vars_declarations += 'long[] ' + var.name_str + '_handler, '
            else:
                vars_declarations += var.var_type.to_java_getter_setter_string() + ' ' + var.name_str + ', '
        return vars_declarations

    # returns "ById(String id)" or "(String id, String username)" or "()"
    def __convert_bys_to_string(self, by_string_list, is_native_declaration, is_native_call):
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
        for java_var in self.java_variable_list:
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

    def __rename_object_name_if_list(self):
        new_object_name = ''
        if self.object_name == 'List':
            new_object_name = 'com.lesschat.core.task.List'
        else:
            new_object_name = self.object_name
        return new_object_name

    def __to_object_name_java_style(self):
        new_object_name = ''
        new_object_name = self.object_name[0].lower() + self.object_name[1:]
        return new_object_name
