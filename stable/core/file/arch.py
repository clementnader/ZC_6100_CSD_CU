# -*-coding:utf-8 -*
import tarfile
import re
import enum
import os
import shutil

from .file import copy_file

class ArchiveFile:

    @staticmethod
    def is_archive_file(str_file_path):

        b_archive_file = False

        if tarfile.is_tarfile(str_file_path):
           b_archive_file = True
        else:
            pass

        return b_archive_file

    @staticmethod
    def extract_all(str_arch_file_path, str_extract_dir_path):
        os.chdir(str_extract_dir_path)
        try:
            if str_arch_file_path.lower().endswith('.tgz') or str_arch_file_path.lower().endswith('.tar.gz'):
                with tarfile.open(str_arch_file_path,'r:gz') as tar_file:
                    tar_file.extractall()
                    tar_file.close()           
        except:
            raise

    @staticmethod
    def extract_file(str_arch_file_path, str_file_path, str_extract_dir_path):
        os.chdir(str_extract_dir_path)
        try:
            if str_arch_file_path.lower().endswith('.tgz') or str_arch_file_path.lower().endswith('.tar.gz'):
                with tarfile.open(str_arch_file_path,'r:gz') as tar_file:
                    tar_file.extract(str_file_path)
                    tar_file.close()

                    str_file_name = os.path.basename(str_file_path)
                    copy_file(str_file_path, str_extract_dir_path)

                    match = re.search('(.*?)/', str_file_path)
                    if None != match:
                        str_dir_name = match.group(1)
                        str_dir_path = str_extract_dir_path + '/' + str_dir_name
                        shutil.rmtree(str_dir_path, True)

                    str_file_path = str_extract_dir_path + '/' + str_file_name 
  
        
        except:
            raise

        return str_file_path