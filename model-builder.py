#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - Frank Lin

"""This module provides C++, Java, Objective-C++ code generators.
"""

import os
import sys

from skr_cpp_builder.model_xml_parser import CppModelXmlParser
from skr_java_builder.java_model_xml_parser import JavaModelXmlParser
from skr_jni_builder.jni_model_xml_parser import JniModelXmlParser
from skr_objc_builder.objc_model_xml_parser import ObjcModelXmlParser
from skrutil import io_utils


if __name__ == "__main__":
    # Fixes Chinese chars encoding issue
    reload(sys)
    sys.setdefaultencoding('utf-8')

    input_file_path = sys.argv[1]
    dir_path, file_name = os.path.split(input_file_path)

    io_utils.make_directory_if_not_exists("build")

    if dir_path is None or dir_path == '':
        dir_path = '当前路径'

    print('输入的文件路径为:{0}, 文件名为:{1}'.format(dir_path, file_name))
    print('开始解析据...')

    parser = CppModelXmlParser(5.0)
    parser.parse(input_file_path)

    objc_parser = ObjcModelXmlParser(4.0)
    objc_parser.parse(input_file_path)

    java_parser = JavaModelXmlParser(5.0)
    java_parser.parse(input_file_path)

    jni_parse = JniModelXmlParser(5.0)
    jni_parse.parse(input_file_path)

    print('写入完成, 请查看 {0} 下的 build 文件夹'.format(dir_path))
    print('!!! 记得更新 options.h 中的 DATABASE_VERSION')
