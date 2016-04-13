from skr_cpp_builder.cpp_variable import VarType
from skrutil import string_utils
from skrutil import skr_logger


class JniVariable:
    """JNI variable that provides JNI related method.
    """

    def __init__(self, name, var_type_string, group_name, class_name):
        """Init JNI variable with necessary parameters.

        Args:
            name: A string which is variable name.
            var_type_string: A string which describes the variable type.
            group_name: A string which is C++ folder name (aka package name in Java).
            class_name: A string which is class name in Java.
        """
        self.__var_type = VarType.instance_from_string(var_type_string)
        self.__name = name
        self.__group_name = group_name
        self.__class_name = class_name

    def set_enum_class_name(self, enum_class_name):
        """Sets enum class name is the class is enum type.

        Args:
            enum_class_name: A string which is enum class name.
        """
        self.__var_type.set_enum_class_name(enum_class_name)

    def getter(self):
        """Generate getter declaration before 5.0.

        Returns:
            A string which is native getter declaration before 5.0.
        """
        return self.__getter_method_name() + '\n' + '  (JNIEnv *, jobject, jlong);'

    def getter_impl(self):
        """Generate getter implementation before 5.0.

        Returns:
            A string which is native getter implementation before 5.0.
        """
        method_name = self.__getter_method_name()
        para_name = '  (JNIEnv *env, jobject thiz, jlong handler)'
        step_1 = 'lesschat::{0}* {1} = reinterpret_cast<lesschat::{0}*>(handler);' \
            .format(self.__class_name, string_utils.first_char_to_lower(self.__class_name))
        cpp_return = '{0}->{1}()'.format(string_utils.first_char_to_lower(self.__class_name), self.cpp_method())
        step_2 = 'return {0};'.format(self.jni_variable_from_cpp_variable(cpp_return))
        return method_name + '\n' + para_name + '{{\n  {0}\n  {1}\n}}'.format(step_1, step_2)

    def jni_var_assignment_by_cpp_variable(self):
        """Returns a method which is a JNI filed converted from C++.

        Returns:
            For example:

            jstring jFileId = lesschat::JniHelper::JstringFromString(file.file_id());
        """
        jtype = self.__var_type.to_jni_getter_string()
        jname = 'j{0}'.format(string_utils.to_title_style_name(self.__name))
        return '{0} {1} = {2};'.format(jtype, jname, self.__jni_variable_from_cpp_class())

    def jni_delete_local_ref(self):
        """Gets JNI delete local ref method.

        Returns:
            A string which is JNI delete local ref method.
        """
        if self.__var_type == VarType.cpp_string or self.__var_type == VarType.cpp_string_array:
            return 'env->DeleteLocalRef(j{0});'.format(string_utils.first_char_to_upper(self.__name))
        elif self.__var_type == VarType.cpp_object or self.__var_type == VarType.cpp_object_array:
            skr_logger.skr_log_warning('JniVariable.jni_delete_local_ref() : Not supported type')
            return 'env->DeleteLocalRef(j{0});'.format(string_utils.first_char_to_upper(self.__name))
        else:
            return ''

    def jni_variable_from_cpp_variable(self, return_variable):
        if self.__var_type == VarType.cpp_bool:
            return return_variable
        elif self.__var_type == VarType.cpp_enum:
            return 'static_cast<jint>({0})'.format(return_variable)
        elif self.__var_type == VarType.cpp_int:
            return 'static_cast<jint>({0})'.format(return_variable)
        elif self.__var_type == VarType.cpp_string:
            return 'env->NewStringUTF({0}.c_str())'.format(return_variable)
        elif self.__var_type == VarType.cpp_string_array:
            return 'lesschat::JniHelper::JobjectArrayFromStringVector({0})'.format(return_variable)
        elif self.__var_type == VarType.cpp_time:
            return 'static_cast<jlong>({0}) * 1000'.format(return_variable)
        elif self.__var_type == VarType.cpp_object:
            return 'reinterpret_cast<jlong>({0}.release())'.format(return_variable)
        elif self.__var_type == VarType.cpp_object_array:
            return 'lesschat::JniHelper::JlongArrayFromNativeArray(std::move({0}))'.format(return_variable)

    def to_getter_string(self):
        if self.__var_type.value == 1:
            return 'bool'
        elif self.__var_type.value == 2:
            return 'int'
        elif self.__var_type.value == 3:
            return 'std::string'
        elif self.__var_type.value == 4:
            return 'lesschat::' + self.__var_type.cpp_enum_type_string()
        elif self.__var_type.value == 5:
            return 'std::vector<std::string>'
        elif self.__var_type.value == 6:
            return 'time_t'
        elif self.__var_type.value == 7:
            return 'std::vector<std::unique_ptr<lesschat::{0}>>'.format(self.__var_type.object_class_name)
        elif self.__var_type.value == 8:
            return 'std::unique_ptr<lesschat::{0}>'.format(self.__var_type.object_class_name)
        else:
            print 'Unsupported value'

    def cpp_variable_from_jni_variable(self, return_variable):
        if self.__var_type == VarType.cpp_bool:
            return 'static_cast<bool>({0})'.format(return_variable)
        elif self.__var_type == VarType.cpp_enum:
            return 'static_cast<lesschat::{0}>({1})'.format(self.__var_type.to_getter_string(), return_variable)
        elif self.__var_type == VarType.cpp_int:
            return return_variable
        elif self.__var_type == VarType.cpp_string:
            return 'lesschat::JniHelper::StringFromJstring({0})'.format(return_variable)
        elif self.__var_type == VarType.cpp_string_array:
            return 'lesschat::JniHelper::StringVectorFromJobjectArray({0})'.format(return_variable)
        elif self.__var_type == VarType.cpp_time:
            return 'static_cast<time_t>({0} / 1000)'.format(return_variable)

    def cpp_method(self):
        if self.__var_type == VarType.cpp_bool:
            return 'is_{0}'.format(self.__name)
        else:
            return self.__name

    # from 'display_name' to 'DisplayName'
    def to_title_style_name(self):
        return string_utils.to_title_style_name(self.__name)

    # from 'display_name' to 'displayName'
    def to_param_style_name(self):
        return string_utils.to_objc_property_name(self.__name)

    def jni_variable_name(self):
        return self.__var_type.to_jni_getter_string()

    def jni_variable_sign_name(self):
        return self.__var_type.to_jni_sign_getter_string()

    def __getter_method_name(self):
        title_style_name = string_utils.to_title_style_name(self.__name)
        if self.__var_type == VarType.cpp_bool:
            method_name = 'JNIEXPORT {0} JNICALL Java_com_lesschat_core_{1}_{2}_nativeIs{3}'. \
                format(self.__var_type.to_jni_getter_string(), self.__group_name, self.__class_name, title_style_name)
            return method_name
        else:
            method_name = 'JNIEXPORT {0} JNICALL Java_com_lesschat_core_{1}_{2}_nativeGet{3}'. \
                format(self.__var_type.to_jni_getter_string(), self.__group_name, self.__class_name, title_style_name)
            return method_name

    def __jni_variable_from_cpp_class(self):
        instance_name = string_utils.cpp_class_name_to_cpp_file_name(self.__class_name)
        if self.__var_type == VarType.cpp_bool:
            return 'static_cast<jboolean>({0}.is_{1}())'.format(instance_name, self.__name)
        elif self.__var_type == VarType.cpp_enum:
            return 'static_cast<jint>({0}.{1}())'.format(instance_name, self.__name)
        elif self.__var_type == VarType.cpp_int:
            return 'static_cast<jint>({0}.{1}())'.format(instance_name, self.__name)
        elif self.__var_type == VarType.cpp_string:
            return 'env->NewStringUTF({0}.{1}().c_str())'.format(instance_name, self.__name)
        elif self.__var_type == VarType.cpp_string_array:
            return 'lesschat::JniHelper::JobjectArrayFromStringVector({0}.{1}())'.format(instance_name, self.__name)
        elif self.__var_type == VarType.cpp_time:
            return 'static_cast<jlong>({0}.{1}()) * 1000'.format(instance_name, self.__name)
        elif self.__var_type == VarType.cpp_object:
            skr_logger.skr_log_warning('JniVariable.__jni_variable_from_cpp_class() : C++ object is not supported')
            return ''
        elif self.__var_type == VarType.cpp_object_array:
            skr_logger.skr_log_warning(
                'JniVariable.__jni_variable_from_cpp_class() : C++ object array is not supported')
            return ''
        else:
            skr_logger.skr_log_warning('JniVariable.__jni_variable_from_cpp_class() : Not supported type')

    @property
    def var_type(self):
        return self.__var_type

    @property
    def name(self):
        return self.__name
