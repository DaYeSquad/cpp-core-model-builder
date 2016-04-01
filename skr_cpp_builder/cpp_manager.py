# -*- coding: utf-8 -*-
#!/usr/bin/env python
# cpp_manager.py
#
# Copyright (c) 2016 - Frank Lin

"""
Parse and store lesschat/worktile C++ object manager info.
"""

import re
import copy

from skrutil.skr_logger import skr_log_warning
from skrutil import string_utils


_CPP_BR = '\n\n'
_CPP_SPACE = '  '


class CppManagerSaveCommand:
    """Represents 'SaveObject(s)FromCacheByKey' (<save/>)
    """

    def __init__(self, is_plural, table_name_list, alias_or_none):
        """Init CppManagerSaveCommand with some required parameters.

        Args:
            is_plural: can be True or False
            table_name: should be a string describes override table_name, if table_name is empty, it will use default table_name
        """
        self.is_plural = is_plural
        self.table_name_list = table_name_list
        self.alias_or_none = alias_or_none


class CppManagerFetchCommand:
    """Represents 'FetchObject(s)FromCacheByKey' (<fetch/>)
    """

    def __init__(self, is_plural, where, sort_by_or_none, is_asc, table_name_list, alias_or_none):
        """Init CppManagerFetchCommand with some required parameters.

        Args:
            is_plural: can be True or False
            where: should be class variable names separated by comma (eg: 'uid,username,pwd')
            sort_by_or_none: should be class variable name (eg: 'uid') or None
            is_asc: can be True or False, used with sort_by_or_none
            table_name_list: should be table names override default one or none
        """
        self.sort_by_or_none = sort_by_or_none
        self.is_asc = is_asc
        self.is_plural = is_plural
        self.table_name_list = table_name_list
        self.alias_or_none = alias_or_none

        if where is not None:
            self.where = where
        else:
            self.where = ''

    def sort_sql(self):
        """Sort SQL for easySQLite.

        Returns:
            'key ASC' or 'key DESC'
        """
        if self.sort_by_or_none is not None:
            order = 'ASC'
            if self.is_asc is False:
                order = 'DESC'
            return ', "{0} {1}"'.format(self.sort_by_or_none, order)
        return ''


class CppManagerDeleteCommand:
    """Represents 'DeleteObject(s)FromCacheByKey' (<delete/>)
    """

    def __init__(self, is_plural, where, table_name_list, alias_or_none):
        self.is_plural = is_plural
        self.table_name_list = table_name_list
        self.alias_or_none = alias_or_none

        if where is not None:
            self.where = where
        else:
            self.where = ''


class CppApiDescription:

    def __init__(self, name, alias, method, uri, input_var_list, output_var_list, extra_list):
        self.name = name
        self.alias = alias
        self.method = method
        self.uri = uri
        self.input_var_list = input_var_list
        self.output_var_list = output_var_list
        self.extra_list = extra_list


