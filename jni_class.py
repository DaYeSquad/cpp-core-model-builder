from cpp_class import CppClass
import string_utils

_JNI_BR = '\n\n'
_JNI_SPACE = '  '


class JniClass:
    def __init__(self, group_name, class_name, jni_variable_list, jni_manager_or_none):
        self.group_name = group_name
        self.class_name = class_name
        self.jni_var_list = jni_variable_list
        self.jni_manager_or_none = jni_manager_or_none

        if self.jni_manager_or_none is not None:
            self.jni_manager_or_none.set_object_name(class_name, class_name + 's')
            self.jni_manager_or_none.set_jni_variable_list(jni_variable_list)
            self.jni_manager_or_none.set_group_name(group_name)

        self.def_cpp = '#ifdef __cplusplus\nextern "C" {\n#endif'
        self.end_def_cpp = '#ifdef __cplusplus\n}\n#endif'

    def generate_header(self):
        file_name = 'com_lesschat_core_{0}_{1}.h'.format(self.group_name, self.class_name)
        file_path = 'jni/' + file_name
        output_header = open(file_path, 'w')

        def_guard = '#ifndef _Included_com_lesschat_core_{0}_{1}\n#define _Included_com_lesschat_core_{0}_{1}'.format(
                self.group_name, self.class_name)

        end_def_guard = '#endif'

        output_header.write('#include <jni.h>')
        output_header.write(_JNI_BR)
        output_header.write(def_guard + '\n')
        output_header.write(self.def_cpp + _JNI_BR)

        # create method
        # output_header.write(self.create())
        # output_header.write(_JNI_BR)

        # release method
        output_header.write(self.release())
        output_header.write(_JNI_BR)

        for jni_var in self.jni_var_list:
            output_header.write(jni_var.getter())
            output_header.write(_JNI_BR)

        output_header.write(_JNI_BR)
        output_header.write(self.end_def_cpp + '\n')
        output_header.write(end_def_guard + '\n')

    def generate_implementation(self):
        file_name = 'com_lesschat_core_{0}_{1}.cc'.format(self.group_name, self.class_name)
        file_path = 'jni/' + file_name
        output_header = open(file_path, 'w')

        style_class_name = string_utils.cpp_class_name_to_cpp_file_name(self.class_name)
        header_name = 'com_lesschat_core_{0}_{1}.h'.format(self.group_name, self.class_name)
        cpp_name = '{0}/{1}.h'.format(self.group_name, style_class_name)
        output_header.write('#include "{0}"'.format(header_name) + '\n')
        output_header.write('#include "{0}"'.format(cpp_name) + '\n')
        output_header.write('#include "utils/android/jni_helper.h"')

        output_header.write(_JNI_BR)
        output_header.write(self.def_cpp + _JNI_BR)

        # create method
        # output_header.write(self.create_impl())
        # output_header.write(_JNI_BR)

        # release method
        output_header.write(self.release_impl())
        output_header.write(_JNI_BR)

        for jni_var in self.jni_var_list:
            output_header.write(jni_var.getter_impl())
            output_header.write(_JNI_BR)

        output_header.write(self.end_def_cpp)

    def generate_manager_header(self):

        if self.jni_manager_or_none is None:
            return

        jni_manager = self.jni_manager_or_none

        file_name = 'com_lesschat_core_{0}_{1}Manager.h'.format(self.group_name, self.class_name)
        file_path = 'jni/' + file_name
        output_header = open(file_path, 'w')

        def_header = '#ifndef _Included_com_lesschat_core_{0}_{1}Manager\n' \
                     '#define _Included_com_lesschat_core_{0}_{1}Manager'
        def_guard = def_header.format(self.group_name, self.class_name)
        end_def_guard = '#endif'

        output_header.write('#include <jni.h>' + _JNI_BR)
        output_header.write(def_guard + '\n')
        output_header.write(self.def_cpp + _JNI_BR)

        output_header.write(jni_manager.generate_fetch_declarations())

        output_header.write(self.end_def_cpp + '\n')
        output_header.write(end_def_guard + '\n')

    def generate_manager_implementation(self):
        if self.jni_manager_or_none is None:
            return

        jni_manager = self.jni_manager_or_none

        file_name = 'com_lesschat_core_{0}_{1}Manager.cc'.format(self.group_name, self.class_name)
        file_path = 'jni/' + file_name
        output_header = open(file_path, 'w')

        header_name = '#include "com_lesschat_core_{0}_{1}Manager.h"\n'.format(self.group_name, self.class_name)
        cpp_name = '#include "{0}/{1}_manager.h"\n'\
            .format(self.group_name, CppClass.convert_class_name_to_file_name(self.class_name))

        output_header.write(header_name)
        output_header.write(cpp_name)
        output_header.write('#include "utils/android/jni_helper.h"')
        output_header.write(_JNI_BR)

        output_header.write(self.def_cpp)
        output_header.write(_JNI_BR)

        output_header.write(jni_manager.generate_fetch_implementations())

        output_header.write(self.end_def_cpp + '\n')

    def release(self):
        return self.release_method_name() + '\n' + '  (JNIEnv *, jobject, jlong);'

    def release_method_name(self):
        return 'JNIEXPORT void JNICALL Java_com_lesschat_core_{0}_{1}_nativeRelease{1}'.\
            format(self.group_name, self.class_name)

    # def create(self):
    #     return self.create_method_name() + '\n' + '  (JNIEnv *, jobject);'
    #
    # def create_method_name(self):
    #     return 'JNIEXPORT jlong JNICALL Java_com_lesschat_core_{0}_{1}_nativeCreate{1}'.\
    #         format(self.group_name, self.class_name)
    #
    # def create_impl(self):
    #     method_name = self.create_method_name()
    #     para_name = '  (JNIEnv *env, jobject thiz)'
    #     step_1 = 'lesschat::{0}* {1} = new lesschat::{0}();'\
    #         .format(self.class_name, string_utils.first_char_to_lower(self.class_name))
    #     step_2 = 'return reinterpret_cast<jlong>({0});'.format(string_utils.first_char_to_lower(self.class_name))
    #     return method_name + '\n' + para_name + '{{\n  {0}\n  {1}\n}}'.format(step_1, step_2)

    def release_impl(self):
        method_name = self.release_method_name()
        para_name = '  (JNIEnv *env, jobject thiz, jlong handler)'
        step_1 = 'lesschat::{0}* {1} = reinterpret_cast<lesschat::{0}*>(handler);'\
            .format(self.class_name, string_utils.first_char_to_lower(self.class_name))
        step_2 = 'LCC_SAFE_DELETE({0});'.format(string_utils.first_char_to_lower(self.class_name))
        return method_name + '\n' + para_name + '{{\n  {0}\n  {1}\n}}'.format(step_1, step_2)


