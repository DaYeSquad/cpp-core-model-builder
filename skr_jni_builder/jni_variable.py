from skr_cpp_builder.cpp_variable import VarType
from skrutil import string_utils


class JniVariable:

    def __init__(self, name, var_type_string, group_name, class_name):
        var_type = VarType.type_from_string(var_type_string)

        self.name = name
        self.var_type = VarType(var_type)
        self.group_name = group_name
        self.class_name = class_name

    def getter(self):
        return self.getter_method_name() + '\n' + '  (JNIEnv *, jobject, jlong);'

    def set_enum_class_name(self, enum_class_name):
        self.var_type.set_enum_class_name(enum_class_name)

    def getter_method_name(self):
        title_style_name = string_utils.to_title_style_name(self.name)
        if self.var_type == VarType.cpp_bool:
            method_name = 'JNIEXPORT {0} JNICALL Java_com_lesschat_core_{1}_{2}_nativeIs{3}'.\
                format(self.var_type.to_jni_getter_string(), self.group_name, self.class_name, title_style_name)
            return method_name
        else:
            method_name = 'JNIEXPORT {0} JNICALL Java_com_lesschat_core_{1}_{2}_nativeGet{3}'.\
                format(self.var_type.to_jni_getter_string(), self.group_name, self.class_name,  title_style_name)
            return method_name

    def getter_impl(self):
        method_name = self.getter_method_name()
        para_name = '  (JNIEnv *env, jobject thiz, jlong handler)'
        step_1 = 'lesschat::{0}* {1} = reinterpret_cast<lesschat::{0}*>(handler);'\
            .format(self.class_name, string_utils.first_char_to_lower(self.class_name))
        cpp_return = '{0}->{1}()'.format(string_utils.first_char_to_lower(self.class_name), self.cpp_method())
        step_2 = 'return {0};'.format(self.jni_variable_from_cpp_variable(cpp_return))
        return method_name + '\n' + para_name + '{{\n  {0}\n  {1}\n}}'.format(step_1, step_2)

    def jni_variable_from_cpp_variable(self, return_variable):
        if self.var_type == VarType.cpp_bool:
            return return_variable
        elif self.var_type == VarType.cpp_enum:
            return 'static_cast<jint>({0})'.format(return_variable)
        elif self.var_type == VarType.cpp_int:
            return 'static_cast<jint>({0})'.format(return_variable)
        elif self.var_type == VarType.cpp_string:
            return 'env->NewStringUTF({0}.c_str())'.format(return_variable)
        elif self.var_type == VarType.cpp_string_array:
            return 'lesschat::JniHelper::JobjectArrayFromStringVector({0})'.format(return_variable)
        elif self.var_type == VarType.cpp_time:
            return 'static_cast<jlong>({0}) * 1000'.format(return_variable)

    def to_getter_string(self):
        if self.var_type.value == 4:
            return 'lesschat::' + self.var_type.cpp_enum_type_string()
        else:
            return self.var_type.to_getter_string();

    def cpp_variable_from_jni_variable(self, return_variable):
        if self.var_type == VarType.cpp_bool:
            return 'static_cast<bool>({0})'.format(return_variable)
        elif self.var_type == VarType.cpp_enum:
            return 'static_cast<lesschat::{0}>({1})'.format(self.var_type.to_getter_string(), return_variable)
        elif self.var_type == VarType.cpp_int:
            return return_variable
        elif self.var_type == VarType.cpp_string:
            return 'lesschat::JniHelper::StringFromJstring({0})'.format(return_variable)
        elif self.var_type == VarType.cpp_string_array:
            return 'lesschat::JniHelper::StringVectorFromJobjectArray({0})'.format(return_variable)
        elif self.var_type == VarType.cpp_time:
            return 'static_cast<time_t>({0} / 1000)'.format(return_variable)

    def cpp_method(self):
        if self.var_type == VarType.cpp_bool:
            return 'is_{0}'.format(self.name)
        else:
            return self.name

    # from 'display_name' to 'DisplayName'
    def to_title_style_name(self):
        return string_utils.to_title_style_name(self.name)

    # from 'display_name' to 'displayName'
    def to_param_style_name(self):
        return string_utils.to_objc_property_name(self.name)

    def jni_variable_name(self):
        return self.var_type.to_jni_getter_string()

    def jni_variable_sign_name(self):
        return self.var_type.to_jni_sign_getter_string()

