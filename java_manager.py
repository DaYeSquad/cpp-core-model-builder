import re
from java_variable import VarType
from skr_logger import skr_log_warning

_JAVA_BR = '\n\n'
_JAVA_SPACE = '    '


def function_space(count):
    space = ''
    for i in range(1, count + 1):
        space += _JAVA_SPACE
    return space


class JavaManagerFetchCommand:
    def __init__(self, is_plural, where):
        self.is_plural = is_plural
        if where is not None:
            self.where = where
        else:
            self.where = ''


class JavaManager:
    def __init__(self, manager_name):
        self.manager_name = manager_name
        self.object_name = ''
        self.plural_object_name = ''
        self.java_variable_list = []
        self.fetch_commands = []

    def set_object_name(self, class_name, plural_class_name):
        self.object_name = class_name
        self.plural_object_name = plural_class_name

    def set_java_variable_list(self, java_variable_list):
        self.java_variable_list = java_variable_list

    def add_fetch_command(self, fetch_command):
        self.fetch_commands.append(fetch_command)

    def generate_fetch(self):
        fetch_function = ''
        for fetch_command in self.fetch_commands:
            by_list = []
            if fetch_command.where != '':
                by_list = re.split(',', fetch_command.where)

            if not fetch_command.is_plural:
                if len(by_list) == 0:
                    skr_log_warning('Singular often comes with at least one by parameter')
                fetch_function += function_space(1) + 'public {0} fetch{0}FromCache{1} {{\n' \
                    .format(self.object_name, self.__convert_bys_to_string(by_list, False, False))
                fetch_function += function_space(2) + 'long handler = nativeFetch{0}FromCache{1};\n\n' \
                    .format(self.object_name, self.__convert_bys_to_string(by_list, False, True))
                fetch_function += function_space(2) + 'if (handler == JniHelper.sNullPointer) {\n'
                fetch_function += function_space(3) + 'return null;\n'
                fetch_function += function_space(2) + '}\n\n'
                fetch_function += function_space(2) + 'return new {0}(handler);\n'.format(self.object_name)
                fetch_function += function_space(1) + '}' + _JAVA_BR
            else:
                fetch_function += function_space(1) + 'public List<{0}> fetch{1}FromCache{2} {{\n' \
                    .format(self.object_name, self.plural_object_name,
                            self.__convert_bys_to_string(by_list, False, False))
                fetch_function += function_space(2) + 'long[] handlers = nativeFetch{0}FromCache{1};\n\n'\
                    .format(self.plural_object_name, self.__convert_bys_to_string(by_list, False, True))
                fetch_function += function_space(2) + 'List<{0}> {1} = new ArrayList<>();\n'\
                    .format(self.object_name, self.object_name.lower() + 's')
                fetch_function += function_space(2) + 'for (long handler: handlers) {\n'
                fetch_function += function_space(3) + '{0}.add(new {1}(handler));\n'\
                    .format(self.object_name.lower() + 's', self.object_name)
                fetch_function += function_space(2) + '}\n\n'
                fetch_function += function_space(2) + 'return {0};\n'\
                    .format(self.object_name.lower() + 's')
                fetch_function += function_space(1) + '}' + _JAVA_BR
        return fetch_function

    def generate_fetch_native(self):
        fetch_function = ''
        for fetch_command in self.fetch_commands:
            by_list = []
            if fetch_command.where != '':
                by_list = re.split(',', fetch_command.where)

            if not fetch_command.is_plural:
                if len(by_list) == 0:
                    skr_log_warning('Singular often comes with at least one by parameter')
                fetch_function += function_space(1) + 'private native {0} nativeFetch{0}FromCache{1};'\
                    .format(self.object_name, self.__convert_bys_to_string(by_list, True, False)) + _JAVA_BR
            else:
                fetch_function += function_space(1) + 'private native long[] nativeFetch{0}FromCache{1};'\
                    .format(self.plural_object_name, self.__convert_bys_to_string(by_list, True, False)) + _JAVA_BR
        return fetch_function

    # returns "ById(String id)" or "(String id, String username)" or "()"
    def __convert_bys_to_string(self, by_string_list, is_native_declaration, is_native_call):
        if len(by_string_list) == 0:  # ()
            return '()'
        elif len(by_string_list) == 1:  # "ById(String id)"
            by_string = by_string_list[0]
            java_var = self.__java_var_by_name(by_string)
            if java_var is not None:
                if is_native_declaration:
                    if java_var.var_type == VarType.java_enum:
                        return 'By{0}(long handler, {1} {2})'.format(java_var.get_set_name_str, 'int',
                                                                     java_var.name_str)
                    elif java_var.var_type == VarType.java_string_array:
                        return 'By{0}(long handler, {1} {2})'.format(java_var.get_set_name_str, 'String[]',
                                                                     java_var.name_str)
                    return 'By{0}(long handler, {1} {2})'.format(java_var.get_set_name_str,
                                                                 java_var.var_type.to_getter_setter_string(),
                                                                 java_var.name_str)
                elif is_native_call:
                    if java_var.var_type == VarType.java_enum:
                        return 'By{0}(mNativeHandler, {1}.getValue())'.format(java_var.get_set_name_str, java_var.name_str)
                    elif java_var.var_type == VarType.java_string_array:
                        return 'By{0}(mNativeHandler, new String[{1}.size()])'.format(java_var.get_set_name_str, java_var.name_str)
                    return 'By{0}(mNativeHandler, {1})'.format(java_var.get_set_name_str, java_var.name_str)
                else:
                    if java_var.var_type == VarType.java_enum:
                        return 'By{0}({1} {2})'.format(java_var.get_set_name_str, java_var.java_enum, java_var.name_str)
                    return 'By{0}({1} {2})'.format(java_var.get_set_name_str,
                                                   java_var.var_type.to_getter_setter_string(), java_var.name_str)
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
                        if java_var.var_type == VarType.java_enum:
                            bys_string += '{0} {1}, '.format('int', java_var.name_str)
                        elif java_var.var_type == VarType.java_string_array:
                            bys_string += '{0} {1}, '.format('String[]', java_var.name_str)
                        else:
                            bys_string += '{0} {1}, '.format(java_var.var_type.to_getter_setter_string(),
                                                             java_var.name_str)
                    elif is_native_call:
                        if index == 0:
                            bys_string += 'mNativeHandler, '
                        if java_var.var_type == VarType.java_enum:
                            bys_string += '{0}.getValue(), '.format(java_var.name_str)
                        elif java_var.var_type == VarType.java_string_array:
                            bys_string += 'new String[{0}.size()], '.format(java_var.name_str)
                        else:
                            bys_string += '{0}, '.format(java_var.name_str)
                    else:
                        if java_var.var_type == VarType.java_enum:
                            bys_string += '{0} {1}, '.format(java_var.java_enum, java_var.name_str)
                        else:
                            bys_string += '{0} {1}, '.format(java_var.var_type.to_getter_setter_string(),
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
