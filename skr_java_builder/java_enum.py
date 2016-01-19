_JAVA_BR = '\n\n'
_JAVA_SPACE = '    '


def function_space(count):
    space = ''
    for i in range(1, count + 1):
        space += _JAVA_SPACE
    return space


class JavaEnum:
    def __init__(self, enum_class_name):
        self.enum_class_name = enum_class_name
        self.int_alias_tuple_list = []

    def append(self, int_value, alias):
        self.int_alias_tuple_list.append((int_value, alias))

    def generate_java_enum(self, pre_spaces):
        java_enum = ''
        java_enum += '{0}public enum {1} {{\n'.format(pre_spaces, self.enum_class_name)
        enum_count = 0
        for int_alias_tuple in self.int_alias_tuple_list:
            java_enum += _JAVA_SPACE + '{0}{1}   ({2})'.format(pre_spaces,
                                                               int_alias_tuple[1],
                                                               int_alias_tuple[0])

            if enum_count < len(self.int_alias_tuple_list) - 1:
                enum_count += 1
                java_enum += ",\n"
            else:
                java_enum += ";" + _JAVA_BR

        enum_class_instance = self.enum_class_name.lower()

        java_enum += function_space(2) + self.enum_class_name + '(int i) {value = i;}' + _JAVA_BR
        java_enum += function_space(2) + 'int value;' + _JAVA_BR
        java_enum += function_space(2) + 'public int getValue() { return value; }' + _JAVA_BR
        java_enum \
            += function_space(2) + 'public static {0} get{0}ByValue(int value) {{'.format(self.enum_class_name) + "\n"
        java_enum \
            += function_space(3) + '{0}[] {1}s = {2}.values();\n'\
            .format(self.enum_class_name, enum_class_instance, self.enum_class_name)
        java_enum \
            += function_space(4) + 'for ({0} {1}: {2}s) {{\n'\
            .format(self.enum_class_name, enum_class_instance, enum_class_instance)
        java_enum \
            += function_space(4) + 'if ({0}.getValue() == value) {{\n'.format(enum_class_instance)
        java_enum += function_space(5) + 'return {0};\n'.format(enum_class_instance)
        java_enum += function_space(4) + '}\n'
        java_enum += function_space(3) + '}\n'
        java_enum += function_space(3) + 'return {0}.{1};\n'\
            .format(self.enum_class_name, self.int_alias_tuple_list[0][1])
        java_enum += function_space(2) + '}\n'
        java_enum += function_space(1) + '}\n'
        return java_enum
