import shutil
import os


# make directory if not exists and delete and make if exists
def make_directory_if_not_exists(path):
    if os.path.exists(path):
        shutil.rmtree(path)
        os.makedirs(path)
    else:
        os.makedirs(path)