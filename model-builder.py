# -*- coding: utf-8 -*-
#!/usr/bin/env python
# model-builder.py
# simple C++ generator, originally targetted for starting build sakura core.
#
# Copyright (c) 2016 - Frank Lin

"""
Used to execute command to parse lesschat core model xml
"""

import os
import sys

from skrutil import io_utils

from skr_cpp_builder.model_xml_parser import CppModelXmlParser
from skr_java_builder.java_model_xml_parser import JavaModelXmlParser
from skr_jni_builder.jni_model_xml_parser import JniModelXmlParse
from skr_objc_builder.objc_model_xml_parser import ObjcModelXmlParser


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

if __name__ == "__main__":
    # 解决中文编码解析问题
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')

    input_file_path = sys.argv[1]
    dir_path, file_name = os.path.split(input_file_path)

    io_utils.make_directory_if_not_exists("build")

    if dir_path is None or dir_path == '':
        dir_path = '当前路径'
    print('输入的文件路径为:%s, 文件名为:%s' %
          (dir_path,
          file_name))

    print('开始解析据...')

    parser = CppModelXmlParser(4.0)
    parser.parse(input_file_path)

    # objc_parser = ObjcModelXmlParser(4.0)
    # objc_parser.parse(input_file_path)

    # java_parser = JavaModelXmlParser(4.0)
    # java_parser.parse(input_file_path)

    jni_parse = JniModelXmlParse(4.0)
    jni_parse.parse(input_file_path)

    print('写入完成, 请查看 %s 下的 build 文件夹' % (dir_path))
    print('!!! 记得更新 options.h 中的 DATABASE_VERSION')
