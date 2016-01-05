# -*- coding: utf-8 -*-
#!/usr/bin/env python
# Copyright (c) 2016 Frank Lin. All rights reserved.

"""
Used to execute command to parse lesschat core model xml
"""

import sys
import os

from model_xml_parser import CppModelXmlParser
from objc_model_xml_parser import ObjcModelXmlParser


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

if __name__ == "__main__":

    input_file_path = sys.argv[1]
    dir_path, file_name = os.path.split(input_file_path)
    if dir_path is None or dir_path == '':
        dir_path = '当前路径'
    print('输入的文件路径为:%s, 文件名为:%s' %
          (dir_path,
          file_name))

    print('开始解析据...')

    parser = CppModelXmlParser(1.0)
    parser.parse(file_name)

    objc_parser = ObjcModelXmlParser(1.0)
    objc_parser.parse(file_name)

    print('写入完成, 请查看 %s 下的 core 文件夹' % (dir_path))
