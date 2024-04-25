# -*-coding:utf-8 -*
import sys
import re


class SrcAdaFile:

    @classmethod
    def get_list_from_1Darray(cls, str_1Darray):

        re_1Darray_value = '=>\s+(\d+)'
        l_1Darray_values = re.findall(re_1Darray_value, str_1Darray)

        return l_1Darray_values

    @classmethod
    def get_list_from_2Darray(cls, str_2Darray):

        l_2Darray_values = []

        re_1Darray = '\d+\s+=>\s+(\(.*?\))'
        l_1Darray = re.findall(re_1Darray_constant, str_2Darray)

        for str_1Darray in l_1Darray:
            l_1Darray_values = cls.get_list_from_1Darray(str_1Darray)
            l_2Darray_values.append(l_1Darray_values)

        return l_2Darray_values

    @staticmethod
    def get_constant(str_file_path, str_constant_name):

        re_const_decl = '^\s*' + str_constant_name + '\s+:\s+constant.*:='
        re_const_val = '^\s*(?P<value>.*)\s*'
        re_const_decl_val = re_const_decl + re_const_val + ';'

        b_const = False
        str_value = ''

        with open(str_file_path, 'r', encoding="latin-1") as workFile:

            for str_line in workFile:
                if b_const:
                    if ';' in str_line:
                        match = re.search(re_const_val + ';', str_line)
                        if match is not None:
                            str_value += match.group('value')
                        break
                    else:
                        match = re.search(re_const_val, str_line)
                        if match is not None:
                            str_value += match.group('value')
                else:
                    match = re.search(re_const_decl, str_line)
                    if match is not None:
                        b_const = True
                        if ';' in str_line:
                            match = re.search(re_const_decl_val, str_line)
                            if match is not None:
                                str_value = match.group('value')
                            break

        str_value = str_value.replace('_', '')
        return str_value

    @staticmethod
    def get_return(str_file_path, str_function_name):

        re_func_decl = '^\s*function\s+' + str_function_name + '.*is'
        re_func_return = '^\s*return\s+(?P<value>.*)\s*;'

        b_func = False
        str_value = ''

        with open(str_file_path, 'r', encoding="utf-8") as workFile:

            for str_line in workFile:
                if b_func:
                    match = re.search(re_func_return, str_line)
                    if match is not None:
                        str_value = match.group('value')
                        break
                else:
                    match = re.search(re_func_decl, str_line)
                    if match is not None:
                        b_func = True

        str_value = str_value.replace('_', '')
        return str_value


if '__main__' == __name__:
    str_dir_path = 'C:/_Ansaldo/Produits/PAI_NG_SEI2006/Sw_LCAS/d_Code/'
    str_file_path = str_dir_path + 'and_lcap3_sei6.0_e35_i845/Code/sei_lcap3_cfg_svl_csd_mtor2.adb'
    str_constant_name = 'Svl_Csd_Snv1_Skc_Inin_1'
    str_constant = SrcAdaFile.get_constant(str_file_path, str_constant_name)
    l_values = SrcAdaFile.get_list_from_2Darray(str_constant)
    print(l_values)

    str_file_path = str_dir_path + 'and_lcap3_sei6.0_e35_i845/Code/csd_lcap3_signature_vle_at.ad6'
    str_function_name = 'SVL_CSD_SNVx_CSD_AT_1'
    str_return = SrcAdaFile.get_return(str_file_path, str_function_name)
    l_values = SrcAdaFile.get_list_from_1Darray(str_return)
    print(l_values)