class CppManager:
    """Object Manager methods declaration and implementation.
    """

    def __init__(self, manager_name):
        self.manager_name = manager_name  # UserManager
        self.save_commands = []
        self.delete_commands = []
        self.fetch_commands = []
        self.apis = []

        self.object_name = ''  # User
        self.plural_object_name = ''  # Users

        self.cpp_variable_list = []
        self.cpp_replacement_list = []

        self.table_name_list = []

    def set_object_name(self, class_name, plural_class_name):
        self.object_name = class_name
        self.plural_object_name = plural_class_name

    def set_cpp_variable_list(self, cpp_variable_list):
        self.cpp_variable_list = cpp_variable_list

    def set_replacement_list(self, cpp_replacement_list):
        self.cpp_replacement_list = cpp_replacement_list

    def set_table_name_list(self, table_name_list):
        self.table_name_list = table_name_list

    def add_save_command(self, save_command):
        self.save_commands.append(save_command)

    def add_fetch_command(self, fetch_command):
        self.fetch_commands.append(fetch_command)

    def add_delete_command(self, delete_command):
        self.delete_commands.append(delete_command)

    def add_api_description(self, api_description):
        self.apis.append(api_description)

    def class_name(self):
        return self.manager_name

    def sqlite_table_var(self, given_name=None):
        if given_name is None or given_name == '':
            return 'std::unique_ptr<sql::Table> {0};'.format(self.__sqlite_tb_name())
        else:
            return 'std::unique_ptr<sql::Table> {0}_tb_;'.format(given_name)

    def sqlite_record_by_object_declaration(self, table_name=''):
        """Returns 'sql::Record RecordByObject(const Object& obj) const;' (if table_name is empty)
            or
            'sql::Record RecordByTaskFromTable(const Task& task) const; declaration'
        """
        if table_name == '':
            return 'sql::Record RecordBy{0}(const {0}& {1}) const;'\
                .format(self.object_name, self.object_name.lower())
        else:
            return 'sql::Record RecordBy{0}From{2}(const {0}& {1}) const;'\
                .format(self.object_name, self.object_name.lower(), string_utils.to_title_style_name(table_name))

    def sqlite_record_by_object_implementation(self, table_name=''):
        """Returns 'sql::Record RecordByObject(const Object& obj) const;' (if table_name is empty)
            or
            'sql::Record RecordByTaskFromTable(const Task& task) const; implementation'
        """
        impl = ''
        if table_name == '':
            impl += 'sql::Record {0}::RecordBy{1}(const {1}& {2}) const {{\n'\
                .format(self.manager_name, self.object_name, self.object_name.lower())
            impl += _CPP_SPACE + 'sql::Record record({0}->fields());\n\n'.format(self.__sqlite_tb_name())
        else:
            impl += 'sql::Record {0}::RecordBy{1}From{3}(const {1}& {2}) const {{\n'\
                .format(self.manager_name, self.object_name, self.object_name.lower(), string_utils.to_title_style_name(table_name))
            impl += _CPP_SPACE + 'sql::Record record({0}->fields());\n\n'.format(self.__sqlite_tb_name(table_name))

        for cpp_var in self.cpp_variable_list:
            impl += _CPP_SPACE
            impl += cpp_var.to_set_sql_string(self.object_name.lower())

        impl += '\n'
        impl += _CPP_SPACE
        impl += 'return record;\n'
        impl += '}'
        return impl

    def sqlite_object_from_record_declaration(self):
        """Returns 'std::unique_ptr<Object> ObjectFromRecord(sql::Record* record) const;' declaration"""
        return 'std::unique_ptr<{0}> {0}FromRecord(sql::Record* record) const;'.format(self.object_name)

    def sqlite_object_from_record_implementation(self):
        """Returns 'std::unique_ptr<Object> ObjectFromRecord(sql::Record* record) const;' implementation"""
        impl = 'std::unique_ptr<{0}> {1}::{0}FromRecord(sql::Record* record) const {{\n'.format(self.object_name, self.manager_name)
        for cpp_var in self.cpp_variable_list:
            impl += _CPP_SPACE
            impl += cpp_var.to_get_sql_value_string()
        impl += '\n'
        impl += _CPP_SPACE
        impl += 'unique_ptr<{0}> {1}(new {0}());\n'.format(self.object_name, self.object_name.lower())
        impl += _CPP_SPACE
        impl += '{0}->Init('.format(self.object_name.lower())
        for cpp_var in self.cpp_variable_list:
            impl += cpp_var.name
            impl += ', '
        impl = impl[:-2]  # remove last 2 chars
        impl += ');\n'
        impl += _CPP_SPACE
        impl += 'return {0};\n'.format(self.object_name.lower())
        impl += '}'
        return impl

    def unsafe_save_declaration(self, pre_spaces, table_name=''):
        """Returns 'UnsafeSaveObjectToCache' or 'UnsafeSaveObjectToTable' declaration"""
        if table_name == '':
            return '{2}void UnsafeSave{0}ToCache(const {0}& {1}) const;\n\n'\
                .format(self.object_name, self.object_name.lower(), pre_spaces)
        else:
            return '{2}void UnsafeSave{0}To{3}(const {0}& {1}) const;\n\n'\
                .format(self.object_name, self.object_name.lower(), pre_spaces, string_utils.to_title_style_name(table_name))

    def unsafe_save_implementation(self, table_name=''):
        """Returns 'UnsafeSaveObjectToCache' or 'UnsafeSaveObjectToTable' implementation"""
        impl = ''
        if table_name == '':
            impl += 'void {0}::UnsafeSave{1}ToCache(const {1}& {2}) const {{\n'\
                .format(self.manager_name, self.object_name, self.object_name.lower())
            impl += _CPP_SPACE + 'sql::Record record = RecordBy{0}({1});\n'.format(self.object_name, self.object_name.lower())
        else:
            impl += 'void {0}::UnsafeSave{1}To{3}(const {1}& {2}) const {{\n'\
                .format(self.manager_name, self.object_name, self.object_name.lower(), string_utils.to_title_style_name(table_name))
            impl += _CPP_SPACE + 'sql::Record record = RecordBy{0}From{2}({1});\n'.format(self.object_name, self.object_name.lower(), string_utils.to_title_style_name(table_name))
        impl += _CPP_SPACE + '{0}->addOrReplaceRecord(&record);\n'.format(self.__sqlite_tb_name(table_name))
        impl += '}'
        return impl

    def sqlite_key_declaration(self):
        declarations = ''
        for cpp_var in self.cpp_variable_list:
            sql_var_name = cpp_var.name
            if cpp_var.override_sql_key is not None:
                sql_var_name = cpp_var.override_sql_key
            declarations += 'static std::string const {0} = "{1}";\n'\
                .format(cpp_var.to_sql_key(), sql_var_name)
        declarations += '\nstatic std::string const kSqlAnd = " AND ";\n'
        return declarations

    def easy_sqlite_field_declaration(self):
        declarations = 'static sql::Field {0}[] = {{\n'.format(self.__sqlite_field_definition_name())
        for cpp_var in self.cpp_variable_list:
            declarations += _CPP_SPACE + 'sql::Field({0}, {1}, {2}),\n'\
                .format(cpp_var.to_sql_key(), cpp_var.to_easy_sqlite_value_type(), cpp_var.sql_flag_string())
        declarations += _CPP_SPACE + 'sql::Field(sql::DEFINITION_END),\n'
        declarations += '};'
        return declarations

    def generate_save_declarations(self, pre_spaces):
        declaration = ''
        for save_command in self.save_commands:
            if not save_command.is_plural:
                if save_command.alias_or_none is None:
                    declaration += '{2}void Save{0}ToCache(const {0}& {1}) const;\n\n'.format(self.object_name,
                                                                                              self.object_name.lower(),
                                                                                              pre_spaces)
                else:
                    declaration += '{2}void {3}(const {0}& {1}) const;\n\n'.format(self.object_name,
                                                                                   self.object_name.lower(),
                                                                                   pre_spaces,
                                                                                   save_command.alias_or_none)
            else:
                if save_command.alias_or_none is None:
                    declaration += '{0}void Save{1}ToCache(const std::vector<std::unique_ptr<{2}>>& {3}s) const;\n\n'\
                        .format(pre_spaces, self.plural_object_name, self.object_name, self.object_name.lower())
                else:
                    declaration += '{0}void {1}(const std::vector<std::unique_ptr<{2}>>& {3}s) const;\n\n'\
                        .format(pre_spaces, save_command.alias_or_none, self.object_name, self.object_name.lower())
        return declaration

    def generate_save_implementations(self):
        impl = ''
        for save_command in self.save_commands:
            impl += self.__save_implementation(save_command) + _CPP_BR
        return impl

    def generate_delete_declarations(self, pre_spaces):
        declaration = ''
        for delete_command in self.delete_commands:
            by_list = []
            if delete_command.where != '':
                by_list = re.split(',', delete_command.where)

            if not delete_command.is_plural:
                # validation
                if len(by_list) == 0:
                    skr_log_warning('Singular often comes with at least one by parameter')

                # logic
                if delete_command.alias_or_none is None:
                    declaration += '{0}void Delete{1}FromCache{2} const;\n\n'\
                        .format(pre_spaces, self.object_name, self.__convert_bys_to_string(by_list))
                else:
                    declaration += '{0}void {1}{2} const;\n\n'\
                        .format(pre_spaces, self.object_name, self.__convert_bys_to_string(by_list), delete_command.alias_or_none)
            else:
                if delete_command.alias_or_none is None:
                    declaration += '{0}void Delete{1}FromCache{2} const;\n\n'\
                        .format(pre_spaces, self.plural_object_name, self.__convert_bys_to_string(by_list))
                else:
                    print(delete_command.alias_or_none)
                    declaration += '{0}void {1}{2} const;\n\n'\
                        .format(pre_spaces, delete_command.alias_or_none, self.__convert_bys_to_string(by_list))
        return declaration

    def generate_delete_implementations(self):
        impl = ''
        for delete_command in self.delete_commands:
            impl += self.__delete_implementation(delete_command) + _CPP_BR
        return impl

    def generate_fetch_declarations(self, pre_spaces):
        declaration = ''
        for fetch_command in self.fetch_commands:
            by_list = []
            if fetch_command.where != '':
                by_list = re.split(',', fetch_command.where)

            if not fetch_command.is_plural:
                # validation
                if len(by_list) == 0:
                    skr_log_warning('Singular often comes with at least one by parameter')

                # logic
                if fetch_command.alias_or_none is None:
                    declaration += '{0}std::unique_ptr<{1}> Fetch{1}FromCache{2} const;\n\n'\
                        .format(pre_spaces, self.object_name, self.__convert_bys_to_string(by_list))
                else:
                    declaration += '{0}std::unique_ptr<{1}> {3}{2} const;\n\n'\
                        .format(pre_spaces, self.object_name, self.__convert_bys_to_string(by_list), fetch_command.alias_or_none)
            else:
                if fetch_command.alias_or_none is None:
                    declaration += '{0}std::vector<std::unique_ptr<{1}>> Fetch{2}FromCache{3} const;\n\n'\
                        .format(pre_spaces, self.object_name, self.plural_object_name, self.__convert_bys_to_string(by_list))
                else:
                    declaration += '{0}std::vector<std::unique_ptr<{1}>> {2}{3} const;\n\n'\
                        .format(pre_spaces, self.object_name, fetch_command.alias_or_none, self.__convert_bys_to_string(by_list))
        return declaration

    def generate_fetch_implementations(self):
        impl = ''
        for fetch_command in self.fetch_commands:
            impl += self.__fetch_implementation(fetch_command)
            impl += _CPP_BR
        return impl

    def generate_constructor_implementation(self):
        return '{0}::{0}(Director* director)\n:ObjectManager(director) {{\n}}'.format(self.manager_name)

    def generate_deconstructor_implementation(self):
        return '{0}::~{0}() {{\n}}'.format(self.manager_name)

    def generate_init_or_die_implementation(self):
        impl = 'bool {0}::InitOrDie() {{\n'.format(self.manager_name)
        impl += _CPP_SPACE + 'bool success = true;' + _CPP_BR
        impl += _CPP_SPACE + 'do {\n'
        impl += self.__tables_init_implementation()
        impl += _CPP_SPACE + '} while(0);' + _CPP_BR
        impl += _CPP_SPACE
        impl += 'return success;\n'
        impl += '}'
        return impl

    def generate_default_manager_implementation(self):
        impl = 'const {0}* {0}::DefaultManager() {{\n'.format(self.manager_name)
        impl += _CPP_SPACE + 'return Director::DefaultDirector()->{0}();\n'.format(self.__convert_class_name_to_file_name(self.manager_name))
        impl += '}'
        return impl

    def generate_wep_api_declarations(self):
        declaration = '// {0} --------------------------------------------------------'.format(self.object_name)
        declaration += _CPP_BR

        for api in self.apis:
            declaration += '// {0}\n'.format(api.uri)
            declaration += 'void {0}({1});'.format(api.name, self.__api_parameters_declaration(api))
            declaration += _CPP_BR

        return declaration

    def generate_web_api_implementation(self):
        impl = '#include "web_api.h"\n\n#include "json11/json11.hpp"\n\n#include "utils/string_utils.h"\n#include "utils/json11_utils.h"\n\n'
        impl += 'using std::string;\nusing std::vector;\nusing std::unique_ptr;\n\nusing sakura::HttpRequest;\nusing sakura::HttpClient;\nusing sakura::HttpResponse;\n\n'
        impl += 'NS_LCC_BEGIN\n\n'
        impl += '////////////////////////////////////////////////////////////////////////////////\n'
        impl += '// WebApi, public:\n\n'
        impl += '// {0} --------------------------------------------------------'.format(self.object_name)
        impl += _CPP_BR
        for api in self.apis:
            impl += 'void WebApi::{0}({1}) {{\n'.format(api.name, self.__api_parameters_declaration(api))
            impl += string_utils.indent(2) + self.__api_implementation(api) + '\n'
            impl += '}'
            impl += _CPP_BR
        impl += 'NS_LCC_END'
        return impl

    def generate_manager_http_declarations(self, pre_spaces):
        declaration = ''

        for api in self.apis:
            declaration += pre_spaces + 'void {0}({1}) const;'.format(api.alias, self.__api_parameters_declaration(api))
            declaration += _CPP_BR

        return declaration

    def generate_manager_http_implementation(self):
        impl = ''
        for api in self.apis:
            impl += 'void {2}::{0}({1}) const {{\n'.format(api.alias, self.__api_parameters_declaration(api), self.manager_name)
            impl += self.__manager_http_implementation_v2(api) + '\n'
            impl += '}'
            impl += _CPP_BR
        return impl

    # returns "ById(const std::string& id)" or "(const std::string& id, const std::string& username)" or "()"
    def __convert_bys_to_string(self, by_string_list):
        if len(by_string_list) == 0:  # ()
            return '()'
        elif len(by_string_list) == 1:  # "ById(const std::string& id)"
            by_string = by_string_list[0]
            cpp_var = self.__cpp_var_by_name(by_string)
            if cpp_var is not None:
                return 'By{0}({1})'.format(cpp_var.to_title_style_name(), cpp_var.initializer())
            else:
                print('Unknown "{0}" in "by"'.format(by_string))
                return ''
        else:  # "(const std::string& id, const std::string& username)"
            bys_string = '('
            for by_string in by_string_list:
                cpp_var = self.__cpp_var_by_name(by_string)
                if cpp_var is not None:
                    bys_string += cpp_var.initializer() + ', '
                else:
                    print('Unknown "{0}" in "by"'.format(by_string))
                    return ''
            bys_string = bys_string[:-2]  # remove last 2 chars
            bys_string += ')'
            return bys_string

    # returns "string where_condition = kUid + '='' + uid + ''';"
    def __convert_bys_to_sql_where(self, by_string_list):
        if len(by_string_list) == 0:
            return 'string where_condition = "";'
        else:
            where_sql = 'string where_condition = '
            for by_string in by_string_list:
                cpp_var = self.__cpp_var_by_name(by_string)
                where_sql += cpp_var.to_where_equal_sql()
                where_sql += ' + kSqlAnd + '
            where_sql = where_sql[:-13]  # remove last ' AND '
            where_sql += ';'
            return where_sql

    # returns None if not found
    def __cpp_var_by_name(self, name_string):
        for cpp_var in self.cpp_variable_list:
            if cpp_var.name == name_string:
                return cpp_var
        return None

    # returns None if not found
    def __find_cpp_var_by_name(self, name_string, var_list):
        for cpp_var in var_list:
            if cpp_var.name == name_string:
                return cpp_var
        return None

    # returns "definition_users"
    def __sqlite_field_definition_name(self):
        return 'definition_{0}'.format(self.plural_object_name.lower())

    # returns "users_tb_"
    def __sqlite_tb_name(self, table_name=''):
        if table_name == '':
            return '{0}_tb_'.format(self.plural_object_name.lower())
        else:
            return '{0}_tb_'.format(table_name.lower())

    # convert 'UserGroup' to 'user_group', only works if first letter is upper case.
    @staticmethod
    def __convert_class_name_to_file_name(name):
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    def __save_implementation(self, save_command):
        if save_command.is_plural:
            impl = ''
            if save_command.alias_or_none is None:
                impl += 'void {0}::Save{3}ToCache(const std::vector<std::unique_ptr<{1}>>& {2}) const {{\n'\
                    .format(self.manager_name, self.object_name, self.plural_object_name.lower(), self.plural_object_name)
            else:
                impl += 'void {0}::{3}(const std::vector<std::unique_ptr<{1}>>& {2}) const {{\n'\
                    .format(self.manager_name, self.object_name, self.plural_object_name.lower(), save_command.alias_or_none)
            impl += '  LockMainDatabase();\n\n  BeginTransaction();' + _CPP_BR
            impl += '  for (auto it = {0}.begin(); it != {0}.end(); ++it) {{\n'.format(self.plural_object_name.lower())

            if len(save_command.table_name_list) == 0:
                impl += '    UnsafeSave{0}ToCache(**it);\n'.format(self.object_name)
            else:
                for table_name in save_command.table_name_list:
                    if table_name == self.plural_object_name:
                        impl += '    UnsafeSave{0}ToCache(**it);\n'.format(self.object_name)
                    else:
                        impl += '    UnsafeSave{0}To{1}(**it);\n'.format(self.object_name, string_utils.to_title_style_name(table_name))

            impl += '  }\n\n'
            impl += '  CommitTransaction();\n\n  UnlockMainDatabase();\n'
            impl += '}'
            return impl
        else:
            impl = 'void {0}::Save{1}ToCache(const {1}& {2}) const {{\n'.format(self.manager_name, self.object_name, self.object_name.lower())
            impl += '  LockMainDatabase();' + _CPP_BR

            if len(save_command.table_name_list) == 0:
                impl += '  UnsafeSave{0}ToCache({1});'.format(self.object_name, self.object_name.lower()) + _CPP_BR
            else:
                for table_name in save_command.table_name_list:
                    if table_name == self.plural_object_name.lower():
                        impl += '  UnsafeSave{0}ToCache({1});'.format(self.object_name, self.object_name.lower()) + _CPP_BR
                    else:
                        impl += '  UnsafeSave{0}To{2}({1});'.format(self.object_name, self.object_name.lower(), string_utils.to_title_style_name(table_name)) + _CPP_BR

            impl += '  UnlockMainDatabase();\n'
            impl += '}'
            return impl

    def __delete_implementation(self, delete_command):
        if not delete_command.is_plural:
            by_list = []
            where_sql = 'string where_condition = "";'
            if delete_command.where != '':
                by_list = re.split(',', delete_command.where)
                where_sql = self.__convert_bys_to_sql_where(by_list)

            impl = ''
            if delete_command.alias_or_none is None:
                impl += 'void {0}::Delete{1}FromCache{2} const {{\n'\
                    .format(self.manager_name, self.object_name, self.__convert_bys_to_string(by_list))
            else:
                impl += 'void {0}::{1}{2} const {{\n'\
                    .format(self.manager_name, delete_command.alias_or_none, self.__convert_bys_to_string(by_list))
            impl += _CPP_SPACE
            impl += where_sql + _CPP_BR
            impl += '  LockMainDatabase();' + _CPP_BR

            if len(delete_command.table_name_list) == 0:
                impl += '  {0}->deleteRecords(where_condition);\n\n'.format(self.__sqlite_tb_name())
            else:
                for table_name in delete_command.table_name_list:
                    if table_name == self.plural_object_name:
                        impl += '  {0}->deleteRecords(where_condition);\n\n'.format(self.__sqlite_tb_name())
                    else:
                        impl += '  {0}->deleteRecords(where_condition);\n\n'.format(self.__sqlite_tb_name(table_name))

            impl += '  UnlockMainDatabase();\n'
            impl += '}'
            return impl
        else:
            by_list = []
            where_sql = 'string where_condition = "";'
            if delete_command.where != '':
                by_list = re.split(',', delete_command.where)
                where_sql = self.__convert_bys_to_sql_where(by_list)

            impl = ''
            if delete_command.alias_or_none is None:
                impl += 'void {0}::Delete{1}FromCache{2} const {{\n'\
                    .format(self.manager_name, self.plural_object_name, self.__convert_bys_to_string(by_list))
            else:
                impl += 'void {0}::{1}{2} const {{\n'\
                    .format(self.manager_name, delete_command.alias_or_none, self.__convert_bys_to_string(by_list))
            impl += _CPP_SPACE
            impl += where_sql + _CPP_BR
            impl += _CPP_SPACE
            impl += 'LockMainDatabase();' + _CPP_BR

            if len(delete_command.table_name_list) == 0:
                impl += '  {0}->deleteRecords(where_condition);\n\n'.format(self.__sqlite_tb_name())
            else:
                for table_name in delete_command.table_name_list:
                    if table_name == self.plural_object_name:
                        impl += '  {0}->deleteRecords(where_condition);\n\n'.format(self.__sqlite_tb_name())
                    else:
                        impl += '  {0}->deleteRecords(where_condition);\n\n'.format(self.__sqlite_tb_name(table_name))

            impl += _CPP_SPACE
            impl += 'UnlockMainDatabase();\n'
            impl += '}'
            return impl

    def __fetch_implementation(self, fetch_command):
        by_list = []
        where_sql = 'string where_condition = "";'
        if fetch_command.where != '':
            by_list = re.split(',', fetch_command.where)
            where_sql = self.__convert_bys_to_sql_where(by_list)

        if not fetch_command.is_plural:
            impl = ''
            if fetch_command.alias_or_none is None:
                impl += 'std::unique_ptr<{0}> {2}::Fetch{0}FromCache{1} const {{\n'\
                        .format(self.object_name, self.__convert_bys_to_string(by_list), self.manager_name)
            else:
                impl += 'std::unique_ptr<{0}> {2}::{3}{1} const {{\n'\
                        .format(self.object_name, self.__convert_bys_to_string(by_list), self.manager_name, fetch_command.alias_or_none)
            impl += _CPP_SPACE + where_sql + _CPP_BR
            impl += '  LCC_DB_LOCK_GUARD;' + _CPP_BR

            tb_list = copy.copy(fetch_command.table_name_list)

            if len(tb_list) == 0:
                impl += '  {0}->open(where_condition);\n'.format(self.__sqlite_tb_name())
                impl += '  if ({0}->recordCount() != 0) {{\n'.format(self.__sqlite_tb_name())
                impl += '    sql::Record* record = {0}->getRecord(0);\n'.format(self.__sqlite_tb_name())
                impl += '    unique_ptr<{0}> rtn({0}FromRecord(record));\n'.format(self.object_name)
                impl += '    return rtn;\n'
                impl += '  }' + _CPP_BR
            else:
                for table_name in tb_list:
                    impl += '  {0}->open(where_condition);\n'.format(self.__sqlite_tb_name(table_name))
                    impl += '  if ({0}->recordCount() != 0) {{\n'.format(self.__sqlite_tb_name(table_name))
                    impl += '    sql::Record* record = {0}->getRecord(0);\n'.format(self.__sqlite_tb_name(table_name))
                    impl += '    unique_ptr<{0}> rtn({0}FromRecord(record));\n'.format(self.object_name)
                    impl += '    return rtn;\n'
                    impl += '  }' + _CPP_BR
            impl += '  return nullptr;\n'
            impl += '}'
            return impl
        else:
            # validations
            # table_name_list is not supported in plural case.
            if len(fetch_command.table_name_list) > 0 and fetch_command.alias_or_none is None:
                skr_log_warning('"tables" attribute only supported <fetch singular="true"/>')
            elif len(fetch_command.table_name_list) > 1 and fetch_command.alias_or_none is not None:
                skr_log_warning('"tables" attribute only supported at most 1 override name')

            # logic
            override_table_name = ''
            if len(fetch_command.table_name_list) > 0:
                override_table_name = fetch_command.table_name_list[0]

            impl = ''
            if fetch_command.alias_or_none is None:
                impl += 'std::vector<std::unique_ptr<{0}>> {3}::Fetch{1}FromCache{2} const {{\n\n'\
                        .format(self.object_name, self.plural_object_name, self.__convert_bys_to_string(by_list), self.manager_name)
            else:
                impl += 'std::vector<std::unique_ptr<{0}>> {3}::{1}{2} const {{\n\n'\
                        .format(self.object_name, fetch_command.alias_or_none, self.__convert_bys_to_string(by_list), self.manager_name)
            impl += '  vector<unique_ptr<{0}>> {1};\n\n'.format(self.object_name, self.plural_object_name.lower())
            impl += _CPP_SPACE + where_sql + _CPP_BR
            impl += '  LockMainDatabase();' + _CPP_BR
            impl += '  {0}->open(where_condition{1});\n\n'.format(self.__sqlite_tb_name(override_table_name), fetch_command.sort_sql())
            impl += '  for (int i = 0; i < {0}->recordCount(); ++i) {{\n'.format(self.__sqlite_tb_name(override_table_name))
            impl += '    sql::Record* record = {0}->getRecord(i);\n'.format(self.__sqlite_tb_name(override_table_name))
            impl += '    {0}.push_back({1}FromRecord(record));\n'.format(self.plural_object_name.lower(), self.object_name)
            impl += '  }\n\n'
            impl += '  UnlockMainDatabase();' + _CPP_BR
            impl += '  return {0};\n'.format(self.plural_object_name.lower())
            impl += '}'
            return impl

    def __api_parameters_declaration(self, api_description):
        declaration = ''
        for input_var in api_description.input_var_list:
            declaration += input_var.to_get_description_string()
            declaration += ', '

        declaration += 'std::function<void(bool success, const std::string& error'

        if len(api_description.output_var_list) > 0:
            output_declaration = ', '
            for output_var in api_description.output_var_list:
                output_declaration += output_var.to_set_description_string()
                output_declaration += ', '
            output_declaration = output_declaration[:-2]
            declaration += output_declaration

        declaration += ')> callback'

        return declaration

    def __api_implementation(self, api_description):
        var_names_or_none = string_utils.strings_or_none_in_brackets(api_description.uri)
        cpp_uri = ''
        if var_names_or_none is not None:
            cpp_uri = '"'
            cpp_uri += api_description.uri
            for var_name in var_names_or_none:
                cpp_var = self.__find_cpp_var_by_name(var_name, api_description.input_var_list)
                cpp_uri = cpp_uri.replace('[{0}]'.format(var_name), '[{0}]'.format(cpp_var.to_convert_to_string_description()))
            cpp_uri = cpp_uri.replace('[', '" + ')
            cpp_uri = cpp_uri.replace(']', ' + "')
            cpp_uri += '"'

            check_cpp_uri = cpp_uri[-5:]
            if check_cpp_uri == ' + ""':  # parameter is the last component
                cpp_uri = cpp_uri[:-5]
        else:
            cpp_uri = '"{0}"'.format(api_description.uri)

        impl = 'string api_path = {0};'.format(cpp_uri)
        impl += '\n'
        impl += string_utils.indent(2) + 'string url = BaseUrlForCurrentTeam() + api_path;' + _CPP_BR
        impl += string_utils.indent(2) + 'unique_ptr<HttpRequest> request = GenBaseRequestForCurrentTeam(HttpRequest::Type::{0});\n'.format(api_description.method)
        impl += string_utils.indent(2) + 'request->set_url(url);' + _CPP_BR

        impl += self.__generate_post_or_put_body(api_description)

        impl += string_utils.indent(2) + 'HttpClient::SharedClient()->\n'
        impl += string_utils.indent(2) + 'Send(std::move(request), [callback](unique_ptr<HttpResponse> response) {\n'
        impl += string_utils.indent(4) + 'if (response->is_succeed()) {\n'
        impl += string_utils.indent(6) + 'string error;\n'
        impl += string_utils.indent(6) + 'json11::Json json_obj = json11::Json::parse(response->response_data_as_string(), error);\n'
        impl += string_utils.indent(6) + 'int state_code = json_obj[kJsonKeyState].int_value();\n'
        impl += string_utils.indent(6) + 'if (state_code == 200) {\n'

        output_success_parameters = ''
        output_fail_parameters = ''
        for output_var in api_description.output_var_list:
            impl += output_var.parse_json(8)
            impl += '\n'

            output_success_parameters += ', '
            output_success_parameters += output_var.to_move_string()

            output_fail_parameters += ', '
            output_fail_parameters += output_var.to_null_string()

        impl += string_utils.indent(8) + 'callback(true, ""{0});\n'.format(output_success_parameters)
        impl += string_utils.indent(6) + '} else {\n'
        impl += string_utils.indent(8) + 'string ret_error = ErrorMessageFromStateCode(state_code);\n'
        impl += string_utils.indent(8) + 'callback(false, ret_error{0});\n'.format(output_fail_parameters)
        impl += string_utils.indent(6) + '}\n'
        impl += string_utils.indent(4) + '} else {\n'
        impl += string_utils.indent(6) + 'string ret_error = response->error_buffer();\n'
        impl += string_utils.indent(6) + 'callback(false, ret_error{0});\n'.format(output_fail_parameters)
        impl += string_utils.indent(4) + '}\n'
        impl += string_utils.indent(2) + '});'
        return impl

    def __generate_post_or_put_body(self, api_description):
        if api_description.method == 'POST' or api_description.method == 'PUT':
            valid_var_list = []

            for input_var in api_description.input_var_list:
                if input_var.json_path is not None and input_var.json_path != '':
                    valid_var_list.append(input_var)
            if len(valid_var_list) == 0:
                return ''

            body = string_utils.indent(2) + 'json11::Json put_or_post_json = json11::Json::object {\n'
            for var in valid_var_list:
                json_paths = re.split('/', var.json_path)
                if len(json_paths) > 2:
                    print 'We do not support ugly json which has more than 2 levels'
                    assert False
                elif len(json_paths) == 1:
                    body += string_utils.indent(4) + '{{ "{0}", {1} }},\n'.format(var.json_path, var.to_json11_type())
                elif len(json_paths) == 2:
                    body += string_utils.indent(4) + '{{ "{0}", json11::Json::object {{{{ "{1}", {2} }}}} }},\n'.format(json_paths[0], json_paths[1], var.to_json11_type())
            body += string_utils.indent(2) + '};\n'
            body += string_utils.indent(2) + 'string put_or_post_json_str = put_or_post_json.dump();' + _CPP_BR
            body += string_utils.indent(2) + 'request->set_request_data(put_or_post_json_str);' + _CPP_BR
            return body
        else:
            print 'Only PUT or POST method can have request_body'
            return ''

    def __manager_http_implementation(self, api_description):
        capture_parameters = ''
        input_parameters = ''
        for input_var in api_description.input_var_list:
            input_parameters += input_var.name + ', '

            if input_var.capture:
                capture_parameters += input_var.name + ', '

        output_callback_parameters = ''
        output_parameters = '(bool success, const std::string &error'
        if len(api_description.output_var_list) > 0:
            for output_var in api_description.output_var_list:
                output_parameters += ', '
                output_parameters += output_var.to_set_description_string()

                output_callback_parameters += ', '
                output_callback_parameters += output_var.to_move_string()
        output_parameters += ')'

        impl = string_utils.indent(2) + 'WebApi::Api()->{0}({1}[{3}this, callback]{2} {{\n'.format(api_description.name, input_parameters, output_parameters, capture_parameters)
        impl += string_utils.indent(4) + 'if (success) {\n'

        for output_var in api_description.output_var_list:
            impl += self.__cpp_cache_by_cache_description_name(output_var.cache_desc, output_var.name)

        for extra in api_description.extra_list:
            impl += self.__cpp_cache_by_cache_description_name(extra)

        impl += string_utils.indent(4) + '}\n'
        impl += string_utils.indent(4) + 'callback(success, error{0});\n'.format(output_callback_parameters)
        impl += string_utils.indent(2) + '});'

        return impl

    # v1 we first post HTTP request then update the database while v2 we exchange the steps.
    def __manager_http_implementation_v2(self, api_description):
        capture_parameters = ''
        input_parameters = ''
        for input_var in api_description.input_var_list:
            input_parameters += input_var.name + ', '

            if input_var.capture:
                capture_parameters += input_var.name + ', '

        output_callback_parameters = ''
        output_parameters = '(bool success, const std::string &error'
        if len(api_description.output_var_list) > 0:
            for output_var in api_description.output_var_list:
                output_parameters += ', '
                output_parameters += output_var.to_set_description_string()

                output_callback_parameters += ', '
                output_callback_parameters += output_var.to_move_string()
        output_parameters += ')'

        impl = ''
        if api_description.method == 'GET' or api_description.method == 'POST':
            impl += string_utils.indent(2) + 'WebApi::Api()->{0}({1}[{3}this, callback]{2} {{\n'.format(api_description.name, input_parameters, output_parameters, capture_parameters)
            impl += string_utils.indent(4) + 'if (success) {\n'

            for output_var in api_description.output_var_list:
                impl += self.__cpp_cache_by_cache_description_name(output_var.cache_desc, output_var.name)

            for extra in api_description.extra_list:
                impl += self.__cpp_cache_by_cache_description_name(extra)

            impl += string_utils.indent(4) + '}\n'
            impl += string_utils.indent(4) + 'callback(success, error{0});\n'.format(output_callback_parameters)
            impl += string_utils.indent(2) + '});'
        else:
            for output_var in api_description.output_var_list:
                impl += self.__cpp_cache_by_cache_description_name(output_var.cache_desc, output_var.name, 2)

            for extra in api_description.extra_list:
                impl += self.__cpp_cache_by_cache_description_name(extra, "", 2)

            impl += string_utils.indent(2) + 'WebApi::Api()->{0}({1}[{3}this, callback]{2} {{\n'.format(api_description.name, input_parameters, output_parameters, capture_parameters)
            impl += string_utils.indent(4) + 'callback(success, error{0});\n'.format(output_callback_parameters)
            impl += string_utils.indent(2) + '});'

        return impl

    def __cpp_cache_by_cache_description_name(self, cache_desc, name='', indent=6):
        cache_attr = cache_desc

        if cache_attr is None or cache_attr == '':  # if no 'cache'
            return ''

        impl = ''
        caches = re.split(',', cache_attr)
        for cache in caches:
            if cache[0] == '#':  # if define
                impl += string_utils.indent(indent) + self.__find_replace_string_by_name(cache[1:]) + '\n'
            else:  # if by command
                cpp_class = 'this->'
                method = ''

                # command_components[0]: save(s)/delete(s)/update(s)
                # command_components[1]: (id, project_id) - replace string
                command_components = re.split('\(', cache)
                sql_verb = command_components[0]
                parameters = ''
                num_parameters = 0
                if len(command_components) == 2:
                    parameters = command_components[1]
                    parameters = parameters[:-1]
                    num_parameters = len(re.split(',', parameters))
                else:
                    parameters = name
                    num_parameters = 0

                if sql_verb == 'saves':
                    method = 'Save{0}ToCache({1});\n'.format(self.plural_object_name, name)
                elif sql_verb == 'save':
                    method = 'Save{0}ToCache(*{1});\n'.format(self.object_name, name)
                elif sql_verb == 'deletes':
                    if num_parameters == 0:
                        method = 'Delete{0}FromCache();\n'.format(self.plural_object_name)
                    elif num_parameters == 1:
                        by = 'by_{0}'.format(parameters)
                        by = string_utils.to_title_style_name(by)
                        method = 'Delete{0}FromCache{2}({1});\n'.format(self.plural_object_name, parameters, by)
                    else:
                        method = 'Delete{0}FromCache({1});\n'.format(self.plural_object_name, parameters)
                elif sql_verb == 'delete':
                    if num_parameters == 0:
                        method = 'Delete{0}FromCache();\n'.format(self.object_name)
                    elif num_parameters == 1:
                        by = 'by_{0}'.format(parameters)
                        by = string_utils.to_title_style_name(by)
                        method = 'Delete{0}FromCache{2}({1});\n'.format(self.object_name, parameters, by)
                    else:
                        method = 'Delete{0}FromCache({1});\n'.format(self.object_name, parameters)
                elif sql_verb[:7] == 'fupdate':  # generate implementation automatically
                    components = re.split(':', sql_verb)
                    fetch_by_id = components[1]
                    impl = string_utils.indent(indent) + 'unique_ptr<{0}> {1} = this->Fetch{0}FromCacheBy{2}({3});\n'\
                        .format(self.object_name,
                                string_utils.cpp_class_name_to_cpp_file_name(self.object_name),
                                string_utils.to_title_style_name(fetch_by_id),
                                fetch_by_id)

                    for parameter in re.split(',', parameters):
                        impl += string_utils.indent(indent) + '{0}->set_{1}({1});\n'.format(string_utils.cpp_class_name_to_cpp_file_name(self.object_name), parameter)

                    impl += string_utils.indent(indent) + 'this->Save{0}ToCache(*{1});\n'.format(self.object_name, string_utils.cpp_class_name_to_cpp_file_name(self.object_name))
                    return impl
                else:
                    print 'Unsupported method'
                    assert False
                impl += string_utils.indent(indent) + cpp_class + method

        return impl

    def __find_replace_string_by_name(self, name):
        for replacement in self.cpp_replacement_list:
            if replacement.search == name:
                return replacement.replace
        return ''

    def __tables_init_implementation(self):
        default_table_name = self.plural_object_name.lower()
        tb_list = copy.copy(self.table_name_list)
        tb_list.append(default_table_name)

        impl = ''
        for table_name in tb_list:
            cpp_table_name = '{0}_tb_'.format(table_name)
            impl += _CPP_SPACE + _CPP_SPACE
            impl += '{0} = unique_ptr<sql::Table>(new sql::Table(MainDatabaseHandler(), "{1}", {2}));'\
                    .format(cpp_table_name, table_name, self.__sqlite_field_definition_name()) + _CPP_BR
            impl += _CPP_SPACE + _CPP_SPACE
            impl += 'if (!{0}->exists()) {{\n'.format(cpp_table_name)
            impl += _CPP_SPACE + _CPP_SPACE + _CPP_SPACE
            impl += 'success = {0}->create();\n'.format(cpp_table_name)
            impl += _CPP_SPACE + _CPP_SPACE + _CPP_SPACE
            impl += 'LCC_ASSERT(success);\n'
            impl += _CPP_SPACE + _CPP_SPACE
            impl += '}' + _CPP_BR
        return impl
