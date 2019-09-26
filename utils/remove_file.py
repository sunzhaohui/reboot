# _*_ encoding:utf-8 _*_
__author__ = 'sunzhaohui'
__date__ = '2019-09-25 17:09'

import os

def remove_file(file_path):
    if os.path.isdir(file_path):
        os.removedirs(file_path)
    elif os.path.isfile(file_path):
        os.remove(file_path)
        file_dir = os.path.split(file_path)[0]
        if os.listdir(file_dir):
            pass
        else:
            os.removedirs(file_dir)