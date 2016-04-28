#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - Frank Lin

import re

from skrutil.skr_logger import skr_log_warning

_JNI_BR = '\n\n'
_JNI_SPACE = '  '


def function_space(count):
    space = ''
    for i in range(1, count + 1):
        space += _JNI_SPACE
    return space


class JniManagerFetchCommand:
    def __init__(self, is_plural, where, alias):
        self.is_plural = is_plural

        if alias is not None:
            self.alias = alias
        else:
            self.alias = ''

        if where is not None:
            self.where = where
        else:
            self.where = ''


class JniManagerSaveCommand:
    def __init__(self, is_plural):
        self.is_plural = is_plural


class JniManagerDeleteCommand:
    def __init__(self, is_plural, where):
        self.is_plural = is_plural
        if where is not None:
            self.where = where
        else:
            self.where = ''


class JniApiDescription:
    """Represents manager's API description (<api/>).
    """

    def __init__(self, function_name, input_var_list, output_var_list):
        self.function_name = function_name
        self.input_var_list = input_var_list
        self.output_var_list = output_var_list


class JniManager:
    """Object manager in JNI part.
    """

    def __init__(self, manager_name):
        self.manager_name = manager_name
        self.save_commands = []
        self.delete_commands = []
        self.fetch_commands = []

        self.object_name = ''
        self.plural_object_name = ''
        self.group_name = ''

        self.jni_variable_list = []
        self.apis = []

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

    def add_api_description(self, api_description):
        self.apis.append(api_description)

    def class_name(self):
        return self.manager_name

    def generate_fetch_declarations(self):
        declaration = ''

        for fetch_command in self.fetch_commands:
            by_list = []
            if fetch_command.where != '':
                by_list = re.split(',', fetch_command.where)

            bys = self.__convert_bys_to_string(by_list, self.fetch_has_sign)

            if fetch_command.alias != '':
                fetch_fun_name = fetch_command.alias
            elif not fetch_command.is_plural:
                fetch_fun_name = 'Fetch{0}FromCache'.format(self.object_name)
            else:
                fetch_fun_name = 'Fetch{0}FromCache'.format(self.plural_object_name)

            if not fetch_command.is_plural:
                if len(by_list) == 0:
                    skr_log_warning('Singular often comes with at least one by parameter')
                declaration += 'JNIEXPORT jlong JNICALL Java_com_lesschat_core_{0}_{1}_native'. \
                    format(self.group_name, self.manager_name)
                declaration += fetch_fun_name + bys

            else:
                declaration += 'JNIEXPORT jlongArray JNICALL Java_com_lesschat_core_{0}_{1}_native'. \
                    format(self.group_name, self.manager_name)
                declaration += fetch_fun_name + bys
        return declaration

    def generate_fetch_implementations(self, version, config):
        """Gets fetch implementation of JNI manager code.

        Args:
            version: A float version number of <JniModelXmlParser>.
            config: A <Config> object describes user-defined names.

        Returns:
            A string which is fetch implementation of JNI manager code.
        """
        impl = ''
        for fetch_command in self.fetch_commands:
            if version < 5.0:
                impl += self.__fetch_implementation(fetch_command)
            else:
                impl += self.__fetch_implementation_v2(fetch_command, config)
            impl += _JNI_BR
        return impl

    def __fetch_implementation_v2(self, fetch_command, config):
        by_list = []
        impl = ''
        if fetch_command.where != '':
            by_list = re.split(',', fetch_command.where)

        bys = self.__convert_bys_to_string_impl(by_list, self.fetch_has_sign)

        if fetch_command.alias != '':
            fetch_fun_name = fetch_command.alias
        elif not fetch_command.is_plural:
            fetch_fun_name = 'Fetch{0}FromCache'.format(self.object_name)
        else:
            fetch_fun_name = 'Fetch{0}FromCache'.format(self.plural_object_name)

        if not fetch_command.is_plural:
            if len(by_list) == 0:
                skr_log_warning('Singular often comes with at least one by parameter')
            impl += 'JNIEXPORT jobject JNICALL Java_{2}_{0}_{1}_native' \
                .format(self.group_name, self.manager_name, config.jni_package_path)
            impl += fetch_fun_name + bys
            impl += _JNI_SPACE + 'const {1}::{0}* coreManager = reinterpret_cast<{1}::{0}*>(handler);' \
                .format(self.manager_name, config.cpp_namespace)
            impl += _JNI_BR

            cpp_method_param = ''
            for by_string in by_list:
                jni_var = self.__jni_var_by_name(by_string)
                if jni_var is not None:
                    impl += _JNI_SPACE + jni_var.var_type.to_getter_string() + " cpp" + jni_var.to_param_style_name()
                    impl += ' = ' + jni_var.cpp_variable_from_jni_variable(jni_var.to_param_style_name(), config) + ';'
                    cpp_method_param += 'cpp' + jni_var.to_param_style_name() + ', '
            impl += _JNI_BR
            if len(by_list) == 1:
                cpp_method_by = 'By' + jni_var.to_title_style_name()
            else:
                cpp_method_by = ''

            cpp_method_name = fetch_fun_name + cpp_method_by
            cpp_method_param = cpp_method_param[:-2]
            impl += _JNI_SPACE + 'std::unique_ptr<{3}::{0}> coreObject = coreManager->{1}({2});\n\n' \
                .format(self.object_name, cpp_method_name, cpp_method_param, config.cpp_namespace)
            impl += _JNI_SPACE + 'if(coreObject == nullptr){\n    return NULL;\n  }\n'
            impl += _JNI_SPACE + 'return {1}::JniHelper::GetJ{0}ByCore{0}(*coreObject);\n}}'.format(self.object_name,
                                                                                                    config.cpp_namespace)
        else:
            impl += 'JNIEXPORT jobjectArray JNICALL Java_{2}_{0}_{1}_native' \
                .format(self.group_name, self.manager_name, config.jni_package_path)
            impl += fetch_fun_name + bys
            impl += _JNI_SPACE + 'const {1}::{0}* coreManager = reinterpret_cast<{1}::{0}*>(handler);' \
                .format(self.manager_name, config.cpp_namespace)
            impl += _JNI_BR

            cpp_method_param = ''
            for by_string in by_list:
                jni_var = self.__jni_var_by_name(by_string)
                if jni_var is not None:
                    impl += _JNI_SPACE + jni_var.to_getter_string() + " cpp" + jni_var.to_param_style_name()
                    impl += ' = ' + jni_var.cpp_variable_from_jni_variable(jni_var.to_param_style_name(), config) + ';\n'
                    cpp_method_param += 'cpp' + jni_var.to_param_style_name() + ', '
            if len(by_list) == 1:
                cpp_method_by = 'By' + jni_var.to_title_style_name()
            else:
                cpp_method_by = ''

            cpp_method_name = fetch_fun_name + cpp_method_by
            cpp_method_param = cpp_method_param[:-2]
            impl += _JNI_SPACE
            impl += 'std::vector<std::unique_ptr<{3}::{0}>> coreObjects = coreManager->{1}({2});\n\n' \
                .format(self.object_name, cpp_method_name, cpp_method_param, config.cpp_namespace)
            impl += _JNI_SPACE + 'return {1}::JniHelper::GetJ{0}sArrayByCore{0}s(coreObjects);\n}}'.format(
                self.object_name, config.cpp_namespace)
        return impl

    def __fetch_implementation(self, fetch_command):
        by_list = []
        impl = ''
        if fetch_command.where != '':
            by_list = re.split(',', fetch_command.where)

        bys = self.__convert_bys_to_string_impl(by_list, self.fetch_has_sign)

        if fetch_command.alias != '':
            fetch_fun_name = fetch_command.alias
        elif not fetch_command.is_plural:
            fetch_fun_name = 'Fetch{0}FromCache'.format(self.object_name)
        else:
            fetch_fun_name = 'Fetch{0}FromCache'.format(self.plural_object_name)

        if not fetch_command.is_plural:
            if len(by_list) == 0:
                skr_log_warning('Singular often comes with at least one by parameter')
            impl += 'JNIEXPORT jlong JNICALL Java_com_lesschat_core_{0}_{1}_native' \
                .format(self.group_name, self.manager_name)
            impl += fetch_fun_name + bys
            impl += _JNI_SPACE + 'const lesschat::{0}* core_manager = reinterpret_cast<lesschat::{0}*>(handler);' \
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

            cpp_method_name = fetch_fun_name + cpp_method_by
            cpp_method_param = cpp_method_param[:-2]
            impl += _JNI_SPACE + 'std::unique_ptr<lesschat::{0}> core_object = core_manager->{1}({2});\n\n' \
                .format(self.object_name, cpp_method_name, cpp_method_param)
            impl += _JNI_SPACE + 'if(core_object == nullptr){\n    return 0;\n  }\n'
            impl += _JNI_SPACE + 'return reinterpret_cast<long>(core_object.release());\n}'

        else:
            impl += 'JNIEXPORT jlongArray JNICALL Java_com_lesschat_core_{0}_{1}_native' \
                .format(self.group_name, self.manager_name)
            impl += fetch_fun_name + bys
            impl += _JNI_SPACE + 'const lesschat::{0}* core_manager = reinterpret_cast<lesschat::{0}*>(handler);' \
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

            cpp_method_name = fetch_fun_name + cpp_method_by
            cpp_method_param = cpp_method_param[:-2]
            impl += _JNI_SPACE
            impl += 'std::vector<std::unique_ptr<lesschat::{0}>> core_objects = core_manager->{1}({2});\n\n' \
                .format(self.object_name, cpp_method_name, cpp_method_param)
            impl += _JNI_SPACE + 'return lesschat::JniHelper::JlongArrayFromNativeArray(std::move(core_objects));\n}'
        return impl

    def generate_http_function_declarations(self):
        declaration = ''
        for api in self.apis:
            declaration += '/*\n'
            declaration += ' * Class:     com_lesschat_core_{0}_{1}\n'.format(self.group_name, self.manager_name)
            declaration += ' * Method:    native{0}\n'.format(api.function_name)
            signature = 'J'
            for input_var in api.input_var_list:
                signature += input_var.var_type.to_jni_sign_getter_string()
            declaration += ' * Signature: ({0})V\n'.format(signature)
            declaration += ' */\n'

            declaration += 'JNIEXPORT void JNICALL Java_com_lesschat_core_{0}_{1}_native{2}\n'\
                .format(self.group_name, self.manager_name, api.function_name)
            declaration += '  (JNIEnv*, jobject, jlong'
            for input_var in api.input_var_list:
                declaration += ', {0}'.format(input_var.var_type.to_jni_getter_string())
            declaration += ');\n\n'
        return declaration

    def generate_http_function_implementations(self, config):
        """Generates HTTP - Cache methods.

        Args:
            config: A <Config> object represents user-defined config including namespace and package path.

        Returns:
            A string that is JNI http methods.
        """
        namespace = config.cpp_namespace
        implementation = ''
        for api in self.apis:
            implementation += 'JNIEXPORT void JNICALL Java_{3}_{0}_{1}_native{2}\n'\
                .format(self.group_name, self.manager_name, api.function_name, config.jni_package_path)
            implementation += '  (JNIEnv* env, jobject thiz, jlong handler'
            for input_var in api.input_var_list:
                implementation += ', {0} {1}'.format(input_var.var_type.to_jni_getter_string(),
                                                     input_var.to_param_style_name())
            implementation += ') {\n'
            implementation += function_space(1) + 'const {1}::{0}* core_manager = ' \
                                                  'reinterpret_cast<{1}::{0}*>(handler);\n\n' \
                .format(self.manager_name, namespace)
            implementation += function_space(1) + 'jobject global_thiz = env->NewGlobalRef(thiz);\n'
            implementation += function_space(1) + 'jobject global_null = env->NewGlobalRef(NULL);\n\n'
            for input_var in api.input_var_list:
                implementation += _JNI_SPACE + input_var.to_getter_string() + " cpp_" + input_var.to_param_style_name()
                implementation += ' = ' + input_var.cpp_variable_from_jni_variable(input_var.to_param_style_name(), config)
                implementation += ';\n'
            implementation += '\n'

            implementation += function_space(1) + 'core_manager->{0}('.format(api.function_name)
            space_length = len(function_space(1) + 'core_manager->{0}('.format(api.function_name))
            space = ''
            for i in range(space_length):
                space += " "
            index = 0
            for input_var in api.input_var_list:
                if index == 0:
                    implementation += 'cpp_{0},\n'.format(input_var.to_param_style_name())
                else:
                    implementation += space + 'cpp_{0},\n'.format(input_var.to_param_style_name())
                index += 1

            if len(api.input_var_list) > 0:
                implementation += space + '[env, global_thiz, global_null]('
            else:
                implementation += '[env, global_thiz, global_null]('
            space_length = len('[env, global_thiz, global_null](')
            for i in range(space_length):
                space += " "
            implementation += 'bool success,\n'
            implementation += space + '{0} error'.format(config.cpp_error_type)
            for i in range(len(api.output_var_list)):
                implementation += ',\n{0}{1} {2}'.format(space,
                                                         api.output_var_list[i].to_getter_string(namespace),
                                                         api.output_var_list[i].name)
            implementation += '){\n'

            implementation += function_space(2) + 'JNIEnv *jni_env = {0}::JniHelper::GetJniEnv();\n'.format(namespace)
            implementation += function_space(2) + 'jclass jclazz = jni_env->GetObjectClass(global_thiz);\n\n'
            implementation += function_space(2) + 'if(jclazz == NULL) {\n'
            implementation += function_space(3) + 'return;\n'
            implementation += function_space(2) + '}\n'
            java_callback_function_name_str = 'on{0}'.format(api.function_name)
            java_callback_function_sign_str = 'ZLjava/lang/String;'
            for output_var in api.output_var_list:
                java_callback_function_sign_str += output_var.var_type.to_jni_signature_v2()
            implementation += function_space(2) + 'jmethodID method_id = jni_env->GetMethodID(jclazz, "{0}", "({1})V");\n'\
                .format(java_callback_function_name_str, java_callback_function_sign_str)
            implementation += function_space(2) + 'if(method_id == NULL) {\n'
            implementation += function_space(3) + 'return;\n'
            implementation += function_space(2) + '}\n'

            # TODO(lin.xiaoe.f@gmail.com): We should improve it in future.
            if config.cpp_error_type == 'const std::string&':
                implementation += function_space(2) + 'jstring jerror = jni_env->NewStringUTF(error.c_str());\n\n'
            elif config.cpp_error_type == 'WebApi::Error':
                implementation += function_space(2) + 'jstring jerror = jni_env->NewStringUTF(error.description.c_str());\n\n'
            else:
                skr_log_warning('This is a tmp ugly implementation, you should support your own type here.')

            if len(api.output_var_list) != 0:
                implementation += function_space(2) + 'if (success){\n'
                implementation += function_space(3) + 'jni_env->CallVoidMethod(global_thiz, method_id, success, jerror'
                space_length = len(function_space(3) + 'jni_env->CallVoidMethod(')
                space = ''
                for i in range(space_length):
                    space += " "
                for output_var in api.output_var_list:
                    implementation += ',\n' + space + output_var.jni_variable_from_cpp_variable_v2(output_var.name,
                                                                                                   namespace)
                implementation += ');\n'

                implementation += function_space(2) + '} else {\n'
                implementation += function_space(3) + 'jni_env->CallVoidMethod(global_thiz, method_id, success, jerror'
                for output_var in api.output_var_list:
                    implementation += ', global_null'
                implementation += ');\n'
                implementation += function_space(2) + '}\n\n'
            else:
                implementation += function_space(2) + 'jni_env->CallVoidMethod(global_thiz, method_id, success, jerror);\n\n'

            implementation += function_space(2) + 'jni_env->DeleteGlobalRef(global_thiz);\n'
            implementation += function_space(2) + 'jni_env->DeleteGlobalRef(global_null);\n'
            implementation += function_space(1) + '});\n'
            implementation += '}\n\n'
        return implementation

    def __convert_bys_to_string(self, by_string_list, has_sign):
        """Returns "ById" or "".
        """
        if len(by_string_list) == 0:  # empty string
            if has_sign:
                return '__J\n  (JNIEnv *, jobject, jlong);\n\n'
            else:
                return '\n  (JNIEnv *, jobject, jlong);\n\n'
        elif len(by_string_list) == 1:  # "ById(const std::string& id)"
            by_string = by_string_list[0]
            jni_var = self.__jni_var_by_name(by_string)
            if jni_var is not None:
                return 'By{0}\n  (JNIEnv *, jobject, jlong, {1});\n\n' \
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
                return 'By{0}\n  (JNIEnv *env, jobject thiz, jlong handler, {1} {2}){{\n' \
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

    def __jni_var_by_name(self, name_string):
        """Returns <JniVariable> object or None if not found.
        """
        for jni_var in self.jni_variable_list:
            if jni_var.name == name_string:
                return jni_var
        return None
