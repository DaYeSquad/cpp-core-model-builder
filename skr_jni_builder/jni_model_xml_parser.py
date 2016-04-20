#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - Frank Lin

import xml.etree.ElementTree

from skrutil import io_utils

from jni_variable import JniVariable
from jni_manager import JniManager
from skr_jni_builder.jni_manager import JniManagerSaveCommand
from skr_jni_builder.jni_manager import JniManagerFetchCommand
from skr_jni_builder.jni_manager import JniManagerDeleteCommand
from skr_jni_builder.jni_manager import JniApiDescription

from jni_class import JniClass


class JniModelXmlParser:
    """Parse XML file and generates related JNI files. Pairs with <JavaModelXmlParser>.
    """
    def __init__(self, version):
        self.__version = version

    def parse(self, directory, config):
        """Parses module XML file and gets code for JNI implementation.

        Args:
            directory: The directory which is full path of XML file.
            config: A <Config> object describes user-defined names.

        Returns:
            A string which is JNI implementation.
        """
        # create core folder if not exists and remove last build
        jni_dir_path = 'build/jni'
        io_utils.make_directory_if_not_exists(jni_dir_path)

        # start parsing xml
        e = xml.etree.ElementTree.parse(directory)
        root = e.getroot()

        # search directories
        for folder_node in root.findall('group'):
            group_name = folder_node.get('name')

            # search classes
            for class_node in folder_node.findall('class'):
                class_name = class_node.get('name')

                print 'Find class {0} under "{1}" group'.format(class_name, group_name)

                # parse all <variable/>
                jni_var_list = []
                for variable in class_node.findall('variable'):
                    variable_name = variable.get('name')
                    variable_type = variable.get('type')
                    variable_enum_or_none = variable.get('enum')

                    jni_var = JniVariable(variable_name, variable_type, group_name, class_name)
                    jni_var.set_enum_class_name(variable_enum_or_none)
                    jni_var_list.append(jni_var)

                # parse <manager/>
                jni_manager = None
                manager_or_none = class_node.find('manager')
                if manager_or_none is not None:
                    manager_name = manager_or_none.get('name')
                    jni_manager = JniManager(manager_name)

                    # parse all <save/>
                    for save_node in manager_or_none.findall('save'):
                        is_plural = False
                        plural_node = save_node.get('plural')
                        if plural_node is not None:
                            is_plural = True
                        save_command = JniManagerSaveCommand(is_plural)
                        jni_manager.add_save_command(save_command)

                    # parse all <delete/>
                    for delete_node in manager_or_none.findall('delete'):
                        is_plural = False
                        plural_node = delete_node.get('plural')
                        if plural_node is not None:
                            is_plural = True

                        by = delete_node.get('by')
                        delete_command = JniManagerDeleteCommand(is_plural, by)
                        jni_manager.add_delete_command(delete_command)

                    # parse all <fetch/>
                    for fetch_node in manager_or_none.findall('fetch'):
                        is_plural = False

                        is_plural_attr = fetch_node.get('plural')
                        if is_plural_attr == 'true':
                            is_plural = True

                        by = fetch_node.get('by')
                        alias = fetch_node.get('alias')
                        fetch_command = JniManagerFetchCommand(is_plural, by, alias)
                        jni_manager.add_fetch_command(fetch_command)

                    for fetch_node in manager_or_none.findall('fetches'):
                        is_plural = True
                        by = fetch_node.get('by')
                        alias = fetch_node.get('alias')
                        fetch_command = JniManagerFetchCommand(is_plural, by, alias)
                        jni_manager.add_fetch_command(fetch_command)

                    # parse all <api/>
                    for api_node in manager_or_none.findall('api'):
                        api_function_name = api_node.get('name')
                        function_name = api_node.get('alias')

                        input_var_list = []
                        inputs_node = api_node.find('inputs')
                        for variable_node in inputs_node.findall('variable'):
                            var_name = variable_node.get('name')
                            var_type_string = variable_node.get('type')
                            var_enum_or_none = variable_node.get('enum')

                            var = JniVariable(var_name, var_type_string, group_name, class_name)
                            var.set_enum_class_name(var_enum_or_none)

                            input_var_list.append(var)

                        output_var_list = []
                        outputs_node = api_node.find('outputs')
                        for variable_node in outputs_node.findall('variable'):
                            var_name = variable_node.get('name')
                            var_type_string = variable_node.get('type')
                            var_enum_or_none = variable_node.get('enum')

                            var = JniVariable(var_name, var_type_string, group_name, class_name)
                            var.set_enum_class_name(var_enum_or_none)

                            output_var_list.append(var)

                        api = JniApiDescription(function_name, input_var_list, output_var_list)
                        jni_manager.add_api_description(api)

                jni_wrapper = JniClass(group_name, class_name, jni_var_list, jni_manager)
                if self.__version < 5.0:
                    # write jni wrapper header
                    jni_wrapper.generate_header()

                    # write jni wrapper implementation
                    jni_wrapper.generate_implementation()

                    # write jni wrapper manager header
                    jni_wrapper.generate_manager_header()

                    # write jni wrapper manager implementation
                    jni_wrapper.generate_manager_implementation()
                else:
                    # write jni helper implementation
                    jni_wrapper.generate_jni_helper_implementation(config)

                    # write jni wrapper manager implementation
                    jni_wrapper.generate_manager_implementation(self.__version, config)
