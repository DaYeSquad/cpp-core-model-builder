#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - Frank Lin

from skrutil import string_utils
from skrutil.string_utils import indent

_JNI_BR = '\n\n'
_JNI_SPACE = '  '


class JniClass:
    """JNI part generator, responsible for generating JNI source code for Object and ObjectManager.
    """

    def __init__(self, group_name, class_name, jni_variable_list, jni_manager_or_none):
        """Init JniClass with necessary parameters.

        Args:
            group_name: A string which is the C++ folder name.
            class_name: A string which is the C++ class name.
            jni_variable_list: List of <JniVariable>.
            jni_manager_or_none: <JniManager>.
        """
        self.__group_name = group_name
        self.__class_name = class_name
        self.__jni_var_list = jni_variable_list
        self.__jni_manager_or_none = jni_manager_or_none

        if self.__jni_manager_or_none is not None:
            self.__jni_manager_or_none.set_object_name(class_name, class_name + 's')
            self.__jni_manager_or_none.set_jni_variable_list(jni_variable_list)
            self.__jni_manager_or_none.set_group_name(group_name)

        self.__def_cpp = '#ifdef __cplusplus\nextern "C" {\n#endif'
        self.__end_def_cpp = '#ifdef __cplusplus\n}\n#endif'

    def generate_header(self):
        """Gets JNI object header. It is not required, so since 5.0, we don't use this method anymore.

        Returns:
            A string which is the declaration of JNI object header.
        """
        file_name = 'com_lesschat_core_{0}_{1}.h'.format(self.__group_name, self.__class_name)
        file_path = 'build/jni/' + file_name
        output_header = open(file_path, 'w')

        def_guard = '#ifndef _Included_com_lesschat_core_{0}_{1}\n#define _Included_com_lesschat_core_{0}_{1}'.format(
                self.__group_name, self.__class_name)

        end_def_guard = '#endif'

        output_header.write('#include <jni.h>')
        output_header.write(_JNI_BR)
        output_header.write(def_guard + '\n')
        output_header.write(self.__def_cpp + _JNI_BR)

        # release method
        output_header.write(self.__release())
        output_header.write(_JNI_BR)

        for jni_var in self.__jni_var_list:
            output_header.write(jni_var.getter())
            output_header.write(_JNI_BR)

        output_header.write(_JNI_BR)
        output_header.write(self.__end_def_cpp + '\n')
        output_header.write(end_def_guard + '\n')

    def generate_implementation(self):
        """Gets JNI implementation which is used before 4.0.

        Returns:
            A string which is JNI object implementation.
        """
        file_name = 'com_lesschat_core_{0}_{1}.cc'.format(self.__group_name, self.__class_name)
        file_path = 'build/jni/' + file_name
        output_header = open(file_path, 'w')

        style_class_name = string_utils.cpp_class_name_to_cpp_file_name(self.__class_name)
        header_name = 'com_lesschat_core_{0}_{1}.h'.format(self.__group_name, self.__class_name)
        cpp_name = '{0}/{1}.h'.format(self.__group_name, style_class_name)
        output_header.write('#include "{0}"'.format(header_name) + '\n')
        output_header.write('#include "{0}"'.format(cpp_name) + '\n')
        output_header.write('#include "utils/android/jni_helper.h"')

        output_header.write(_JNI_BR)
        output_header.write(self.__def_cpp + _JNI_BR)

        # release method
        output_header.write(self.__release_impl())
        output_header.write(_JNI_BR)

        for jni_var in self.__jni_var_list:
            output_header.write(jni_var.getter_impl())
            output_header.write(_JNI_BR)

        output_header.write(self.__end_def_cpp)

    def generate_jni_helper_implementation(self, config):
        """Gets JNI helper object converting method implementation & declaration.

        Returns:
            A string which is JNI helper object converting method implementation & declaration.
        """
        file_name = 'jni_helper_{0}.cc'.format(self.__class_name)
        file_path = 'build/jni/' + file_name
        output_cc = open(file_path, 'w')

        impl = '// Copy belows to core/utils/android/jni_helper.h\n\n\n'

        impl += '{0}\n\n'.format(self.__jni_get_jobject_by_core_object_declaration())
        impl += self.__jni_get_jobjects_array_by_core_objects_declaration() + '\n'
        impl += '\n\n\n'

        impl += '// Copy belows to core/utils/android/jni_helper.cc\n\n\n'
        impl += self.__jni_get_jobject_by_core_object_implementation(config)

        impl += '\n\n'
        impl += self.__jni_get_jobjects_array_by_core_objects_implementation()
        impl += '\n'

        output_cc.write(impl)

    def generate_manager_header(self):
        """Gets JNI object manager header. It is not required, so since 5.0, we don't use this method anymore.

        Returns:
            A string which is the declaration of JNI object manager header.
        """
        if self.__jni_manager_or_none is None:
            return

        jni_manager = self.__jni_manager_or_none

        file_name = 'com_lesschat_core_{0}_{1}Manager.h'.format(self.__group_name, self.__class_name)
        file_path = 'build/jni/' + file_name
        output_header = open(file_path, 'w')

        def_header = '#ifndef _Included_com_lesschat_core_{0}_{1}Manager\n' \
                     '#define _Included_com_lesschat_core_{0}_{1}Manager'
        def_guard = def_header.format(self.__group_name, self.__class_name)
        end_def_guard = '#endif'

        output_header.write('#include <jni.h>' + _JNI_BR)
        output_header.write(def_guard + '\n')
        output_header.write(self.__def_cpp + _JNI_BR)

        output_header.write(jni_manager.generate_fetch_declarations())
        output_header.write(jni_manager.generate_http_function_declarations())

        output_header.write(self.__end_def_cpp + '\n')
        output_header.write(end_def_guard + '\n')

    def generate_manager_implementation(self, version, config):
        """Gets JNI object manager implementation.

        Args:
            version: A float version number of <JniModelXmlParser>.
            config: A <Config> object describes user-defined names.

        Returns:
            A string which is JNI object manager implementation.
        """
        if self.__jni_manager_or_none is None:
            return

        jni_manager = self.__jni_manager_or_none

        file_name = '{2}_{0}_{1}Manager.cc'.format(self.__group_name, self.__class_name, config.jni_package_path)
        file_path = 'build/jni/' + file_name
        output_header = open(file_path, 'w')

        header_name = '#include "{2}_{0}_{1}Manager.h"\n'.format(self.__group_name,
                                                                 self.__class_name,
                                                                 config.jni_package_path)
        cpp_name = '#include "{0}/{1}_manager.h"\n'\
            .format(self.__group_name, string_utils.cpp_class_name_to_cpp_file_name(self.__class_name))

        output_header.write(header_name)
        output_header.write(cpp_name)
        output_header.write('#include "utils/android/jni_helper.h"')
        output_header.write(_JNI_BR)

        output_header.write(self.__def_cpp)
        output_header.write(_JNI_BR)

        output_header.write(jni_manager.generate_fetch_implementations(version, config))
        output_header.write(jni_manager.generate_http_function_implementations())

        output_header.write(self.__end_def_cpp + '\n')

    def __release(self):
        return self.__release_method_name() + '\n' + '  (JNIEnv *, jobject, jlong);'

    def __release_method_name(self):
        return 'JNIEXPORT void JNICALL Java_com_lesschat_core_{0}_{1}_nativeRelease{1}'.\
            format(self.__group_name, self.__class_name)

    def __release_impl(self):
        method_name = self.__release_method_name()
        para_name = '  (JNIEnv *env, jobject thiz, jlong handler)'
        step_1 = 'lesschat::{0}* {1} = reinterpret_cast<lesschat::{0}*>(handler);'\
            .format(self.__class_name, string_utils.first_char_to_lower(self.__class_name))
        step_2 = 'LCC_SAFE_DELETE({0});'.format(string_utils.first_char_to_lower(self.__class_name))
        return method_name + '\n' + para_name + '{{\n  {0}\n  {1}\n}}'.format(step_1, step_2)

    def __jni_get_jobject_by_core_object_declaration(self):
        return 'static jobject GetJ{0}ByCore{0}(const {0}& {1});'.format(
            self.__class_name, string_utils.cpp_class_name_to_cpp_file_name(self.__class_name))

    def __jni_get_jobject_by_core_object_implementation(self, config):
        impl = 'jobject JniHelper::GetJ{0}ByCore{0}(const lesschat::{0}& {1}) {{\n'.format(
            self.__class_name, string_utils.cpp_class_name_to_cpp_file_name(self.__class_name))
        impl += indent(2) + 'JNIEnv* env = GetJniEnv();\n'
        impl += indent(2) + 'if (!env) {\n'
        impl += indent(4) + 'sakura::log_error("Failed to get JNIEnv");\n'
        impl += indent(4) + 'return nullptr;\n'
        impl += indent(2) + '}\n\n'
        impl += indent(2) + 'jclass {0}Jclass = JniReferenceCache::SharedCache()->{1}_jclass();\n'.format(
            string_utils.first_char_to_lower(self.__class_name),
            string_utils.cpp_class_name_to_cpp_file_name(self.__class_name))
        impl += indent(2) + 'jmethodID {0}ConstructorMethodID = env->GetMethodID({0}Jclass, "<init>", "('.format(
            string_utils.first_char_to_lower(self.__class_name))
        for jni_var in self.__jni_var_list:
            impl += jni_var.var_type.to_jni_signature()
        impl += ')V");\n\n'

        for jni_var in self.__jni_var_list:
            impl += indent(2) + jni_var.jni_var_assignment_by_cpp_variable(config) + '\n'

        impl += '\n'

        constructor_fst_line = indent(2) + 'jobject j{0}Object = env->NewObject('.format(self.__class_name)
        num_constructor_indent = len(constructor_fst_line)

        impl += constructor_fst_line

        parameters = []
        jclass_instance_name = '{0}Jclass'.format(string_utils.first_char_to_lower(self.__class_name))
        constructor_method_id = '{0}ConstructorMethodID'.format(string_utils.first_char_to_lower(self.__class_name))
        parameters.append(constructor_method_id)
        for jni_var in self.__jni_var_list:
            parameters.append('j{0}'.format(string_utils.to_title_style_name(jni_var.name)))

        impl += jclass_instance_name + ',\n'
        for parameter in parameters:
            impl += indent(num_constructor_indent) + parameter + ',\n'
        impl = impl[:-2]
        impl += ');'
        impl += '\n'

        for jni_var in self.__jni_var_list:
            delete_method = jni_var.jni_delete_local_ref()
            if delete_method != '':
                impl += indent(2) + delete_method + '\n'
        impl += '\n'

        impl += indent(2) + 'return j{0}Object;'.format(self.__class_name)
        impl += '\n'
        impl += '}\n'
        impl += '\n'
        return impl

    def __jni_get_jobjects_array_by_core_objects_declaration(self):
        return 'static jobjectArray GetJ{0}sArrayByCore{0}s(const std::vector<std::unique_ptr<{0}>>& {1}s);'.format(
            self.__class_name, string_utils.cpp_class_name_to_cpp_file_name(self.__class_name))

    def __jni_get_jobjects_array_by_core_objects_implementation(self):
        object_name = string_utils.cpp_class_name_to_cpp_file_name(self.__class_name)

        impl = 'jobjectArray JniHelper::GetJ{0}sArrayByCore{0}s(const std::vector<std::unique_ptr<{0}>>& {1}s) {{'.format(
            self.__class_name, object_name)

        impl += '\n'
        impl += indent(2) + 'jclass {0}Jclass = JniReferenceCache::SharedCache()->{1}_jclass();\n'.format(
            string_utils.first_char_to_lower(self.__class_name),
            object_name)

        impl += indent(2) + 'JNIEnv* env = GetJniEnv();\n'
        impl += indent(2) + 'if (!env) {\n'
        impl += indent(4) + 'return env->NewObjectArray(0, {0}Jclass, NULL);\n'.format(
            string_utils.first_char_to_lower(self.__class_name))
        impl += indent(2) + '}\n\n'
        impl += indent(2) + 'jobjectArray jobjs = env->NewObjectArray({0}s.size(), {1}Jclass, NULL);\n\n'.format(
            object_name,
            string_utils.first_char_to_lower(self.__class_name))

        impl += indent(2) + 'jsize i = 0;\n'
        impl += indent(2) + 'for (auto it = {0}s.begin(); it != {0}s.end(); ++it) {{\n'.format(object_name)
        impl += indent(4) + 'jobject j{0} = GetJ{0}ByCore{0}(**it);\n'.format(self.__class_name)
        impl += indent(4) + 'env->SetObjectArrayElement(jobjs, i, j{0});\n'.format(self.__class_name)
        impl += indent(4) + 'env->DeleteLocalRef(j{0});\n'.format(self.__class_name)
        impl += indent(4) + '++i;\n'
        impl += indent(2) + '}\n'
        impl += indent(2) + 'return jobjs;\n'
        impl += '}'
        return impl
