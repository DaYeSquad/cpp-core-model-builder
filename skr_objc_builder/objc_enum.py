from skrutil import string_utils


_CPP_BR = '\n\n'
_OBJC_SPACE = '  '


class ObjcEnum:

    def __init__(self, enum_class_name):
        self.enum_class_name = enum_class_name
        self.int_alias_tuple_list = []

    def append(self, int_value, alias):
        self.int_alias_tuple_list.append((int_value, alias))

    def generate_objc_enum(self, class_name):
        objc_enum = ''
        objc_enum += 'typedef NS_ENUM(NSUInteger, LCC{0}{1}) {{\n'\
            .format(class_name, self.enum_class_name)
        for int_alias_tuple in self.int_alias_tuple_list:
            objc_enum += _OBJC_SPACE + 'LCC{2}{3}{0} = {1},\n'\
                .format(string_utils.cpp_enum_class_name_to_objc_enum_class_name(int_alias_tuple[1]),
                        int_alias_tuple[0],
                        class_name,
                        self.enum_class_name)
        objc_enum += '};\n'
        return objc_enum
