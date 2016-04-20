#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - Frank Lin

from skrutil.string_utils import indent
from skrutil.skr_logger import skr_log_warning

_JAVA_BR = '\n\n'
_JAVA_SPACE = '    '


class JavaEnum:
    """Describes the Java enumeration.

    Since 5.0, we follow Android Performance tips, use int with @IntDef instead of enum class.

    To use:
    >>> java_enum = JavaEnum("Type")
    >>> java_enum.append(3, "NONE")
    >>> java_enum.append(4, "ALL")
    >>> java_enum.generate_android_enum(2)
    """

    def __init__(self, enum_class_name):
        """Init Java enum by class name.

        Args:
            enum_class_name: A string describes enum name.
        """
        self.__enum_class_name = enum_class_name
        self.__int_alias_tuple_list = []

    def append(self, int_value, alias):
        """Add enum by int value and its alias.

        Args:
            int_value: A string describes enum integer.
            alias: A string describes the name of enum.
        """
        self.__int_alias_tuple_list.append((int_value, alias))

    def generate_android_enum(self, pre_spaces):
        """Generates Android Style enums, uses int with @IntDef decoration.

        Args:
            pre_spaces: A string with only white spaces describes the spaces in front of each line of code.

        Returns:
            A string which is Java enum class implementation. For example:

            Retention(RetentionPolicy.SOURCE)
            @IntDef({VISIBILITY_PUBLIC, VISIBILITY_PRIVATE})
            public @interface Visibility {}
            public static final int VISIBILITY_PUBLIC = 1;
            public static final int VISIBILITY_PRIVATE = 2;
        """
        name_list = []
        int_def_list = []

        name_prefix = '{0}_'.format(self.__enum_class_name.upper())
        for int_alias_tuple in self.__int_alias_tuple_list:
            name = '{0}{1}'.format(name_prefix, int_alias_tuple[1])
            name_list.append(name)
            int_def_list.append('public static final int {0} = {1};'.format(name, int_alias_tuple[0]))

        java_enum = '{0}@Retention(RetentionPolicy.SOURCE)\n'.format(pre_spaces)
        java_enum += '{0}@IntDef({{'.format(pre_spaces)

        if len(name_list) > 0:
            for name in name_list:
                java_enum += '{0}, '.format(name)
            java_enum = java_enum[:-2]  # remove comma and space
        else:
            skr_log_warning('Java enum should at least has one definition')

        java_enum += '})\n'
        java_enum += '{0}public @interface {1} {{}}\n'.format(pre_spaces, self.__enum_class_name)

        for int_def in int_def_list:
            java_enum += '{0}{1}\n'.format(pre_spaces, int_def)
        return java_enum

    def generate_java_enum(self, pre_spaces):
        """Generates Java Style enums, uses Java enum class.

        In new development, use <generate_java_enum_v2> instead.

        Args:
            pre_spaces: A string with only white spaces describes the spaces in front of each line of code.

        Returns:
            A string which is Java enum class implementation. For example:

            public enum ApplicationType {
                DRIVE  (1),
                TASK   (2),
                EVENT  (3),
                REPORT (4);

                ApplicationType(int i) {
                    value = i;
                }

                int value;

                public int getValue() {
                    return value;
                }

                public static ApplicationType getApplicationTypeByValue(int value) {
                    ApplicationType[] types = ApplicationType.values();
                    for (ApplicationType type : types) {
                        if (type.getValue() == value) {
                            return type;
                        }
                    }
                    return ApplicationType.TASK;
                }
            }
        """
        java_enum = ''
        java_enum += '{0}public enum {1} {{\n'.format(pre_spaces, self.__enum_class_name)
        enum_count = 0
        for int_alias_tuple in self.__int_alias_tuple_list:
            java_enum += _JAVA_SPACE + '{0}{1}   ({2})'.format(pre_spaces,
                                                               int_alias_tuple[1],
                                                               int_alias_tuple[0])

            if enum_count < len(self.__int_alias_tuple_list) - 1:
                enum_count += 1
                java_enum += ",\n"
            else:
                java_enum += ";" + _JAVA_BR

        enum_class_instance = self.__enum_class_name.lower()

        java_enum += indent(2) + self.__enum_class_name + '(int i) {value = i;}' + _JAVA_BR
        java_enum += indent(2) + 'int value;' + _JAVA_BR
        java_enum += indent(2) + 'public int getValue() { return value; }' + _JAVA_BR
        java_enum \
            += indent(2) + 'public static {0} get{0}ByValue(int value) {{'.format(self.__enum_class_name) + "\n"
        java_enum \
            += indent(3) + '{0}[] {1}s = {2}.values();\n'\
            .format(self.__enum_class_name, enum_class_instance, self.__enum_class_name)
        java_enum \
            += indent(4) + 'for ({0} {1}: {2}s) {{\n'\
            .format(self.__enum_class_name, enum_class_instance, enum_class_instance)
        java_enum \
            += indent(4) + 'if ({0}.getValue() == value) {{\n'.format(enum_class_instance)
        java_enum += indent(5) + 'return {0};\n'.format(enum_class_instance)
        java_enum += indent(4) + '}\n'
        java_enum += indent(3) + '}\n'
        java_enum += indent(3) + 'return {0}.{1};\n'\
            .format(self.__enum_class_name, self.__int_alias_tuple_list[0][1])
        java_enum += indent(2) + '}\n'
        java_enum += indent(1) + '}\n'
        return java_enum
