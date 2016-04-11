import xml.etree.ElementTree

from skrutil import io_utils
from skrutil import string_utils

from skr_cpp_builder.cpp_manager import CppManagerSaveCommand
from skr_cpp_builder.cpp_manager import CppManagerFetchCommand
from skr_cpp_builder.cpp_manager import CppManagerDeleteCommand
from skr_cpp_builder.cpp_manager import CppApiDescription

from objc_class import ObjcClass
from objc_variable import ObjcVariable
from objc_enum import ObjcEnum
from objc_manager import ObjcManager


class ObjcModelXmlParser:

    def __init__(self, version):
        self.version = version

    def parse(self, directory):
        # create core folder if not exists and remove last build
        objc_dir_path = 'build/ObjectiveCppWrapper'
        io_utils.make_directory_if_not_exists(objc_dir_path)

        # start parsing xml
        e = xml.etree.ElementTree.parse(directory)
        root = e.getroot()

        # search directories
        for folder_node in root.findall('group'):
            group_name = folder_node.get('name')
            objc_group_name = 'build/ObjectiveCppWrapper/' + string_utils.cpp_group_name_to_objc_group_name(group_name)
            io_utils.make_directory_if_not_exists(objc_group_name)

            # search classes
            for class_node in folder_node.findall('class'):
                class_name = class_node.get('name')

                print 'Find objc class {0} under "{1}" group'.format(class_name, group_name)

                # parse all <enum/>
                objc_enum_list = []
                for enum in class_node.findall('enum'):
                    enum_name = enum.get('name')
                    objc_enum = ObjcEnum(enum_name)
                    for enum_value in enum.findall('value'):
                        int_value = enum_value.get('int_value')
                        alias = enum_value.get('alias')
                        objc_enum.append(int_value, alias)
                    objc_enum_list.append(objc_enum)

                # parse all <variable/>
                objc_var_list = []
                for variable in class_node.findall('variable'):
                    variable_name = variable.get('name')
                    variable_type = variable.get('type')
                    variable_enum_or_none = variable.get('enum')

                    objc_var = ObjcVariable(variable_name, variable_type)
                    objc_var.set_enum_class_name(variable_enum_or_none)
                    objc_var_list.append(objc_var)

                # parse <manager/>
                objc_manager = None
                manager_or_none = class_node.find('manager')
                if manager_or_none is not None:
                    manager_name = manager_or_none.get('name')
                    objc_manager = ObjcManager(manager_name)

                    # parse all <save/>
                    for save_node in manager_or_none.findall('save'):
                        is_plural = False
                        plural_node = save_node.get('plural')
                        if plural_node is not None:
                            is_plural = True
                        alias_attr = save_node.get('alias')
                        save_command = CppManagerSaveCommand(is_plural, [], alias_attr)
                        objc_manager.add_save_command(save_command)

                    # parse all <delete/>
                    for delete_node in manager_or_none.findall('delete'):
                        is_plural = False
                        plural_node = delete_node.get('plural')
                        if plural_node is not None:
                            is_plural = True

                        by = delete_node.get('by')
                        alias_attr = delete_node.get('alias')
                        delete_command = CppManagerDeleteCommand(is_plural, by, [], alias_attr)
                        objc_manager.add_delete_command(delete_command)

                    # parse all <fetch/>
                    for fetch_node in manager_or_none.findall('fetch'):
                        is_plural = False
                        plural_node = fetch_node.get('plural')
                        if plural_node is not None:
                            is_plural = True

                        by = fetch_node.get('by')
                        sort_by_or_none = fetch_node.get('sort')
                        is_asc = True
                        if sort_by_or_none is not None:
                            desc_desciption_or_none = fetch_node.get('desc')
                            if desc_desciption_or_none is not None:
                                if desc_desciption_or_none == 'true':
                                    is_asc = False
                        alias_attr = fetch_node.get('alias')
                        fetch_command = CppManagerFetchCommand(is_plural, by, sort_by_or_none, is_asc, [], alias_attr)
                        objc_manager.add_fetch_command(fetch_command)

                    # parse all <api/>
                    for api_node in manager_or_none.findall('api'):                        
                        api_name = api_node.get('name')
                        api_alias = api_node.get('alias')
                        api_method = api_node.get('method')
                        api_uri = api_node.get('uri')

                        input_var_list = []
                        inputs_node = api_node.find('inputs')
                        for variable_node in inputs_node.findall('variable'):
                            var_name = variable_node.get('name')
                            var_type_string = variable_node.get('type')
                            var_enum_or_none = variable_node.get('enum')

                            var = ObjcVariable(var_name, var_type_string)
                            var.set_enum_class_name(var_enum_or_none)

                            input_var_list.append(var)

                        output_var_list = []
                        outputs_node = api_node.find('outputs')
                        for variable_node in outputs_node.findall('variable'):
                            var_name = variable_node.get('name')
                            var_type_string = variable_node.get('type')
                            var_enum_or_none = variable_node.get('enum')

                            var = ObjcVariable(var_name, var_type_string)
                            var.set_enum_class_name(var_enum_or_none)

                            output_var_list.append(var)

                        api = CppApiDescription(api_name, api_alias, api_method, api_uri, input_var_list, output_var_list, [])
                        objc_manager.add_api_description(api)

                # write objective-c++ wrapper core addition header
                objc_wrapper = ObjcClass(group_name, class_name, objc_var_list, objc_enum_list, objc_manager)
                objc_wrapper.generate_core_addition_header()

                # write objective-c++ wrapper header
                objc_wrapper.generate_header()

                # write objective-c++ wrapper implementation
                objc_wrapper.generate_implementation()

                # write objective-c++ wrapper manager category header
                objc_wrapper.generate_manager_core_addition_header()

                # write objective-c++ wrapper manager header
                objc_wrapper.generate_manager_header()

                # write objective-c++ wrapper manager implementation
                objc_wrapper.generate_manager_implementation()
