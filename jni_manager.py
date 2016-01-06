import re
from skr_logger import skr_log_warning
import string_utils

_JNI_BR = '\n\n'
_JNI_SPACE = '  '

class JniManager:
    def __init__(self, manager_name):
        self.manager_name = manager_name
        self.save_commands = []
        self.delete_commands = []
        self.fetch_commands = []

        self.object_name = ''
        self.plural_object_name = ''
        self.group_name = ''

        self.jni_variable_list = []

        self.fetch_has_sign = False
        self.size_same_fetch_method_name = 0

    def set_object_name(self, class_name, plural_class_name):
        self.object_name = class_name
        self.plural_object_name = plural_class_name

    def set_group_name(self, group_name):
        self.group_name = group_name

    def set_jni_variable_list(self, jni_variable_list):
        self.jni_variable_list = jni_variable_list

    def add_save_command(self, save_command):
        self.save_commands.append(save_command)

    def add_fetch_command(self, fetch_command):
        self.fetch_commands.append(fetch_command)
        if self.fetch_has_sign:
            return
        by_list = []

        if fetch_command.where != '':
            by_list = re.split(',', fetch_command.where)

        if len(by_list) == 0:
            self.size_same_fetch_method_name += 1
        elif len(by_list) > 1:
            self.size_same_fetch_method_name += 1

        if self.size_same_fetch_method_name > 1:
            self.fetch_has_sign = True

    def add_delete_command(self, delete_command):
        self.delete_commands.append(delete_command)

    def class_name(self):
        return self.manager_name

    def generate_fetch_declarations(self):
        declaration = ''

        for fetch_command in self.fetch_commands:
            by_list = []
            if fetch_command.where != '':
                by_list = re.split(',', fetch_command.where)

            bys = self.__convert_bys_to_string(by_list, self.fetch_has_sign)

            if not fetch_command.is_plural:
                if len(by_list) == 0:
                    skr_log_warning('Singular often comes with at least one by parameter')
                declaration += 'JNIEXPORT jlong JNICALL Java_com_lesschat_core_{0}_{1}_nativeFetch{2}FromCache{3}'\
                    .format(self.group_name, self.manager_name, self.object_name, bys)
            else:
                declaration += 'JNIEXPORT jlongArray JNICALL Java_com_lesschat_core_{0}_{1}_nativeFetch{2}FromCache{3}'\
                    .format(self.group_name, self.manager_name, self.plural_object_name, bys)
        return declaration

    def generate_fetch_implementations(self):
        impl = ''
        for fetch_command in self.fetch_commands:
            impl += self.__fetch_implementation(fetch_command)
            impl += _JNI_BR
        return impl

    def __fetch_implementation(self, fetch_command):
        by_list = []
        impl = ''
        if fetch_command.where != '':
            by_list = re.split(',', fetch_command.where)

        bys = self.__convert_bys_to_string_impl(by_list, self.fetch_has_sign)

        if not fetch_command.is_plural:
            if len(by_list) == 0:
                    skr_log_warning('Singular often comes with at least one by parameter')
            impl += 'JNIEXPORT jlong JNICALL Java_com_lesschat_core_{0}_{1}_nativeFetch{2}FromCache{3}'\
                    .format(self.group_name, self.manager_name, self.object_name, bys)
            impl += _JNI_SPACE + 'const lesschat::{0}* core_manager = reinterpret_cast<lesschat::{0}*>(handler);'\
                .format(self.manager_name)
            impl += _JNI_BR

            cpp_method_param = ''
            for by_string in by_list:
                jni_var = self.__jni_var_by_name(by_string)
                if jni_var is not None:
                    impl += _JNI_SPACE + jni_var.var_type.to_getter_string() + " cpp_" + jni_var.to_param_style_name()
                    impl += ' = ' + jni_var.cpp_variable_from_jni_variable(jni_var.to_param_style_name()) + ';'
                    cpp_method_param += 'cpp_' + jni_var.to_param_style_name() + ', '
            impl += _JNI_BR
            if len(by_list) == 1:
                cpp_method_by = 'By' + jni_var.to_title_style_name()
            else:
                cpp_method_by = ''

            cpp_method_name = 'Fetch{0}FromCache{1}'.format(self.object_name, cpp_method_by)
            cpp_method_param = cpp_method_param[:-2]
            impl += _JNI_SPACE + 'std::unique_ptr<lesschat::{0}> core_object = core_manager->{1}({2});\n\n'\
                .format(self.object_name, cpp_method_name, cpp_method_param)
            impl += _JNI_SPACE + 'if(core_object == nullptr){\n    return 0;\n  }\n'
            impl += _JNI_SPACE + 'return reinterpret_cast<long>(core_object.release());\n}'

        else:
            impl += 'JNIEXPORT jlongArray JNICALL Java_com_lesschat_core_{0}_{1}_nativeFetch{2}FromCache{3}'\
                    .format(self.group_name, self.manager_name, self.plural_object_name, bys)
            impl += _JNI_SPACE + 'const lesschat::{0}* core_manager = reinterpret_cast<lesschat::{0}*>(handler);'\
                .format(self.manager_name)
            impl += _JNI_BR

            cpp_method_param = ''
            for by_string in by_list:
                jni_var = self.__jni_var_by_name(by_string)
                if jni_var is not None:
                    impl += _JNI_SPACE + jni_var.to_getter_string() + " cpp_" + jni_var.to_param_style_name()
                    impl += ' = ' + jni_var.cpp_variable_from_jni_variable(jni_var.to_param_style_name()) + ';\n'
                    cpp_method_param += 'cpp_' + jni_var.to_param_style_name() + ', '
            if len(by_list) == 1:
                cpp_method_by = 'By' + jni_var.to_title_style_name()
            else:
                cpp_method_by = ''

            cpp_method_name = 'Fetch{0}FromCache{1}'.format(self.plural_object_name, cpp_method_by)
            cpp_method_param = cpp_method_param[:-2]
            impl += _JNI_SPACE
            impl += 'std::vector<std::unique_ptr<lesschat::{0}>> core_objects = core_manager->{1}({2});\n\n'\
                .format(self.object_name, cpp_method_name, cpp_method_param)
            impl += _JNI_SPACE + 'return lesschat::JniHelper::JlongArrayFromNativeArray(std::move(core_objects));\n}'
        return impl

    # returns "ById" or ""
    def __convert_bys_to_string(self, by_string_list, has_sign):
        if len(by_string_list) == 0:  # empty string
            if has_sign:
                return '__J\n  (JNIEnv *, jobject, jlong);\n\n'
            else:
                return '\n  (JNIEnv *, jobject, jlong);\n\n'
        elif len(by_string_list) == 1:  # "ById(const std::string& id)"
            by_string = by_string_list[0]
            jni_var = self.__jni_var_by_name(by_string)
            if jni_var is not None:
                return 'By{0}\n  (JNIEnv *, jobject, jlong, {1});\n\n'\
                    .format(jni_var.to_title_style_name(), jni_var.jni_variable_name())
            else:
                print 'Unknown "{0}" in "by"'.format(by_string)
                return ''
        else:  # "(const std::string& id, const std::string& username)"
            bys_string = '{0}\n  (JNIEnv *, jobject, jlong, '
            sign = 'J'
            for by_string in by_string_list:
                jni_var = self.__jni_var_by_name(by_string)
                if jni_var is not None:
                    bys_string += jni_var.jni_variable_name() + ', '
                    sign += jni_var.jni_variable_sign_name()
                else:
                    print 'Unknown "{0}" in "by"'.format(by_string)
                    return ''
            bys_string = bys_string[:-2]  # remove last 2 chars
            bys_string += ');\n\n'
            sign_ = ''
            if has_sign:
                sign_ = '__' + sign
            return bys_string.format(sign_)

    def __convert_bys_to_string_impl(self, by_string_list, has_sign):
        if len(by_string_list) == 0:  # empty string
            if has_sign:
                return '__J\n  (JNIEnv *, jobject, jlong);\n\n'
            else:
                return '\n  (JNIEnv *env, jobject thiz, jlong handler){\n'
        elif len(by_string_list) == 1:  # "ById(const std::string& id)"
            by_string = by_string_list[0]
            jni_var = self.__jni_var_by_name(by_string)
            if jni_var is not None:
                return 'By{0}\n  (JNIEnv *env, jobject thiz, jlong handler, {1} {2}){{\n'\
                    .format(jni_var.to_title_style_name(), jni_var.jni_variable_name(), jni_var.to_param_style_name())
            else:
                print 'Unknown "{0}" in "by"'.format(by_string)
                return ''
        else:  # "(const std::string& id, const std::string& username)"
            bys_string = '{0}\n  (JNIEnv *env, jobject thiz, jlong handler, '
            sign = 'J'
            for by_string in by_string_list:
                jni_var = self.__jni_var_by_name(by_string)
                if jni_var is not None:
                    bys_string += jni_var.jni_variable_name() + ' {0}, '.format(jni_var.to_param_style_name())
                    sign += jni_var.jni_variable_sign_name()
                else:
                    print 'Unknown "{0}" in "by"'.format(by_string)
                    return ''
            bys_string = bys_string[:-2]  # remove last 2 chars
            bys_string += '){{\n'
            sign_ = ''
            if has_sign:
                sign_ = '__' + sign
            return bys_string.format(sign_)

    # returns None if not found
    def __jni_var_by_name(self, name_string):
        for jni_var in self.jni_variable_list:
            if jni_var.name == name_string:
                return jni_var
        return None


