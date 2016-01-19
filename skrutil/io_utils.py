import shutil
import os

import string_utils


# make directory if not exists and delete and make if exists
def make_directory_if_not_exists(path):
    if os.path.exists(path):
        shutil.rmtree(path)
        os.makedirs(path)
    else:
        os.makedirs(path)


# returns "build/core/task/task.h"
def cpp_object_header_path(group_name, class_name):
    cpp_file_name = string_utils.cpp_class_name_to_cpp_file_name(class_name)
    return "build/{0}/{1}.h".format(group_name, cpp_file_name)


# returns "build/core/task/task.cc"
def cpp_object_implementation_path(group_name, class_name):
    cpp_file_name = string_utils.cpp_class_name_to_cpp_file_name(class_name)
    return "build/{0}/{1}.cc".format(group_name, cpp_file_name)
