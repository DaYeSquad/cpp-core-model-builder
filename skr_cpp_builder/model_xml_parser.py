import xml.etree.ElementTree

from skrutil import io_utils

from cpp_variable import CppVariable
from cpp_class import CppClass
from cpp_enum import CppEnum
from cpp_manager import CppManager
from cpp_manager import CppManagerSaveCommand
from cpp_manager import CppManagerFetchCommand
from cpp_manager import CppManagerDeleteCommand


class CppModelXmlParser:

    def __init__(self, version):
        self.version = version

    def parse(self, directory):
        # create core folder if not exists and remove last build
        core_dir_path = 'build/core'
        io_utils.make_directory_if_not_exists(core_dir_path)

        # start parsing xml
        e = xml.etree.ElementTree.parse(directory)
        root = e.getroot()

        # search directories
        for folder_node in root.findall('group'):
            group_name = folder_node.get('name')
            group_name = 'core/' + group_name
            io_utils.make_directory_if_not_exists('build/{0}'.format(group_name))

            # search classes
            for class_node in folder_node.findall('class'):
                class_name = class_node.get('name')

                print('Find class {0} under "{1}" group'.format(class_name, group_name))

                # parse all <enum/>
                cpp_enum_list = []
                for enum in class_node.findall('enum'):
                    enum_name = enum.get('name')
                    cpp_enum = CppEnum(enum_name)
                    for enum_value in enum.findall('value'):
                        int_value = enum_value.get('int_value')
                        alias = enum_value.get('alias')
                        cpp_enum.append(int_value, alias)
                    cpp_enum_list.append(cpp_enum)

                # parse all <variable/>
                cpp_var_list = []
                for variable in class_node.findall('variable'):
                    variable_name = variable.get('name')
                    variable_type = variable.get('type')
                    variable_json_path = variable.get('json_path')
                    variable_enum_or_none = variable.get('enum')
                    variable_sql_flag = variable.get('sql_flag')
                    variable_json_search_path = variable.get('json_search_path')

                    cpp_var = CppVariable(variable_name, variable_type, variable_json_path, variable_sql_flag)
                    cpp_var.set_enum_class_name(variable_enum_or_none)
                    cpp_var.set_json_search_path(variable_json_search_path)
                    cpp_var_list.append(cpp_var)

                # parse <manager/>
                cpp_manager = None
                manager_or_none = class_node.find('manager')
                if manager_or_none is not None:
                    manager_name = manager_or_none.get('name')
                    cpp_manager = CppManager(manager_name)

                    # parse all <save/>
                    for save_node in manager_or_none.findall('save'):
                        is_plural = False
                        plural_node = save_node.get('plural')
                        if plural_node is not None:
                            is_plural = True
                        save_command = CppManagerSaveCommand(is_plural)
                        cpp_manager.add_save_command(save_command)

                    # parse all <delete/>
                    for delete_node in manager_or_none.findall('delete'):
                        is_plural = False
                        plural_node = delete_node.get('plural')
                        if plural_node is not None:
                            is_plural = True

                        by = delete_node.get('by')
                        delete_command = CppManagerDeleteCommand(is_plural, by)
                        cpp_manager.add_delete_command(delete_command)

                    # parse all <fetch/>
                    for fetch_node in manager_or_none.findall('fetch'):
                        is_plural = False
                        plural_node = fetch_node.get('plural')
                        if plural_node is not None:
                            is_plural = True

                        by = fetch_node.get('by')
                        fetch_command = CppManagerFetchCommand(is_plural, by)
                        cpp_manager.add_fetch_command(fetch_command)

                # write object header
                cpp_class = CppClass(group_name, class_name, cpp_var_list, cpp_enum_list, cpp_manager)
                cpp_class.generate_header()

                # write object implementation
                cpp_class.generate_implementation()

                # write manager header
                cpp_class.generate_manager_header()

                # write manager implementation
                cpp_class.generate_manager_implementation()
