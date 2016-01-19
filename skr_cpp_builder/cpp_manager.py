# -*- coding: utf-8 -*-
#!/usr/bin/env python
# cpp_manager.py
#
# Copyright (c) 2016 - Frank Lin

"""
Parse and store lesschat/worktile C++ object manager info.
"""

import re
from skrutil.skr_logger import skr_log_warning


_CPP_BR = '\n\n'
_CPP_SPACE = '  '


class CppManagerSaveCommand:

    def __init__(self, is_plural):
        self.is_plural = is_plural


class CppManagerFetchCommand:

    def __init__(self, is_plural, where):
        self.is_plural = is_plural
        if where is not None:
            self.where = where
        else:
            self.where = ''


class CppManagerDeleteCommand:

    def __init__(self, is_plural, where):
        self.is_plural = is_plural
        if where is not None:
            self.where = where
        else:
            self.where = ''


class CppManager:

    def __init__(self, manager_name):
        self.manager_name = manager_name
        self.save_commands = []
        self.delete_commands = []
        self.fetch_commands = []

        self.object_name = ''
        self.plural_object_name = ''

        self.cpp_variable_list = []

    def set_object_name(self, class_name, plural_class_name):
        self.object_name = class_name
        self.plural_object_name = plural_class_name

    def set_cpp_variable_list(self, cpp_variable_list):
        self.cpp_variable_list = cpp_variable_list

    def add_save_command(self, save_command):
        self.save_commands.append(save_command)

    def add_fetch_command(self, fetch_command):
        self.fetch_commands.append(fetch_command)

    def add_delete_command(self, delete_command):
        self.delete_commands.append(delete_command)

    def class_name(self):
        return self.manager_name

    def sqlite_table_var(self):
        return 'std::unique_ptr<sql::Table> {0};'.format(self.__sqlite_tb_name())

    def sqlite_record_by_object_declaration(self):
        return 'sql::Record RecordBy{0}(const {0}& {1}) const;'.format(self.object_name, self.object_name.lower())

    def sqlite_record_by_object_implementation(self):
        impl = 'sql::Record {0}::RecordBy{1}(const {1}& {2}) const {{\n'\
            .format(self.manager_name, self.object_name, self.object_name.lower())
        impl += _CPP_SPACE
        impl += 'sql::Record record({0}->fields());\n\n'.format(self.__sqlite_tb_name())
        for cpp_var in self.cpp_variable_list:
            impl += _CPP_SPACE
            impl += cpp_var.to_set_sql_string(self.object_name.lower())

        impl += '\n'
        impl += _CPP_SPACE
        impl += 'return record;\n'
        impl += '}'
        return impl

    def sqlite_object_from_record_declaration(self):
        return 'std::unique_ptr<{0}> {0}FromRecord(sql::Record* record) const;'.format(self.object_name)

    def sqlite_object_from_record_implementation(self):
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

    def sqlite_key_declaration(self):
        declarations = ''
        for cpp_var in self.cpp_variable_list:
            declarations += 'static std::string const {0} = "{1}";\n'\
                .format(cpp_var.to_sql_key(), cpp_var.name)
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

    def unsafe_save_declaration(self, pre_spaces):
        return '{2}void UnsafeSave{0}ToCache(const {0}& {1}) const;\n\n'\
            .format(self.object_name, self.object_name.lower(), pre_spaces)

    def generate_save_declarations(self, pre_spaces):
        declaration = ''
        for save_command in self.save_commands:
            if not save_command.is_plural:
                declaration += '{2}void Save{0}ToCache(const {0}& {1}) const;\n\n'.format(self.object_name,
                                                                                          self.object_name.lower(),
                                                                                          pre_spaces)
            else:
                declaration += '{0}void Save{1}ToCache(const std::vector<std::unique_ptr<{2}>>& {3}s) const;\n\n'\
                    .format(pre_spaces, self.plural_object_name, self.object_name, self.object_name.lower())
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
                if len(by_list) == 0:
                    skr_log_warning('Singular often comes with at least one by parameter')
                declaration += '{0}void Delete{1}FromCache{2} const;\n\n'\
                    .format(pre_spaces, self.object_name, self.__convert_bys_to_string(by_list))
            else:
                declaration += '{0}void Delete{1}FromCache{2} const;\n\n'\
                    .format(pre_spaces, self.plural_object_name, self.__convert_bys_to_string(by_list))
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
                if len(by_list) == 0:
                    skr_log_warning('Singular often comes with at least one by parameter')
                declaration += '{0}std::unique_ptr<{1}> Fetch{1}FromCache{2} const;\n\n'\
                    .format(pre_spaces, self.object_name, self.__convert_bys_to_string(by_list))
            else:
                declaration += '{0}std::vector<std::unique_ptr<{1}>> Fetch{2}FromCache{3} const;\n\n'\
                    .format(pre_spaces, self.object_name, self.plural_object_name, self.__convert_bys_to_string(by_list))
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
        impl += _CPP_SPACE + _CPP_SPACE
        impl += '{0} = unique_ptr<sql::Table>(new sql::Table(MainDatabaseHandler(), "{1}", {2}));'\
                .format(self.__sqlite_tb_name(), self.manager_name, self.__sqlite_field_definition_name()) + _CPP_BR
        impl += _CPP_SPACE + _CPP_SPACE
        impl += 'if (!{0}->exists()) {{\n'.format(self.__sqlite_tb_name())
        impl += _CPP_SPACE + _CPP_SPACE + _CPP_SPACE
        impl += 'success = {0}->create();\n'.format(self.__sqlite_tb_name())
        impl += _CPP_SPACE + _CPP_SPACE + _CPP_SPACE
        impl += 'LCC_ASSERT(success);\n'
        impl += _CPP_SPACE + _CPP_SPACE
        impl += '}' + _CPP_BR
        impl += _CPP_SPACE
        impl += '} while(0);' + _CPP_BR
        impl += _CPP_SPACE
        impl += 'return success;\n'
        impl += '}'
        return impl

    def generate_default_manager_implementation(self):
        impl = 'const {0}* {0}::DefaultManager() {{\n'.format(self.manager_name)
        impl += _CPP_SPACE + 'return Director::DefaultDirector()->{0}();\n'.format(self.__convert_class_name_to_file_name(self.manager_name))
        impl += '}'
        return impl

    def generate_unsafe_save_implementation(self):
        impl = 'void {0}::UnsafeSave{1}ToCache(const {1}& {2}) const {{\n'\
            .format(self.manager_name, self.object_name, self.object_name.lower())
        impl += _CPP_SPACE
        impl += 'sql::Record record = RecordBy{0}({1});\n'.format(self.object_name, self.object_name.lower())
        impl += _CPP_SPACE
        impl += '{0}->addOrReplaceRecord(&record);\n'.format(self.__sqlite_tb_name())
        impl += '}'
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

    # returns "definition_users"
    def __sqlite_field_definition_name(self):
        return 'definition_{0}'.format(self.plural_object_name.lower())

    # returns "users_tb_"
    def __sqlite_tb_name(self):
        return '{0}_tb_'.format(self.plural_object_name.lower())

    # convert 'UserGroup' to 'user_group', only works if first letter is upper case.
    @staticmethod
    def __convert_class_name_to_file_name(name):
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    def __save_implementation(self, save_command):
        if save_command.is_plural:
            impl = 'void {0}::Save{3}ToCache(const std::vector<std::unique_ptr<{1}>>& {2}) const {{\n'\
                .format(self.manager_name, self.object_name, self.plural_object_name.lower(), self.plural_object_name)
            impl += _CPP_SPACE
            impl += 'LockMainDatabase();\n\n  BeginTransaction();' + _CPP_BR
            impl += _CPP_SPACE
            impl += 'for (auto it = {0}.begin(); it != {0}.end(); ++it) {{\n'.format(self.plural_object_name.lower())
            impl += _CPP_SPACE + _CPP_SPACE
            impl += 'UnsafeSave{0}ToCache(**it);\n'.format(self.object_name)
            impl += _CPP_SPACE
            impl += '}\n\n'
            impl += _CPP_SPACE
            impl += 'CommitTransaction();\n\n  UnlockMainDatabase();\n'
            impl += '}'
            return impl
        else:
            impl = 'void {0}::Save{1}ToCache(const {1}& {2}) const {{\n'.format(self.manager_name, self.object_name, self.object_name.lower())
            impl += _CPP_SPACE
            impl += 'LockMainDatabase();' + _CPP_BR
            impl += _CPP_SPACE
            impl += 'UnsafeSave{0}ToCache({1});'.format(self.object_name, self.object_name.lower()) + _CPP_BR
            impl += _CPP_SPACE
            impl += 'UnlockMainDatabase();\n'
            impl += '}'
            return impl

    def __delete_implementation(self, delete_command):
        if not delete_command.is_plural:
            by_list = []
            where_sql = 'string where_condition = "";'
            if delete_command.where != '':
                by_list = re.split(',', delete_command.where)
                where_sql = self.__convert_bys_to_sql_where(by_list)
            impl = 'void {0}::Delete{1}FromCache{2} const {{\n'\
                .format(self.manager_name, self.object_name, self.__convert_bys_to_string(by_list))
            impl += _CPP_SPACE
            impl += where_sql + _CPP_BR
            impl += _CPP_SPACE
            impl += 'LockMainDatabase();' + _CPP_BR
            impl += _CPP_SPACE
            impl += '{0}->deleteRecords(where_condition);\n\n'.format(self.__sqlite_tb_name())
            impl += _CPP_SPACE
            impl += 'UnlockMainDatabase();\n'
            impl += '}'
            return impl
        else:
            by_list = []
            where_sql = 'string where_condition = "";'
            if delete_command.where != '':
                by_list = re.split(',', delete_command.where)
                where_sql = self.__convert_bys_to_sql_where(by_list)
            impl = 'void {0}::Delete{1}FromCache{2} const {{\n'\
                .format(self.manager_name, self.plural_object_name, self.__convert_bys_to_string(by_list))
            impl += _CPP_SPACE
            impl += where_sql + _CPP_BR
            impl += _CPP_SPACE
            impl += 'LockMainDatabase();' + _CPP_BR
            impl += _CPP_SPACE
            impl += '{0}->deleteRecords(where_condition);\n\n'.format(self.__sqlite_tb_name())
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
            impl = 'std::unique_ptr<{0}> {2}::Fetch{0}FromCache{1} const {{\n'\
                    .format(self.object_name, self.__convert_bys_to_string(by_list), self.manager_name)
            impl += _CPP_SPACE
            impl += where_sql + _CPP_BR
            impl += _CPP_SPACE
            impl += 'LockMainDatabase();' + _CPP_BR
            impl += _CPP_SPACE
            impl += '{0}->open(where_condition);\n\n'.format(self.__sqlite_tb_name())
            impl += _CPP_SPACE
            impl += 'if ({0}->recordCount() != 0) {{\n'.format(self.__sqlite_tb_name())
            impl += _CPP_SPACE + _CPP_SPACE
            impl += 'sql::Record* record = {0}->getRecord(0);\n'.format(self.__sqlite_tb_name())
            impl += _CPP_SPACE + _CPP_SPACE
            impl += 'unique_ptr<{0}> rtn({0}FromRecord(record));\n'.format(self.object_name)
            impl += _CPP_SPACE + _CPP_SPACE
            impl += 'UnlockMainDatabase();\n'
            impl += _CPP_SPACE + _CPP_SPACE
            impl += 'return rtn;\n'
            impl += _CPP_SPACE
            impl += '}\n\n'
            impl += _CPP_SPACE
            impl += 'UnlockMainDatabase();' + _CPP_BR
            impl += _CPP_SPACE
            impl += 'return nullptr;\n'
            impl += '}'
            return impl
        else:
            impl = 'std::vector<std::unique_ptr<{0}>> {3}::Fetch{1}FromCache{2} const {{\n\n'\
                    .format(self.object_name, self.plural_object_name, self.__convert_bys_to_string(by_list), self.manager_name)
            impl += _CPP_SPACE
            impl += 'vector<unique_ptr<{0}>> {1};\n\n'.format(self.object_name, self.plural_object_name.lower())
            impl += _CPP_SPACE
            impl += where_sql + _CPP_BR
            impl += _CPP_SPACE
            impl += 'LockMainDatabase();' + _CPP_BR
            impl += _CPP_SPACE
            impl += '{0}->open(where_condition);\n\n'.format(self.__sqlite_tb_name())
            impl += _CPP_SPACE
            impl += 'for (int i = 0; i < {0}->recordCount(); ++i) {{\n'.format(self.__sqlite_tb_name())
            impl += _CPP_SPACE + _CPP_SPACE
            impl += 'sql::Record* record = {0}->getRecord(i);\n'.format(self.__sqlite_tb_name())
            impl += _CPP_SPACE + _CPP_SPACE
            impl += '{0}.push_back({1}FromRecord(record));\n'.format(self.plural_object_name.lower(), self.object_name)
            impl += _CPP_SPACE
            impl += '}\n\n'
            impl += _CPP_SPACE
            impl += 'UnlockMainDatabase();' + _CPP_BR
            impl += _CPP_SPACE
            impl += 'return {0};\n'.format(self.plural_object_name.lower())
            impl += '}'
            return impl
