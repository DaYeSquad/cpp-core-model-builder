#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - Frank Lin

from skr_cpp_builder.cpp_variable import VarType
from skrutil import string_utils


_OBJC_BR = '\n\n'
_OBJC_SPACE = '  '


class ObjcVariable:
    """Represents Objective-C++ property by parsing <variable/>.
    """

    def __init__(self, name, var_type_string):
        self.name = name
        self.var_type = VarType.instance_from_string(var_type_string)

    def set_enum_class_name(self, enum_class_name):
        self.var_type.set_enum_class_name(enum_class_name)

    def __objc_name(self):
        return string_utils.to_objc_property_name(self.name)

    def property(self, config):
        """Returns Objective-C++ property declaration.

        Args:
            config: A <Config> object user-defined

        Returns:

        """
        if self.var_type == VarType.cpp_bool:
            return '@property (nonatomic, getter=is{1}) BOOL {0};'\
                .format(self.__objc_name(), string_utils.first_char_to_upper(self.__objc_name()))
        elif self.var_type == VarType.cpp_string or self.var_type == VarType.cpp_string_array:
            return '@property (nonatomic, copy) {0}{1};'.format(self.var_type.to_objc_getter_string(config),
                                                                self.__objc_name())
        else:
            return '@property (nonatomic) {0} {1};'.format(self.var_type.to_objc_getter_string(config),
                                                           self.__objc_name())

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
            impl = '-(NSArray<NSString *> *){0} {{\n'.format(self.__objc_name())
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
            impl = '-(void)set{0}:(NSString *){1} {{\n'.format(string_utils.first_char_to_upper(self.__objc_name()),
                                                               self.__objc_name())
            impl += _OBJC_SPACE
            impl += '_coreHandle->set_{0}([{1} UTF8String]);\n'.format(self.name, self.__objc_name())
            impl += '}'
            return impl
        elif self.var_type == VarType.cpp_string_array:
            impl = '-(void)set{0}:(NSArray<NSString *> *){1} {{\n'.format(string_utils.first_char_to_upper(self.__objc_name()), self.__objc_name())
            impl += _OBJC_SPACE
            impl += '_coreHandle->set_{0}([LCCObjcAdapter stringVectorsFromArrayOfNSString:{1}]);\n'.format(self.name, self.__objc_name())
            impl += '}'
            return impl
        else:
            impl = '-(void)set{1}:({0}){2} {{\n'\
                .format(self.var_type.to_objc_getter_string(),
                        string_utils.first_char_to_upper(self.__objc_name()),
                        self.__objc_name())
            impl += _OBJC_SPACE

            var_type_str = ''
            if self.var_type == VarType.cpp_int:
                var_type_str += '(int)'
            elif self.var_type == VarType.cpp_enum:
                var_type_str += '(lesschat::{0})'.format(self.var_type.cpp_enum_type_string())

            impl += '_coreHandle->set_{0}({1}{2});\n'.format(self.name, var_type_str, self.__objc_name())
            impl += '}'
            return impl

    def parameter(self):
        return '{0}:({1}){0}'.format(self.__objc_name(), self.var_type.to_objc_getter_string())

    # [id UTF8String] or (int)aFloat
    def cast_to_cpp_parameter(self):
        if self.var_type == VarType.cpp_string:
            return '[{0} UTF8String]'.format(self.__objc_name())
        elif self.var_type == VarType.cpp_string_array:
            return '[LCCObjcAdapter stringVectorsFromArrayOfNSString:{0}]'.format(self.__objc_name())
        elif self.var_type == VarType.cpp_enum:
            return '(lesschat::{0}){1}'.format(self.var_type.cpp_enum_type_string(), self.__objc_name())
        elif self.var_type == VarType.cpp_int:
            return '(int){0}'.format(self.__objc_name())
        elif self.var_type == VarType.cpp_bool:
            return self.__objc_name()
        else:
            return '({0}){1}'.format(self.var_type.to_getter_string(), self.__objc_name())

    # from std::vector<std::unique_ptr<Calendar>> to std::vector<std::unique_ptr<lesschat::Calendar>>, (Array also is)
    def objc_wrapper_from_cpp_parameter(self):
        if self.var_type == VarType.cpp_object_array:
            return 'std::vector<std::unique_ptr<lesschat::{0}>> core{1}'.format(self.var_type.object_class_name, string_utils.to_title_style_name(self.name))
        elif self.var_type == VarType.cpp_object:
            return 'std::unique_ptr<lesschat::{0}> core{0}'.format(self.var_type.object_class_name, string_utils.to_title_style_name(self.name))
        else:
            return '{0} {1}'.format(self.var_type.to_getter_string(), self.name)

    # from 'display_name' to 'DisplayName'
    def to_title_style_name(self):
        return string_utils.to_title_style_name(self.name)

    # from coreCalendar to LCCCallendar *calendar = [LCCCalendar calendarWithCoreCalendar:coreCalendar]; (Objc Array also is)
    def objc_form_cpp_parameter(self, indent):
        objc_code = ''
        if self.var_type == VarType.cpp_object_array:
            objc_code += string_utils.indent(indent)
            objc_code += 'NSMutableArray *{0} = [NSMutableArray array];\n'.format(self.__objc_name())
            objc_code += string_utils.indent(indent)
            objc_code += 'for (auto it = core{0}.begin(); it != core{0}.end(); ++it) {{\n'.format(self.to_title_style_name())
            objc_code += string_utils.indent(2 + indent)
            objc_code += '[{0} addObject:[LCC{1} {2}WithCore{1}:**it]];\n'.format(self.__objc_name(), self.var_type.object_class_name, string_utils.first_char_to_lower(self.var_type.object_class_name))
            objc_code += string_utils.indent(indent)
            objc_code += '}'
        elif self.var_type == VarType.cpp_object:
            objc_code += string_utils.indent(indent)
            objc_code += 'LCC{0} *{1} = [LCC{0} {1}WithCore{0}:*core{0}];'.format(self.var_type.object_class_name, self.__objc_name())
        return objc_code