from java_variable import VarType

_JAVA_BR = '\n\n'
_JAVA_SPACE = '    '


def function_space(count):
    space = ''
    for i in range(1, count + 1):
        space += _JAVA_SPACE
    return space


class JavaClass:
    def __init__(self, group_name, class_name, java_variable_list, java_enum_list, java_manager_or_none):
        self.group_name = group_name
        self.class_name = class_name
        self.java_var_list = java_variable_list
        self.java_enum_list = java_enum_list
        self.java_manager_or_none = java_manager_or_none

        if self.java_manager_or_none is not None:
            self.java_manager_or_none.set_object_name(class_name, class_name + 's')
            self.java_manager_or_none.set_java_variable_list(java_variable_list)

    # @staticmethod
    # def __convert_class_name_to_file_name(name):
    #     s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    #     return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    def generate_java(self):
        file_name = self.class_name + '.java'
        file_path = 'build/com/lesschat/core/' + self.group_name + '/' + file_name
        output_java = open(file_path, 'w')

        java_package = 'package com.lesschat.core.' + self.group_name + ';'

        output_java.write(java_package + _JAVA_BR)

        java_import = 'import android.os.Parcel;\n'
        java_import += 'import android.os.Parcelable;' + _JAVA_BR
        java_import += 'import com.lesschat.core.jni.CoreObject;' + _JAVA_BR
        java_import += 'import java.util.ArrayList;\n'
        java_import += 'import java.util.Arrays;\n'
        if self.class_name != 'List':
            java_import += 'import java.util.List;'

        java_class_start = 'public class ' + self.class_name + ' extends CoreObject implements Parcelable {'
        java_class_end = '}'

        output_java.write(java_import + _JAVA_BR)
        output_java.write(java_class_start + _JAVA_BR)

        output_java.write(self.__constructors())
        # output_java.write(self.__initwith())
        output_java.write(function_space(1) + '@Override\n')
        output_java.write(function_space(1) + 'public void dispose() {\n')
        output_java.write(function_space(2) + 'nativeRelease{0}(mNativeHandler);\n'.format(self.class_name))
        output_java.write(function_space(1) + '}' + _JAVA_BR)

        for java_enum in self.java_enum_list:
            output_java.write(java_enum.generate_java_enum(_JAVA_SPACE) + '\n')

        for java_var in self.java_var_list:
            output_java.write(java_var.getter() + _JAVA_BR)
            # output_java.write(java_var.setter() + _JAVA_BR)

        output_java.write(_JAVA_BR)
        output_java.write(self.__native_constructors())
        # output_java.write(self.__native_initwith())
        output_java.write(function_space(1) + 'private native void nativeRelease{0}(long handler);'.format(self.class_name) + _JAVA_BR)

        for java_var in self.java_var_list:
            output_java.write(java_var.native_getter() + _JAVA_BR)
            # output_java.write(java_var.native_setter() + _JAVA_BR)

        output_java.write(self.__parcelable())

        output_java.write(java_class_end)

    def __constructors(self):
        constructor = function_space(1) + 'public {0}() {{ \n        mNativeHandler = nativeCreate{0}(); \n    }}'\
            .format(self.class_name) + _JAVA_BR
        constructor += function_space(1) + 'public {0}(long nativeHandler) {{\n'.format(self.class_name)
        constructor += function_space(2) + 'mNativeHandler = nativeHandler;\n'
        constructor += function_space(1) + '}\n\n'
        # constructor += self.__constructor_with_variable()
        return constructor

    def __constructor_with_variable(self):
        constructor = function_space(1) + 'public {0}('.format(self.class_name)
        space = len(function_space(1) + 'public {0}('.format(self.class_name))
        space_str = ''
        for space_index in range(0, space):
            space_str += ' '
        for index in range(0, len(self.java_var_list)):
            java_var = self.java_var_list[index]
            java_var_type = java_var.var_type
            if index == 0:
                if java_var_type == VarType.cpp_enum:
                    constructor += '{0} {1},\n'.format(java_var.java_enum, java_var.name_str)
                elif java_var_type == VarType.cpp_string_array:
                    constructor += 'String[] {0},\n'.format(java_var.name_str)
                else:
                    constructor += '{0} {1},\n'.format(java_var.var_type.to_java_getter_setter_string(), java_var.name_str)
            else:
                if java_var_type == VarType.cpp_enum:
                    constructor += space_str + '{0} {1},\n'.format(java_var.java_enum, java_var.name_str)
                elif java_var_type == VarType.cpp_string_array:
                    constructor += space_str + 'String[] {0},\n'.format(java_var.name_str)
                else:
                    constructor += space_str + '{0} {1},\n'.format(java_var.var_type.to_java_getter_setter_string(), java_var.name_str)
        constructor = constructor[:-2]
        constructor += '){\n'
        constructor += function_space(2) + 'mNativeHandler = nativeCreate{0}('.format(self.class_name)
        for java_var in self.java_var_list:
            if java_var.var_type == VarType.cpp_enum:
                constructor += java_var.name_str + '.getValue(), '
            else:
                constructor += java_var.name_str + ', '
        constructor = constructor[:-2]
        constructor += ');\n'
        constructor += function_space(1) + '}' + _JAVA_BR
        return constructor

    def __native_constructors(self):
        native_constructor = function_space(1) + 'private native long nativeCreate{0}();'.format(self.class_name) + _JAVA_BR
        # native_constructor += self.__native_constructor_with_variable()
        return native_constructor

    def __native_constructor_with_variable(self):
        space_str = ''
        native_constructor = function_space(1) + 'private native long nativeCreate{0}('.format(self.class_name)
        for space_index in range(0, len(function_space(1) + 'private native long nativeCreate{0}('.format(self.class_name))):
            space_str += ' '
        for index in range(0, len(self.java_var_list)):
            java_var = self.java_var_list[index]
            java_var_type = java_var.var_type
            if index == 0:
                if java_var_type == VarType.cpp_enum:
                    native_constructor += 'int {0},\n'.format(java_var.name_str)
                elif java_var_type == VarType.cpp_string_array:
                    native_constructor += 'String[] {0},\n'.format(java_var.name_str)
                else:
                    native_constructor += '{0} {1},\n'.format(java_var.var_type.to_java_getter_setter_string(), java_var.name_str)
            else:
                if java_var_type == VarType.cpp_enum:
                    native_constructor += space_str + 'int {0},\n'.format(java_var.name_str)
                elif java_var_type == VarType.cpp_string_array:
                    native_constructor += space_str + 'String[] {0},\n'.format(java_var.name_str)
                else:
                    native_constructor += space_str + '{0} {1},\n'.format(java_var.var_type.to_java_getter_setter_string(), java_var.name_str)
        native_constructor = native_constructor[:-2]
        native_constructor += ');' + _JAVA_BR
        return native_constructor

    def __initwith(self):
        initwith = function_space(1) + 'public boolean initWithJson(String json) { return nativeInitWithJson(mNativeHandler, json); }'
        initwith += _JAVA_BR
        return initwith

    def __native_initwith(self):
        native_initwith = function_space(1) + 'private native boolean nativeInitWithJson(long handler, String json);'
        native_initwith += _JAVA_BR
        return native_initwith

    def __parcelable(self):
        parcelable = function_space(1) + 'public {0}(Parcel in) {{\n'.format(self.class_name)
        parcelable += function_space(2) + 'mNativeHandler = in.readLong();\n'
        parcelable += function_space(1) + '}' + _JAVA_BR
        parcelable += function_space(1) + 'public static final Parcelable.Creator<{0}> CREATOR = new Parcelable.Creator<{0}>() {{\n\n'\
            .format(self.class_name)
        parcelable += function_space(2) + 'public {0} createFromParcel(Parcel in) {{ return new {0}(in); }}\n\n'\
            .format(self.class_name)
        parcelable += function_space(2) + 'public {0}[] newArray(int size) {{ return new {0}[size]; }}\n'\
            .format(self.class_name)
        parcelable += function_space(1) + '};' + _JAVA_BR
        parcelable += function_space(1) + '@Override\n'
        parcelable += function_space(1) + 'public int describeContents() { return 0; }' + _JAVA_BR
        parcelable += function_space(1) + '@Override\n'
        parcelable += function_space(1) + 'public void writeToParcel(Parcel parcel, int i) { parcel.writeLong(mNativeHandler); }\n'
        parcelable += '\n'
        return parcelable

    def generate_manager(self):
        if self.java_manager_or_none is None:
            return
        manager_name = self.java_manager_or_none.manager_name
        file_name = self.java_manager_or_none.manager_name + '.java'
        file_path = 'build/com/lesschat/core/' + self.group_name + '/' + file_name
        output_java = open(file_path, 'w')

        java_package = 'package com.lesschat.core.' + self.group_name + ';'

        output_java.write(java_package + _JAVA_BR)

        java_import = ''
        if len(self.java_manager_or_none.apis) != 0:
            java_import += 'import com.lesschat.core.api.*;\n'

        java_import += "import android.support.annotation.NonNull;"
        java_import += 'import com.lesschat.core.{0}.{1}.*;\n'.format(self.group_name, self.class_name)
        java_import += 'import com.lesschat.core.jni.CoreObject;\n'
        java_import += 'import com.lesschat.core.director.Director;\n'
        java_import += 'import com.lesschat.core.jni.JniHelper;\n\n'
        java_import += 'import java.util.ArrayList;\n'
        java_import += 'import java.util.List;' + _JAVA_BR

        java_class_start = 'public class ' + manager_name + ' extends CoreObject {' + _JAVA_BR
        java_class_end = '}'

        java_manager_constructor = 'public static @NonNull {0} getInstance() ' \
                                   '{{ return Director.getInstance().get{0}();}}'
        java_override = '@Override\n'
        java_manager_dispose = 'public void dispose() { }' + _JAVA_BR

        output_java.write(java_import)
        output_java.write(java_class_start)

        output_java.write(self.java_manager_or_none.generate_http_variable())
        output_java.write('\n')

        output_java.write(function_space(1) + java_manager_constructor.format(manager_name) + _JAVA_BR)
        output_java.write(function_space(1) + java_override)
        output_java.write(function_space(1) + java_manager_dispose)

        output_java.write(self.java_manager_or_none.generate_fetch())
        output_java.write(self.java_manager_or_none.generate_http_function())
        output_java.write(self.java_manager_or_none.generate_fetch_native())
        output_java.write(self.java_manager_or_none.generate_http_function_native())

        output_java.write(java_class_end)


