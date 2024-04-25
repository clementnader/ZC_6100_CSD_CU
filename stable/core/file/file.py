# -*-coding:utf-8 -*
import os
import stat
import shutil


# Procedure for file copy
def copy_file(str_filepath, str_dest_dirpath):

    # Exract filename from full path
    str_filepath_head, str_filepath_tail = os.path.split(str_filepath)
    # Copy file
    shutil.copyfile(str_filepath, str_dest_dirpath + '/' + str_filepath_tail)


# Procedure for directory creation/file deletion if existing directory
def create_dir(str_dirpath):

    if os.path.isdir(str_dirpath):
        os.chdir(str_dirpath)
        l_filenames = os.listdir(str_dirpath)
        for str_filename in l_filenames:
            if os.path.isfile(str_filename):
                os.chmod(str_filename, stat.S_IWRITE)
                os.remove(str_filename)
    else:
        os.mkdir(str_dirpath, 777)
