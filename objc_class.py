from cpp_class import CppClass
import string_utils


_OBJC_BR = '\n\n'
_OBJC_SPACE = '  '


class ObjcClass:
    def __init__(self, group_name, class_name, objc_variable_list, objc_enum_list, cpp_manager_or_none):
        self.group_name = group_name
        self.class_name = class_name
        self.objc_var_list = objc_variable_list
        self.objc_enum_list = objc_enum_list
        self.cpp_manager_or_none = cpp_manager_or_none

        if self.cpp_manager_or_none is not None:
            self.cpp_manager_or_none.set_object_name(class_name, class_name + 's')
            self.cpp_manager_or_none.set_cpp_variable_list(objc_variable_list)

    def generate_core_addition_header(self):
        file_name = 'LCC{0}_CoreAddition.h'.format(self.class_name)
        file_path = 'ObjectiveCppWrapper/' + string_utils.cpp_group_name_to_objc_group_name(self.group_name) + '/' + file_name
        output_header = open(file_path, 'w')

        output_header.write('#include "{0}.h"'.format(CppClass.convert_class_name_to_file_name(self.class_name)))
        output_header.write(_OBJC_BR)
        output_header.write('@interface LCC{0} () {{'.format(self.class_name))
        output_header.write('\n')
        output_header.write('@package')
        output_header.write('\n')
        output_header.write(_OBJC_SPACE)
        output_header.write('std::unique_ptr<lesschat::{0}> _coreHandle;'.format(self.class_name))
        output_header.write('\n')
        output_header.write('}')
        output_header.write(_OBJC_BR)
        output_header.write('+ (instancetype){0}WithCore{1}:(const lesschat::{1}&)core{1};'
                            .format(string_utils.first_char_to_lower(self.class_name), self.class_name))
        output_header.write(_OBJC_BR)
        output_header.write('@end')

    def generate_header(self):
        file_name = 'LCC{0}.h'.format(self.class_name)
        file_path = 'ObjectiveCppWrapper/' + string_utils.cpp_group_name_to_objc_group_name(self.group_name) + '/' + file_name
        output_header = open(file_path, 'w')

        output_header.write('#import <Foundation/Foundation.h>')
        output_header.write(_OBJC_BR)

        for objc_enum in self.objc_enum_list:
            output_header.write(objc_enum.generate_objc_enum(self.class_name))
            output_header.write(_OBJC_BR)

        output_header.write('NS_ASSUME_NONNULL_BEGIN\n@interface LCC{0} : NSObject'.format(self.class_name))
        output_header.write(_OBJC_BR)

        for objc_var in self.objc_var_list:
            output_header.write(objc_var.property())
            output_header.write(_OBJC_BR)

        output_header.write('@end\nNS_ASSUME_NONNULL_END')
        output_header.write(_OBJC_BR)

    def generate_implementation(self):
        file_name = 'LCC{0}.mm'.format(self.class_name)
        file_path = 'ObjectiveCppWrapper/' + string_utils.cpp_group_name_to_objc_group_name(self.group_name) + '/' + file_name
        output_impl = open(file_path, 'w')

        output_impl.write('#if !defined(__has_feature) || !__has_feature(objc_arc)\n#error "This file requires ARC support."\n#endif')
        output_impl.write(_OBJC_BR)
        output_impl.write('#import "LCC{0}.h"\n#import "LCC{0}_CoreAddition.h"\n\n#import "LCCObjcAdapter.h"'.format(self.class_name))
        output_impl.write(_OBJC_BR)
        output_impl.write('@implementation LCC{0}'.format(self.class_name))
        output_impl.write(_OBJC_BR)
        output_impl.write('#pragma mark - Property')
        output_impl.write(_OBJC_BR)

        for objc_var in self.objc_var_list:
            output_impl.write(objc_var.getter_impl())
            output_impl.write(_OBJC_BR)
            output_impl.write(objc_var.setter_impl())
            output_impl.write(_OBJC_BR)

        output_impl.write('#pragma mark - Core Addition')
        output_impl.write(_OBJC_BR)
        output_impl.write('+ (instancetype){0}WithCore{1}:(const lesschat::{1}&)core{1} {{\n'
                          .format(string_utils.first_char_to_lower(self.class_name), self.class_name))
        output_impl.write(_OBJC_SPACE)
        output_impl.write('LCC{0} *{1} = [[LCC{0} alloc] init];\n'.format(self.class_name, string_utils.first_char_to_lower(self.class_name)))
        output_impl.write(_OBJC_SPACE)
        output_impl.write('{0}->_coreHandle = core{1}.Clone();\n'.format(string_utils.first_char_to_lower(self.class_name), self.class_name))
        output_impl.write(_OBJC_SPACE)
        output_impl.write('return {0};\n}}'.format(string_utils.first_char_to_lower(self.class_name)))
        output_impl.write(_OBJC_BR)
        output_impl.write('@end\n')
