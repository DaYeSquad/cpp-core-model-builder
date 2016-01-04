from cpp_variable import VarType
import string_utils


_OBJC_BR = '\n\n'
_OBJC_SPACE = '  '


class ObjcVariable:

    def __init__(self, name, var_type_string):
        var_type = VarType.type_from_string(var_type_string)

        self.name = name
        self.var_type = VarType(var_type)

    def set_enum_class_name(self, enum_class_name):
        self.var_type.set_enum_class_name(enum_class_name)

    def __objc_name(self):
        return string_utils.to_objc_property_name(self.name)

    def property(self):
        if self.var_type == VarType.cpp_bool:
            return '@property (nonatomic, getter=is{1}) BOOL {0};'.format(self.__objc_name(), string_utils.first_char_to_upper(self.__objc_name()))
        elif self.var_type == VarType.cpp_string or self.var_type == VarType.cpp_string_array:
            return '@property (nonatomic, copy) {0}{1};'.format(self.var_type.to_objc_getter_string(), self.__objc_name())
        else:
            return '@property (nonatomic) {0} {1};'.format(self.var_type.to_objc_getter_string(), self.__objc_name())

    def getter_impl(self):
        if self.var_type == VarType.cpp_bool:
            impl = '-(BOOL)is{0} {{\n'.format(string_utils.first_char_to_upper(self.__objc_name()))
            impl += _OBJC_SPACE
            impl += 'return _coreHandle->is_{0}();\n'.format(self.name)
            impl += '}'
            return impl
        elif self.var_type == VarType.cpp_string:
            impl = '-(NSString *){0} {{\n'.format(self.__objc_name())
            impl += _OBJC_SPACE
            impl += 'return [NSString stringWithUTF8String:_coreHandle->{0}().c_str()];\n'.format(self.name)
            impl += '}'
            return impl
        elif self.var_type == VarType.cpp_string_array:
            impl = '-(NSString<NSString *> *){0} {{\n'.format(self.__objc_name())
            impl += _OBJC_SPACE
            impl += 'return [LCCObjcAdapter objcArrayOfNSStringFromStringVector:_coreHandle->{0}()];\n'.format(self.name)
            impl += '}'
            return impl
        else:
            impl = '-({0}){1} {{\n'.format(self.var_type.to_objc_getter_string(), self.__objc_name())
            impl += _OBJC_SPACE
            impl += 'return ({0})_coreHandle->{1}();\n'.format(self.var_type.to_objc_getter_string(), self.name)
            impl += '}'
            return impl

    def setter_impl(self):
        if self.var_type == VarType.cpp_string:
            impl = '-(void)set{0}:(NSString *){1} {{\n'.format(string_utils.first_char_to_upper(self.__objc_name()), self.__objc_name())
            impl += _OBJC_SPACE
            impl += '_coreHandle->set_{0}([{1} UTF8String]);\n'.format(self.name, self.__objc_name())
            impl += '}'
            return impl
        elif self.var_type == VarType.cpp_string_array:
            impl = '-(void)set{0}:(NSArray<NSString *> *){1} {{\n'.format(string_utils.first_char_to_upper(self.__objc_name()), self.__objc_name())
            impl += _OBJC_SPACE
            impl += '_coreHandle->set_{0}([LCCObjcAdapter stringVectorsFromArrayOfNSString:{1}];);\n'.format(self.name, self.__objc_name())
            impl += '}'
            return impl
        else:
            impl = '-(void)set{1}:({0}){2} {{\n'\
                .format(self.var_type.to_objc_getter_string(),
                        string_utils.first_char_to_upper(self.__objc_name()),
                        self.__objc_name())
            impl += _OBJC_SPACE
            impl += '_coreHandle->set_{0}(({1}){0});\n'.format(self.name, self.var_type.to_objc_getter_string())
            impl += '}'
            return impl
