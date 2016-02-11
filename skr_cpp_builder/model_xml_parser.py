import xml.etree.ElementTree
import re

from skrutil import io_utils

from cpp_variable import CppVariable
from cpp_class import CppClass
from cpp_enum import CppEnum

from cpp_manager import CppManager
from cpp_manager import CppManagerSaveCommand
from cpp_manager import CppManagerFetchCommand
from cpp_manager import CppManagerDeleteCommand
from cpp_manager import CppApiDescription

from cpp_replacement import CppReplacement


class CppModelXmlParser:

    def __init__(self, version):
        self.version = version

    def parse(self, directory):
        """Parse module description xml file and translate them into Cpp objects.

        Args:
            directory: Path of xml file including the file.
        """
        # create core folder if not exists and remove last build
        core_dir_path = 'build/core'
        io_utils.make_directory_if_not_exists(core_dir_path)

        # create api folder if not exists and remove last build
        api_dir_path = 'build/core/api'
        io_utils.make_directory_if_not_exists(api_dir_path)

        # start parsing xml
        e = xml.etree.ElementTree.parse(directory)
        root = e.getroot()

        # search all <define/>
        replacement_list = []
        for define_node in root.findall('define'):
            replacement = CppReplacement(define_node.get('name'), define_node.get('description'))
            replacement_list.append(replacement)

        # search directories
        for folder_node in root.findall('group'):
            group_name = folder_node.get('name')
            group_name = 'core/' + group_name
            io_utils.make_directory_if_not_exists('build/{0}'.format(group_name))

            # search classes
            for class_node in folder_node.findall('class'):
                class_name = class_node.get('name')
                class_comment = class_node.get('comment')

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
                    cpp_var = CppModelXmlParser.__parse_variable_node(variable)
                    cpp_var_list.append(cpp_var)

                # parse <manager/>
                cpp_manager = None
                manager_node_or_none = class_node.find('manager')
                if manager_node_or_none is not None:
                    manager_name = manager_node_or_none.get('name')
                    cpp_manager = CppManager(manager_name)

                    # parse all <save/>
                    for save_node in manager_node_or_none.findall('save'):
                        save_command = CppModelXmlParser.__parse_save_node(save_node)
                        cpp_manager.add_save_command(save_command)

                    # parse all <saves/>
                    for saves_node in manager_node_or_none.findall('saves'):
                        save_command = CppModelXmlParser.__parse_saves_node(saves_node)
                        cpp_manager.add_save_command(save_command)

                    # parse all <delete/>
                    for delete_node in manager_node_or_none.findall('delete'):
                        delete_command = CppModelXmlParser.__parse_delete_command(delete_node)
                        cpp_manager.add_delete_command(delete_command)

                    # parse all <deletes/>
                    for deletes_node in manager_node_or_none.findall('deletes'):
                        delete_command = CppModelXmlParser.__parse_delete_command(deletes_node)
                        cpp_manager.add_delete_command(delete_command)

                    # parse all <fetch/>
                    for fetch_node in manager_node_or_none.findall('fetch'):
                        fetch_command = CppModelXmlParser.__parse_fetch_node(fetch_node)
                        cpp_manager.add_fetch_command(fetch_command)

                    # parse all <fetches/>
                    for fetches_node in manager_node_or_none.findall('fetches'):
                        fetch_command = CppModelXmlParser.__parse_fetch_node(fetches_node)
                        cpp_manager.add_fetch_command(fetch_command)

                    # parse all <api/>
                    for api_node in manager_node_or_none.findall('api'):
                        api_name = api_node.get('name')
                        api_alias = api_node.get('alias')
                        api_method = api_node.get('method')
                        api_uri = api_node.get('uri')

                        input_var_list = []
                        inputs_node = api_node.find('inputs')
                        for variable_node in inputs_node.findall('variable'):
                            var_name = variable_node.get('name')
                            var_type_string = variable_node.get('type')
                            var_json_path = variable_node.get('json_path')
                            var_cache_desc = variable_node.get('cache')
                            var_enum_or_none = variable_node.get('enum')
                            var_capture_or_none = variable_node.get('capture')
                            if var_capture_or_none is None:
                                var_capture_or_none = False

                            var = CppVariable(var_name, var_type_string, var_json_path, None, var_cache_desc, var_capture_or_none)
                            var.set_enum_class_name(var_enum_or_none)

                            input_var_list.append(var)

                        output_var_list = []
                        extra_list = []
                        outputs_node = api_node.find('outputs')
                        for variable_node in outputs_node.findall('variable'):
                            var_name = variable_node.get('name')
                            var_type_string = variable_node.get('type')
                            var_json_path = variable_node.get('json_path')
                            var_cache_desc = variable_node.get('cache')
                            var_enum_or_none = variable_node.get('enum')

                            var = CppVariable(var_name, var_type_string, var_json_path, None, var_cache_desc)
                            var.set_enum_class_name(var_enum_or_none)

                            output_var_list.append(var)

                        # parse <extra/> inside <output/>
                        for extra_node in outputs_node.findall('extra'):
                            extra_list.append(extra_node.get('cache'))

                        api = CppApiDescription(api_name, api_alias, api_method, api_uri, input_var_list, output_var_list, extra_list)
                        cpp_manager.add_api_description(api)

                    # parse <tables/>
                    table_name_list = []
                    tables_node_or_none = manager_node_or_none.find('tables')
                    if tables_node_or_none is not None:
                        for table_node in tables_node_or_none.findall('table'):
                            table_name_list.append(table_node.get('name'))
                    cpp_manager.set_table_name_list(table_name_list)

                # write object header
                cpp_class = CppClass(group_name, class_name, cpp_var_list, cpp_enum_list, cpp_manager, replacement_list, class_comment)
                cpp_class.generate_header()

                # write object implementation
                cpp_class.generate_implementation()

                # write manager header
                cpp_class.generate_manager_header()

                # write manager implementation
                cpp_class.generate_manager_implementation()

                # write web_api_object.h under "api" folder
                cpp_class.generate_web_api_header()

                # write web_api_object.cc under "api" folder
                cpp_class.generate_web_api_implementation()

    @staticmethod
    def __parse_variable_node(var_node):
        """Parse <variable/>

        Args:
            var_node: variable node

        Returns:
            instance CppVariable object
        """
        variable_name = var_node.get('name')
        variable_type = var_node.get('type')
        variable_json_path = var_node.get('json_path')
        variable_enum_or_none = var_node.get('enum')
        variable_sql_flag = var_node.get('sql_flag')
        var_cache_desc = var_node.get('cache')
        variable_json_search_path = var_node.get('json_search_path')
        var_override_sql_key_or_none = var_node.get('override_sql_key')

        variable_is_read_only = var_node.get('readonly')
        if variable_is_read_only is None:
            variable_is_read_only = False
        else:
            if variable_is_read_only == 'true':
                variable_is_read_only = True
            else:
                variable_is_read_only = False

        var_capture_or_none = var_node.get('capture')
        if var_capture_or_none is None:
            var_capture_or_none = False

        cpp_var = CppVariable(variable_name, variable_type, variable_json_path, variable_sql_flag, var_cache_desc, var_capture_or_none, variable_is_read_only)
        cpp_var.set_enum_class_name(variable_enum_or_none)
        cpp_var.set_json_search_path(variable_json_search_path)
        cpp_var.set_override_sql_key(var_override_sql_key_or_none)
        return cpp_var

    @staticmethod
    def __parse_fetch_node(fetch_node):
        """Parse <fetch/>

        Args:
            fetch_node: fetch node

        Returns:
            instance CppFetchCommand object
        """
        is_plural = False
        plural_attr = fetch_node.get('plural')
        singular_attr = fetch_node.get('singular')
        if plural_attr is not None:
            is_plural = True
        elif singular_attr is not None:
            is_plural = False

        by = fetch_node.get('by')
        sort_by_or_none = fetch_node.get('sort')
        is_asc = True
        if sort_by_or_none is not None:
            desc_desciption_or_none = fetch_node.get('desc')
            if desc_desciption_or_none is not None:
                if desc_desciption_or_none == 'true':
                    is_asc = False

        table_names_or_none = fetch_node.get('tables')
        table_name_list = []
        if table_names_or_none is None or table_names_or_none == '':
            table_name_list = []
        else:
            table_name_list = re.split(',', table_names_or_none)

        fetch_command = CppManagerFetchCommand(is_plural, by, sort_by_or_none, is_asc, table_name_list)
        return fetch_command

    @staticmethod
    def __parse_fetches_node(fetches_node):
        """Parse <fetches/>

        Args:
            fetches_node: fetch node

        Returns:
            instance CppFetchCommand object
        """
        by = fetches_node.get('by')
        sort_by_or_none = fetches_node.get('sort')
        is_asc = True
        if sort_by_or_none is not None:
            desc_desciption_or_none = fetches_node.get('desc')
            if desc_desciption_or_none is not None:
                if desc_desciption_or_none == 'true':
                    is_asc = False

        table_names_or_none = fetches_node.get('tables')
        table_name_list = []
        if table_names_or_none is None or table_names_or_none == '':
            table_name_list = []
        else:
            table_name_list = re.split(',', table_names_or_none)

        fetch_command = CppManagerFetchCommand(True, by, sort_by_or_none, is_asc, table_name_list)
        return fetch_command

    @staticmethod
    def __parse_save_node(save_node):
        """Parse <save/>

        Args:
            save_node: save node

        Returns:
            instance CppSaveCommand object
        """
        # if we have "singular" or "plural" attributes, consider as old style
        is_plural = False
        plural_attr = save_node.get('plural')
        singular_attr = save_node.get('singular')
        if plural_attr is not None:
            is_plural = True
        if singular_attr is not None:
            is_plural = False

        table_name_list = []
        table_names_or_none = save_node.get('tables')
        if table_names_or_none is not None:
            table_name_list = re.split(',', table_names_or_none)

        save_command = CppManagerSaveCommand(is_plural, table_name_list)
        return save_command

    @staticmethod
    def __parse_saves_node(saves_node):
        """Parse <saves/>

        Args:
            saves_node: saves node

        Returns:
            instance CppSaveCommand object
        """
        table_name_list = []
        table_names_or_none = saves_node.get('tables')
        if table_names_or_none is not None:
            table_name_list = re.split(',', table_names_or_none)

        save_command = CppManagerSaveCommand(True, table_name_list)
        return save_command

    @staticmethod
    def __parse_delete_command(delete_node):
        """Parse <delete/>

        Args:
            delete_node: delete node

        Returns:
            instance CppDeleteCommand object
        """
        # if we have "singular" or "plural" attributes, consider as old style
        is_plural = False
        plural_attr = delete_node.get('plural')
        singular_attr = delete_node.get('singular')
        if plural_attr is not None:
            is_plural = True
        elif singular_attr is not None:
            is_plural = False

        by = delete_node.get('by')

        table_name_list = []
        table_names_or_none = delete_node.get('tables')
        if table_names_or_none is not None:
            table_name_list = re.split(',', table_names_or_none)

        delete_command = CppManagerDeleteCommand(is_plural, by, table_name_list)
        return delete_command

    @staticmethod
    def __parse_deletes_command(deletes_node):
        """Parse <delete/>

        Args:
            deletes_node: delete node

        Returns:
            instance CppDeleteCommand object
        """
        by = deletes_node.get('by')

        table_name_list = []
        table_names_or_none = deletes_node.get('tables')
        if table_names_or_none is not None:
            table_name_list = re.split(',', table_names_or_none)

        delete_command = CppManagerDeleteCommand(True, by, table_name_list)
        return delete_command
