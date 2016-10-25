#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - Frank Lin

import xml.etree.ElementTree
import os
import shutil

from java_variable import JavaVariable
from java_class import JavaClass
from java_enum import JavaEnum

from java_manager import JavaManager
from java_manager import JavaManagerFetchCommand
from java_manager import JavaApiDescription


class JavaModelXmlParser:
    """Java file and jni file parser and generator.

    To use:
    >>> java_parser = JavaModelXmlParser(5.0)
    >>> java_parser.parse('directory_to_module_xml_file')
    """

    def __init__(self, version):
        """Init parser and generator with version number.
        Args:
            version: A float that describes version number of module builder, it does not have other usage now.
        """
        self.__version = version

    def parse(self, directory, config):
        """Parse the module XML file and generates the result.

        Args:
            directory: A string represents the absolute path of the directory.
            config: A <
        """
        # create core folder if not exists and remove last build
        core_dir_path = 'build/{0}'.format(config.java_package_path)
        print core_dir_path
        if os.path.exists(core_dir_path):
            shutil.rmtree(core_dir_path)
            os.makedirs(core_dir_path)
        else:
            os.makedirs(core_dir_path)

        # start parsing xml
        e = xml.etree.ElementTree.parse(directory)
        root = e.getroot()

        # search directories
        for folder_node in root.findall('group'):
            group_name = folder_node.get('name')
            group_path = 'build/{0}/'.format(config.java_package_path) + group_name
            if os.path.exists(group_path):
                shutil.rmtree(group_path)
                os.makedirs(group_path)
            else:
                os.makedirs(group_path)

            # search classes
            for class_node in folder_node.findall('class'):
                class_name = class_node.get('name')

                print('Find class {0} under "{1}" group'.format(class_name, group_name))

                # parse all <enum/>
                java_enum_list = []
                for enum in class_node.findall('enum'):
                    enum_name = enum.get('name')
                    java_enum = JavaEnum(enum_name)
                    for enum_value in enum.findall('value'):
                        int_value = enum_value.get('int_value')
                        alias = enum_value.get('alias')
                        java_enum.append(int_value, alias)
                    java_enum_list.append(java_enum)

                # parse all <variable/>
                java_var_list = []
                for variable in class_node.findall('variable'):
                    variable_name = variable.get('name')
                    variable_type = variable.get('type')
                    variable_enum_or_none = variable.get('enum')

                    java_var = JavaVariable(variable_name, variable_type)
                    java_var.set_enum_class_name(variable_enum_or_none)
                    java_var_list.append(java_var)

                # parse <manager/>
                java_manager = None
                manager_or_none = class_node.find('manager')
                if manager_or_none is not None:
                    manager_name = manager_or_none.get('name')
                    java_manager = JavaManager(manager_name)

                    # parse all <fetch/>
                    for fetch_node in manager_or_none.findall('fetch'):
                        is_plural = False

                        # compact with version before 4.0
                        is_plural_attr = fetch_node.get('plural')
                        if is_plural_attr and is_plural_attr == 'true':
                            is_plural = True

                        by = fetch_node.get('by')
                        alias = fetch_node.get('alias')
                        fetch_command = JavaManagerFetchCommand(is_plural, by, alias)
                        java_manager.add_fetch_command(fetch_command)

                    for fetch_node in manager_or_none.findall('fetches'):
                        is_plural = True
                        by = fetch_node.get('by')
                        alias = fetch_node.get('alias')
                        fetch_command = JavaManagerFetchCommand(is_plural, by, alias)
                        java_manager.add_fetch_command(fetch_command)

                    # parse all <api/>
                    for api_node in manager_or_none.findall('api'):
                        function_name = api_node.get('alias')

                        input_var_list = []
                        inputs_node = api_node.find('inputs')
                        for variable_node in inputs_node.findall('variable'):
                            var_name = variable_node.get('name')
                            var_type_string = variable_node.get('type')
                            var_enum_or_none = variable_node.get('enum')

                            var = JavaVariable(var_name, var_type_string)
                            var.set_enum_class_name(var_enum_or_none)

                            input_var_list.append(var)

                        output_var_list = []
                        outputs_node = api_node.find('outputs')
                        for variable_node in outputs_node.findall('variable'):
                            var_name = variable_node.get('name')
                            var_type_string = variable_node.get('type')
                            var_enum_or_none = variable_node.get('enum')

                            var = JavaVariable(var_name, var_type_string)
                            var.set_enum_class_name(var_enum_or_none)

                            output_var_list.append(var)

                        api = JavaApiDescription(function_name, input_var_list, output_var_list)
                        java_manager.add_api_description(api)

                java_class = JavaClass(group_name, class_name, java_var_list, java_enum_list, java_manager)

                if self.__version < 5.0:
                    # Inherit from CoreObject
                    java_class.generate_java()
                    java_class.generate_manager(self.__version)
                else:
                    # Inherit from LessChatObject
                    java_class.generate_java_v2(config)
                    java_class.generate_manager(self.__version, config)
