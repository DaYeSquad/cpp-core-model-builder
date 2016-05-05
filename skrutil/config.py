#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - Frank Lin

import xml.etree.ElementTree

from skr_logger import skr_log_warning


class Config:
    """Config will parse xml file in config folder, the default file is 'lesschat.precfg.xml'.
    """

    def __init__(self, config_path):
        """Init config with config xml path.

        Args:
            config_path: A string which is config xml path.
        """
        self.__config_path = config_path

        self.__cpp_namespace = ''
        self.__cpp_ns_begin = ''
        self.__cpp_ns_end = ''
        self.__module_name = ''
        self.__cpp_error_type = 'const std::string&'

        self.__java_package_name = ''
        self.__java_base_object = ''

        self.__objc_prefix = 'LCC'

        self.__parse()

    def __parse(self):
        e = xml.etree.ElementTree.parse(self.__config_path)
        root = e.getroot()

        # parse C++ necessary parameters
        cpp_node = root.find('cpp')
        if cpp_node is not None:
            self.__cpp_namespace = cpp_node.find('namespace').text
            self.__cpp_ns_begin = cpp_node.find('ns_begin').text
            self.__cpp_ns_end = cpp_node.find('ns_end').text
            self.__module_name = cpp_node.find('module_name').text
            self.__cpp_error_type = cpp_node.find('api_error_type').text

            # validate
            if self.__cpp_namespace == '' \
                    or self.__cpp_ns_begin == '' \
                    or self.__cpp_ns_end == '' \
                    or self.__module_name == '':
                skr_log_warning('Invalid config file. Reason : necessary tags not found.')
                return
        else:
            skr_log_warning('Invalid config file. Reason : <cpp> not found.')
            return

        # parse Java necessary parameters
        java_node = root.find('java')
        if java_node is not None:
            self.__java_package_name = java_node.find('package').text
            self.__java_base_object = java_node.find('base_object').text
        else:
            skr_log_warning('Invalid config file. Reason : <java/> not found.')
            return

        # parse Objective-C++ necessary parameters
        apple_node = root.find('apple')
        if apple_node is not None:
            self.__objc_prefix = apple_node.find('prefix').text
        else:
            skr_log_warning('Invalid config file. Reason : <apple/> not found.')
            return

    @property
    def cpp_namespace(self):
        return self.__cpp_namespace

    @property
    def cpp_ns_begin(self):
        return self.__cpp_ns_begin

    @property
    def cpp_ns_end(self):
        return self.__cpp_ns_end

    @property
    def cpp_module_name(self):
        return self.__module_name

    @property
    def cpp_error_type(self):
        return self.__cpp_error_type

    @property
    def java_package_name(self):
        return self.__java_package_name

    @property
    def java_package_path(self):
        return self.__java_package_name.replace('.', '/')

    @property
    def java_base_object(self):
        return self.__java_base_object

    @property
    def jni_package_path(self):
        return self.__java_package_name.replace('.', '_')

    @property
    def objc_prefix(self):
        return self.__objc_prefix
