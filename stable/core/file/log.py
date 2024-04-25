# -*-coding:utf-8 -*
import sys
import re
from enum import Enum

class LogFile():

    class CompType(Enum):
        COMP_PPC_WRS_VXW_GCC = 'PPC_WRS_VXW_GCC'
        COMP_PPC_WR_TOR2_GCC_GNAT_WRAP = 'PPC_WR_TOR2_GCC_GNAT_WRAP'

    @classmethod
    def _get_comp_cmd_string(cls, str_comp):

        if cls.CompType.COMP_PPC_WRS_VXW_GCC.value == str_comp:
            str_comp_cmd = 'powerpc-wrs-vxworks-gcc' 
        elif cls.CompType.COMP_PPC_WR_TOR2_GCC_GNAT_WRAP.value == str_comp:
            str_comp_cmd = 'cc_gnat_ppc.bat' 
        else:
            str_comp_cmd = ''

        return str_comp_cmd

    @classmethod
    def _get_lang_file_ext(cls, str_lang):

        if 'Ada' == str_lang:
            l_file_ext = [".ads", ".adb"]
        elif 'C' == str_lang:
            l_file_ext = [".c"]
        else:
            l_file_ext = []
        
        return l_file_ext

    @classmethod
    def get_comp_opt(cls, str_file_path, str_comp, str_lang):

        l_comp_opt = []

        str_comp_cmd = cls._get_comp_cmd_string(str_comp)
        l_file_ext = cls._get_lang_file_ext(str_lang)

        re_comp_opt = '-\S+'
        re_all_comp_opt = '(?P<comp_opt>.+)'
        re_input_file = '\S+(?P<file_ext>\.\S+)'

        re_comp_line = '^' + str_comp_cmd + '\s+' + re_all_comp_opt + '\s+' + re_input_file + '$'      


        with open(str_file_path, 'r', encoding = "latin-1") as workfile:

            for str_line in workfile:
                match = re.search(re_comp_line,str_line)
                if match != None:
                    str_file_ext = match.group('file_ext')
                    if str_file_ext in l_file_ext:
                        str_all_comp_opt = match.group('comp_opt')
                        l_comp_opt_line = re.findall(re_comp_opt,str_all_comp_opt)
                        for str_comp_opt in l_comp_opt_line:
                            if str_comp_opt not in l_comp_opt:
                                l_comp_opt.append(str_comp_opt)


        d_comp_opt = {}
        
        for str_comp_opt in l_comp_opt:

            if '-I-' != str_comp_opt and str_comp_opt.startswith('-I'):
                if '-I' not in d_comp_opt:
                    d_comp_opt['-I'] = []
                # d_comp_opt['-I'].append(str_comp_opt.replace('-I',''))
                d_comp_opt['-I'].append(str_comp_opt)
            elif str_comp_opt.startswith('-D'):
                if '-D' not in d_comp_opt:
                    d_comp_opt['-D'] = []
                # d_comp_opt['-D'].append(str_comp_opt.replace('-D',''))
                d_comp_opt['-D'].append(str_comp_opt)
            elif str_comp_opt.startswith('-gnat'):
                if str_comp_opt.startswith('-gnatec'):
                    if '-gnatec' not in d_comp_opt:
                         d_comp_opt['-gnatec'] = []
                    # d_comp_opt['-gnatec'].append(str_comp_opt.replace('-gnatec=',''))
                    d_comp_opt['-gnatec'].append(str_comp_opt)
            elif str_comp_opt not in d_comp_opt:
                d_comp_opt[str_comp_opt] = []

        return d_comp_opt


    @classmethod
    def get_comp_warn(cls, str_file_path):

        d_comp_warn = {}

        re_file_name = '/?(?P<file_name>[\w|_]+\.\w+)'
        re_line_col_number = ':(?P<line_number>\d+):(?P<col_number>\d*):?'
        re_text = '(?P<text>.*)'
        re_comp_warn = re_file_name + re_line_col_number + ' warning: ' + re_text

        with open(str_file_path, 'r', encoding = "latin-1") as workfile:   
            for str_line in workfile:
                match = re.search(re_comp_warn,str_line)
                if match != None:
                    str_file_name = match.group('file_name')
                    if str_file_name not in d_comp_warn:
                        d_comp_warn[str_file_name] = {}
                    
                    str_line_number = match.group('line_number')
                    str_col_number = match.group('col_number')
                    str_text = match.group('text')

                    if str_line_number not in d_comp_warn[str_file_name]:
                        d_comp_warn[str_file_name][str_line_number] = {}
                    if '' == str_col_number :
                        if '' not in d_comp_warn[str_file_name][str_line_number]:
                            d_comp_warn[str_file_name][str_line_number][''] = []
                        d_comp_warn[str_file_name][str_line_number][''].append(str_text)
                    elif str_col_number in d_comp_warn[str_file_name][str_line_number]:
                        d_comp_warn[str_file_name][str_line_number][str_col_number] += ' ' + str_text
                    else:
                        d_comp_warn[str_file_name][str_line_number][str_col_number] = str_text


        return d_comp_warn

                     

        

