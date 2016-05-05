#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - Frank Lin

from skrutil import string_utils
from skrutil.string_utils import cpp_class_name_to_cpp_file_name


_OBJC_BR = '\n\n'
_OBJC_SPACE = '  '
_OBJC_BUILD_PATH = 'build/ObjectiveCppWrapper/'


class ObjcClass:
    """Responsible for generating Object and Object Manager files.
    """

    def __init__(self, group_name, class_name, objc_variable_list, objc_enum_list, objc_manager_or_none):
        self.group_name = group_name
        self.class_name = class_name
        self.objc_var_list = objc_variable_list
        self.objc_enum_list = objc_enum_list
        self.objc_manager_or_none = objc_manager_or_none

        if self.objc_manager_or_none is not None:
            self.objc_manager_or_none.set_object_name(class_name, class_name + 's')
            self.objc_manager_or_none.set_objc_variable_list(objc_variable_list)

    def generate_core_addition_header(self, config):
        """Generates Objective-C++ private header file. (eg: LCCTopic_CoreAddition.h)

        Args:
            config: A <Config> object represents user-defined configs, in this method, only apple/prefix is used.
        """
        file_name = '{1}{0}_CoreAddition.h'.format(self.class_name, config.objc_prefix)
        file_path = _OBJC_BUILD_PATH + string_utils.cpp_group_name_to_objc_group_name(self.group_name) + '/' + file_name
        output_header = open(file_path, 'w')

        output_header.write('#include "{0}.h"'.format(cpp_class_name_to_cpp_file_name(self.class_name)))
        output_header.write(_OBJC_BR)
        output_header.write('@interface {1}{0} () {{'.format(self.class_name, config.objc_prefix))
        output_header.write('\n')
        output_header.write(' @package')
        output_header.write('\n')
        output_header.write(_OBJC_SPACE)
        output_header.write('std::unique_ptr<{1}::{0}> _coreHandle;'.format(self.class_name, config.cpp_namespace))
        output_header.write('\n')
        output_header.write('}')
        output_header.write(_OBJC_BR)
        output_header.write('+ (instancetype){0}WithCore{1}:(const {2}::{1}&)core{1};'
                            .format(string_utils.first_char_to_lower(self.class_name),
                                    self.class_name,
                                    config.cpp_namespace))
        output_header.write(_OBJC_BR)
        output_header.write('@end')

    def generate_header(self, config):
        """Generates Objective-C++ object header file.

        Args:
            config: A <Config> object represents user-defined configs, in this method, only apple/prefix is used.
        """

        file_name = '{1}{0}.h'.format(self.class_name, config.objc_prefix)
        file_path = _OBJC_BUILD_PATH + string_utils.cpp_group_name_to_objc_group_name(self.group_name) + '/' + file_name
        output_header = open(file_path, 'w')

        output_header.write('#import <Foundation/Foundation.h>')
        output_header.write(_OBJC_BR)

        for objc_enum in self.objc_enum_list:
            output_header.write(objc_enum.generate_objc_enum(self.class_name, config))
            output_header.write(_OBJC_BR)

        output_header.write('NS_ASSUME_NONNULL_BEGIN\n@interface {1}{0} : NSObject'.format(self.class_name,
                                                                                           config.objc_prefix))
        output_header.write(_OBJC_BR)

        for objc_var in self.objc_var_list:
            output_header.write(objc_var.property(config))
            output_header.write(_OBJC_BR)

        output_header.write('@end\nNS_ASSUME_NONNULL_END')
        output_header.write(_OBJC_BR)

    def generate_implementation(self, config):
        """Generates Objective-C++ object header file.

        Args:
            config: A <Config> object represents user-defined configs, in this method, only apple/prefix is used.
        """
        file_name = '{1}{0}.mm'.format(self.class_name, config.objc_prefix)
        file_path = _OBJC_BUILD_PATH + string_utils.cpp_group_name_to_objc_group_name(self.group_name) + '/' + file_name
        output_impl = open(file_path, 'w')

        output_impl.write('#if !defined(__has_feature) || !__has_feature(objc_arc)\n#error "This file requires ARC support."\n#endif')
        output_impl.write(_OBJC_BR)
        output_impl.write('#import "{1}{0}.h"\n#import "{1}{0}_CoreAddition.h"\n\n#import "{1}ObjcAdapter.h"'.format(
            self.class_name, config.objc_prefix))
        output_impl.write(_OBJC_BR)
        output_impl.write('@implementation {1}{0}'.format(self.class_name, config.objc_prefix))
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
        output_impl.write('+ (instancetype){0}WithCore{1}:(const {2}::{1}&)core{1} {{\n'
                          .format(string_utils.first_char_to_lower(self.class_name),
                                  self.class_name, config.cpp_namespace))
        output_impl.write(_OBJC_SPACE)
        output_impl.write('{2}{0} *{1} = [[{2}{0} alloc] init];\n'
                          .format(self.class_name,
                                  string_utils.first_char_to_lower(self.class_name),
                                  config.objc_prefix))
        output_impl.write(_OBJC_SPACE)
        output_impl.write('{0}->_coreHandle = core{1}.Clone();\n'
                          .format(string_utils.first_char_to_lower(self.class_name), self.class_name))
        output_impl.write(_OBJC_SPACE)
        output_impl.write('return {0};\n}}'.format(string_utils.first_char_to_lower(self.class_name)))
        output_impl.write(_OBJC_BR)
        output_impl.write('@end\n')

    def generate_manager_core_addition_header(self, config):
        """Generates Objective-C++ object manager private header file.

        Args:
            config: A <Config> object represents user-defined configs, in this method, only apple/prefix is used.
        """
        file_name = '{1}{0}Manager_CoreAddition.h'.format(self.class_name, config.objc_prefix)
        file_path = _OBJC_BUILD_PATH + string_utils.cpp_group_name_to_objc_group_name(self.group_name) + '/' + file_name
        output_header = open(file_path, 'w')

        output_header.write('#include "{0}_manager.h"\n#include "director.h"'.format(
            string_utils.cpp_class_name_to_cpp_file_name(self.class_name)))
        output_header.write(_OBJC_BR)
        output_header.write('@interface {1}{0}Manager () {{\n @private\n'.format(self.class_name, config.objc_prefix))
        output_header.write(_OBJC_SPACE)
        output_header.write('const {1}::{0}Manager *_coreManagerHandler;\n'.format(self.class_name, config.cpp_namespace))
        output_header.write('}')
        output_header.write(_OBJC_BR)
        output_header.write('@end\n')

    def generate_manager_header(self, config):
        """Generates Objective-C++ object manager header file.

        Args:
            config: A <Config> object represents user-defined configs, in this method, only apple/prefix is used.
        """
        if self.objc_manager_or_none is None:
            return

        objc_manager = self.objc_manager_or_none

        file_name = '{1}{0}Manager.h'.format(self.class_name, config.objc_prefix)
        file_path = _OBJC_BUILD_PATH + string_utils.cpp_group_name_to_objc_group_name(self.group_name) + '/' + file_name
        output_header = open(file_path, 'w')

        output_header.write('#import <Foundation/Foundation.h>')
        output_header.write(_OBJC_BR)
        output_header.write('@class {1}{0};'.format(self.class_name, config.objc_prefix))
        output_header.write(_OBJC_BR)

        output_header.write('NS_ASSUME_NONNULL_BEGIN\n')
        output_header.write('@interface {1}{0}Manager : NSObject'.format(self.class_name, config.objc_prefix))

        output_header.write(_OBJC_BR)
        output_header.write('///-----------------------------------------\n')
        output_header.write('/// @name Lifecycle\n')
        output_header.write('///-----------------------------------------\n')
        output_header.write('\n')

        output_header.write('+ (instancetype)defaultManager;')
        output_header.write(_OBJC_BR)
        output_header.write('///-----------------------------------------\n')
        output_header.write('/// @name HTTP\n')
        output_header.write('///-----------------------------------------\n')
        output_header.write('\n')

        output_header.write(objc_manager.generate_web_api_declarations(config))

        output_header.write('///-----------------------------------------\n')
        output_header.write('/// @name Persistent store\n')
        output_header.write('///-----------------------------------------\n')
        output_header.write('\n')

        output_header.write(objc_manager.generate_fetch_declarations(config))
        output_header.write('@end\nNS_ASSUME_NONNULL_END\n')

    def generate_manager_implementation(self, config):
        """Generates Objective-C++ object manager implementation file.

        Args:
            config: A <Config> object represents user-defined configs, in this method, only apple/prefix is used.
        """
        if self.objc_manager_or_none is None:
            return

        objc_manager = self.objc_manager_or_none

        file_name = '{1}{0}Manager.mm'.format(self.class_name, config.objc_prefix)
        file_path = _OBJC_BUILD_PATH + string_utils.cpp_group_name_to_objc_group_name(self.group_name) + '/' + file_name
        output_impl = open(file_path, 'w')

        output_impl.write('#if !defined(__has_feature) || !__has_feature(objc_arc)\n#error "This file requires ARC support."\n#endif')
        output_impl.write(_OBJC_BR)
        output_impl.write('#import "{1}{0}Manager.h"\n#import "{1}{0}Manager_CoreAddition.h"\n\n'
                          .format(self.class_name, config.objc_prefix))
        output_impl.write('#import "{0}Director.h"\n#import "{0}ObjcAdapter.h"\n#import "{0}Utils.h"\n\n'
                          .format(config.objc_prefix))
        output_impl.write('#import "{1}{0}.h"\n#import "{1}{0}_CoreAddition.h"'.format(self.class_name,
                                                                                       config.objc_prefix))
        output_impl.write(_OBJC_BR)
        output_impl.write('@implementation {1}{0}Manager'.format(self.class_name, config.objc_prefix))
        output_impl.write(_OBJC_BR)
        output_impl.write('#pragma mark - Lifecycle')
        output_impl.write(_OBJC_BR)
        output_impl.write(objc_manager.generate_constructor_implementation(config))
        output_impl.write(_OBJC_BR)
        output_impl.write(objc_manager.generate_default_manager_implementation(config))
        output_impl.write(_OBJC_BR)
        output_impl.write('#pragma mark - HTTP')
        output_impl.write(_OBJC_BR)
        output_impl.write(objc_manager.generate_web_api_implementations(config))
        output_impl.write('#pragma mark - Persistent store')
        output_impl.write(_OBJC_BR)
        output_impl.write(objc_manager.generate_fetch_implementations(config))
        output_impl.write('@end\n')
