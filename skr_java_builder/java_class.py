#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - Frank Lin

from java_variable import VarType
from skrutil.string_utils import indent

_JAVA_BR = '\n\n'
_JAVA_SPACE = '    '


class JavaClass:
    """Java file generator, including package, class, fields, enums and manager.
    """

    def __init__(self, group_name, class_name, java_variable_list, java_enum_list, java_manager_or_none):
        """Init Java file generator.

        Args:
            group_name: A string which is package name, input name is C++ folder name, should be all lowercase. (eg: task)
            class_name: A string which is class name, input name is C++ class name, should be capitalized. (eg: Task)
            java_variable_list: A list of <JavaVariable> object which mean all fields in class.
            java_enum_list: A list of <JavaEnum> object which mean all enums in class.
            java_manager_or_none: A <JavaManager> object means ObjectManager or none means the class has no ObjectManager.
        """
        self.__group_name = group_name
        self.__class_name = class_name
        self.__java_var_list = java_variable_list
        self.__java_enum_list = java_enum_list
        self.__java_manager_or_none = java_manager_or_none

        if self.__java_manager_or_none is not None:
            self.__java_manager_or_none.set_object_name(class_name, class_name + 's')
            self.__java_manager_or_none.set_java_variable_list(java_variable_list)

    def generate_java_v2(self, config):
        """Generates java object implementation.

        Args:
            config: A config that enables some user-defined name.
        """
        file_name = self.__class_name + '.java'
        file_path = 'build/{0}/'.format(config.java_package_path) + self.__group_name + '/' + file_name
        output_java = open(file_path, 'w')

        java_package = 'package {0}.'.format(config.java_package_name) + self.__group_name + ';'

        output_java.write(java_package + _JAVA_BR)

        java_import = 'import android.support.annotation.IntDef;\n'
        java_import += 'import java.lang.annotation.Retention;\n'
        java_import += 'import java.lang.annotation.RetentionPolicy;' + _JAVA_BR

        java_import += 'import {0}.base.{1};\n'.format(config.java_package_name, config.java_base_object)
        java_import += 'import {0}.jni.CoreObject;\n'.format(config.java_package_name)
        java_import += 'import java.util.ArrayList;\n'
        java_import += 'import java.util.Arrays;\n'
        if self.__class_name != 'List':
            java_import += 'import java.util.List;'

        java_class_start = 'public final class ' + self.__class_name + ' extends {0} {{'.format(config.java_base_object)
        java_class_end = '}'

        output_java.write(java_import + _JAVA_BR)
        output_java.write(java_class_start + _JAVA_BR)

        # generates enum in class
        for java_enum in self.__java_enum_list:
            output_java.write(java_enum.generate_android_enum(_JAVA_SPACE) + '\n')

        # generates fields in class
        for java_var in self.__java_var_list:
            output_java.write(_JAVA_SPACE + java_var.private_field_name() + '\n')
        output_java.write('\n')

        # generates constructor
        output_java.write(self.__constructors_v2())
        output_java.write(_JAVA_BR)

        # generate getters
        for java_var in self.__java_var_list:
            output_java.write(java_var.getter_v2() + _JAVA_BR)

        # end brace
        output_java.write(java_class_end + '\n')

    def generate_java(self):
        """Gets Java with JNI implementation. The class inherits from |CoreObject| which means invoker should release
         the object himself/herself by calling |CoreObject.dispose()|.

         New development should use <generate_java_v2> instead.

        Returns:
            A string which is the class implementation.
        """
        file_name = self.__class_name + '.java'
        file_path = 'build/com/lesschat/core/' + self.__group_name + '/' + file_name
        output_java = open(file_path, 'w')

        java_package = 'package com.lesschat.core.' + self.__group_name + ';'

        output_java.write(java_package + _JAVA_BR)

        java_import = 'import android.os.Parcel;\n'
        java_import += 'import android.os.Parcelable;' + _JAVA_BR
        java_import += 'import com.lesschat.core.jni.CoreObject;' + _JAVA_BR
        java_import += 'import java.util.ArrayList;\n'
        java_import += 'import java.util.Arrays;\n'
        if self.__class_name != 'List':
            java_import += 'import java.util.List;'

        java_class_start = 'public class ' + self.__class_name + ' extends CoreObject implements Parcelable {'
        java_class_end = '}'

        output_java.write(java_import + _JAVA_BR)
        output_java.write(java_class_start + _JAVA_BR)

        output_java.write(self.__constructors())
        output_java.write(indent(4) + '@Override\n')
        output_java.write(indent(4) + 'public void dispose() {\n')
        output_java.write(indent(2) + 'nativeRelease{0}(mNativeHandler);\n'.format(self.__class_name))
        output_java.write(indent(4) + '}' + _JAVA_BR)

        for java_enum in self.__java_enum_list:
            output_java.write(java_enum.generate_java_enum(_JAVA_SPACE) + '\n')

        for java_var in self.__java_var_list:
            output_java.write(java_var.getter() + _JAVA_BR)

        output_java.write(_JAVA_BR)
        output_java.write(self.__native_constructors())
        output_java.write(indent(4) + 'private native void nativeRelease{0}(long handler);'.format(self.__class_name) + _JAVA_BR)

        for java_var in self.__java_var_list:
            output_java.write(java_var.native_getter() + _JAVA_BR)

        output_java.write(self.__parcelable())
        output_java.write(java_class_end)

    def generate_manager_v2(self, version, config):
        """Generates Java manager implementation code.

        Args:
            version: A float for compact usage.
            config: A <Config> object describes some user-defined names.

        Returns:
            A string which is Java manager implementation code.
        """
        if self.__java_manager_or_none is None:
            return
        manager_name = self.__java_manager_or_none.manager_name
        file_name = self.__java_manager_or_none.manager_name + '.java'
        file_path = 'build/{0}/'.format(config.java_package_path) + self.__group_name + '/' + file_name
        output_java = open(file_path, 'w')

        java_package = 'package {0}.'.format(config.java_package_name) + self.__group_name + ';'

        output_java.write(java_package + _JAVA_BR)

        java_import = ''
        if len(self.__java_manager_or_none.apis) != 0:
            java_import += 'import {0}.api.*;\n'.format(config.java_package_name)

        java_import += 'import android.support.annotation.NonNull;' + '\n'
        java_import += 'import android.support.annotation.Nullable;' + '\n'
        java_import += 'import {0}.api.v3.OnFailureListener;'.format(config.java_package_name) + '\n'
        java_import += 'import {0}.api.v3.OnResponseListener;'.format(config.java_package_name) + '\n'
        java_import += 'import {2}.{0}.{1}.*;\n'.format(self.__group_name, self.__class_name, config.java_package_name)
        java_import += 'import {0}.jni.CoreObject;\n'.format(config.java_package_name)
        java_import += 'import {0}.director.Director;\n'.format(config.java_package_name)
        java_import += 'import {0}.jni.JniHelper;\n\n'.format(config.java_package_name)
        java_import += 'import java.util.ArrayList;\n'
        java_import += 'import java.util.List;' + _JAVA_BR

        java_class_start = 'public class ' + manager_name + ' extends CoreObject {' + _JAVA_BR
        java_class_end = '}'

        java_manager_constructor = 'public static {0} getInstance() {{ return Director.getInstance().get{0}(); }}'
        java_override = '@Override\n'
        java_manager_dispose = 'public void dispose() { }' + _JAVA_BR

        output_java.write(java_import)
        output_java.write(java_class_start)

        if version < 6:
            output_java.write(self.__java_manager_or_none.generate_http_variables())
            output_java.write('\n')

        output_java.write(indent(4) + java_manager_constructor.format(manager_name) + _JAVA_BR)
        output_java.write(indent(4) + java_override)
        output_java.write(indent(4) + java_manager_dispose)

        output_java.write(self.__java_manager_or_none.generate_fetch_v2())
        output_java.write(self.__java_manager_or_none.generate_http_function(version))
        output_java.write(self.__java_manager_or_none.generate_fetch_native_v2())
        output_java.write(self.__java_manager_or_none.generate_http_function_native())

        output_java.write(java_class_end)

    def __constructors(self):
        """Java class constructor with native handler as parameter.

        Returns:
            A string which is the implementation of the constructor. For example:

            public Task(long nativeHandler) {
                mNativeHandler = nativeHandler;
            }
        """
        constructor = indent(4) + 'public {0}() {{ \n        mNativeHandler = nativeCreate{0}(); \n    }}'\
            .format(self.__class_name) + _JAVA_BR
        constructor += indent(4) + 'public {0}(long nativeHandler) {{\n'.format(self.__class_name)
        constructor += indent(2) + 'mNativeHandler = nativeHandler;\n'
        constructor += indent(4) + '}\n\n'
        return constructor

    def __constructors_v2(self):
        """Java class constructor with all fields as parameters.

        Returns:
            A string which is the implementation of the constructor. For example:

            /*package*/ File(String fileId,
                             @File.Type int type,
                             @File.Visibility int visibility,
                             @File.Belong int belong,
                             @File.FolderPermissionSetting int folderPermissionSetting,
                             String createdBy,
                             long createdAt,
                             String updatedBy,
                             long updatedAt) {
                             mFileId = fileId;
                             ... Remainder omitted...
                        }
        """
        package_class = indent(4) + '/*package*/ {0}'.format(self.__class_name)
        num_line_indent = len(package_class) + 1

        if len(self.__java_var_list) > 1:
            first_var = self.__java_var_list[0].input_parameter_name()
            constructor = '{0}({1},\n'.format(package_class, first_var)
            for var in self.__java_var_list:
                if first_var == var.input_parameter_name():
                    continue
                constructor += indent(num_line_indent) + '{0},'.format(var.input_parameter_name()) + '\n'
            constructor = constructor[:-2]  # remove break line and last comma
        elif len(self.__java_var_list) == 1:
            first_var = self.__java_var_list[0].input_parameter_name()
            constructor = '{0}({1})'.format(package_class, first_var)
        else:
            constructor = '{0}()'.format(package_class)

        constructor += ') {\n'

        for var in self.__java_var_list:
            constructor += indent(8) + var.assignment() + '\n'
        constructor += indent(4) + '}'

        return constructor

    def __constructor_with_variable(self):
        constructor = indent(4) + 'public {0}('.format(self.__class_name)
        space = len(indent(4) + 'public {0}('.format(self.__class_name))
        space_str = ''
        for space_index in range(0, space):
            space_str += ' '
        for index in range(0, len(self.__java_var_list)):
            java_var = self.__java_var_list[index]
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
        constructor += indent(2) + 'mNativeHandler = nativeCreate{0}('.format(self.__class_name)
        for java_var in self.__java_var_list:
            if java_var.var_type == VarType.cpp_enum:
                constructor += java_var.name_str + '.getValue(), '
            else:
                constructor += java_var.name_str + ', '
        constructor = constructor[:-2]
        constructor += ');\n'
        constructor += indent(4) + '}' + _JAVA_BR
        return constructor

    def __native_constructors(self):
        native_constructor = indent(4) + 'private native long nativeCreate{0}();'.format(self.__class_name) + _JAVA_BR
        # native_constructor += self.__native_constructor_with_variable()
        return native_constructor

    def __native_constructor_with_variable(self):
        space_str = ''
        native_constructor = indent(4) + 'private native long nativeCreate{0}('.format(self.__class_name)
        for space_index in range(0, len(indent(4) + 'private native long nativeCreate{0}('.format(self.__class_name))):
            space_str += ' '
        for index in range(0, len(self.__java_var_list)):
            java_var = self.__java_var_list[index]
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
        initwith = indent(4) + 'public boolean initWithJson(String json) { return nativeInitWithJson(mNativeHandler, json); }'
        initwith += _JAVA_BR
        return initwith

    def __native_initwith(self):
        native_initwith = indent(4) + 'private native boolean nativeInitWithJson(long handler, String json);'
        native_initwith += _JAVA_BR
        return native_initwith

    def __parcelable(self):
        parcelable = indent(4) + 'public {0}(Parcel in) {{\n'.format(self.__class_name)
        parcelable += indent(2) + 'mNativeHandler = in.readLong();\n'
        parcelable += indent(4) + '}' + _JAVA_BR
        parcelable += indent(4) + 'public static final Parcelable.Creator<{0}> CREATOR = new Parcelable.Creator<{0}>() {{\n\n'\
            .format(self.__class_name)
        parcelable += indent(2) + 'public {0} createFromParcel(Parcel in) {{ return new {0}(in); }}\n\n'\
            .format(self.__class_name)
        parcelable += indent(2) + 'public {0}[] newArray(int size) {{ return new {0}[size]; }}\n'\
            .format(self.__class_name)
        parcelable += indent(4) + '};' + _JAVA_BR
        parcelable += indent(4) + '@Override\n'
        parcelable += indent(4) + 'public int describeContents() { return 0; }' + _JAVA_BR
        parcelable += indent(4) + '@Override\n'
        parcelable += indent(4) + 'public void writeToParcel(Parcel parcel, int i) { parcel.writeLong(mNativeHandler); }\n'
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

        output_java.write(indent(1) + java_manager_constructor.format(manager_name) + _JAVA_BR)
        output_java.write(indent(1) + java_override)
        output_java.write(indent(1) + java_manager_dispose)

        output_java.write(self.java_manager_or_none.generate_fetch())
        output_java.write(self.java_manager_or_none.generate_http_function())
        output_java.write(self.java_manager_or_none.generate_fetch_native())
        output_java.write(self.java_manager_or_none.generate_http_function_native())

        output_java.write(java_class_end)

