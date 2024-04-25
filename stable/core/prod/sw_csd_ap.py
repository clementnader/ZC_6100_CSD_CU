# -*-coding:utf-8 -*
import sys
import os

import json

from enum import Enum, unique

from core.prod.sw import Sw
from core.file.file import *
from core.file.elf import ElfFile
from core.file.disasm import Disasm
from core.file.src_ada import SrcAdaFile
from core.file.arch import ArchiveFile

class SwCsdApConst():
    
    SW_CONST_CSD_AP_SRC_ADA_LC = 'CSD_AP_SRC_ADA_LC'

class SwCsdAp(Sw):

    def __init__(self, d_sw_const, d_proc, str_sw_dirpath, d_sw_files):
        super().__init__(d_sw_const, d_proc, str_sw_dirpath, d_sw_files)
        self.i_nb_sw_inst = 3

    def _set_map(self, str_file_name):

        str_file_path = self.d_files[str_file_name]
        elf = ElfFile(str_file_path)
        d_map = elf.get_mapping()
        
        self.d_map[str_file_name] = d_map

    def _set_instr(self, str_file_name):
               
        str_file_path = self.d_files[str_file_name]
        elf = ElfFile(str_file_path)
        d_undec_instr = elf.get_instructions()
        d_instr = {}

        disassembler = Disasm(self.d_proc)

        for str_symb_name in d_undec_instr:
            if '_CHECKSUM' != str_symb_name and 'csd_ppc_signature' != str_symb_name:
                str_symb_addr = d_undec_instr[str_symb_name]['address']
                d_instr[str_symb_name] = {'address': str_symb_addr, 'instructions': {}}

                for str_instr_addr, str_instr_bytes in d_undec_instr[str_symb_name]['instructions'].items():
                    b_instr, d_dec_instr = disassembler.decode_instr(int(str_instr_bytes,16))
                    if b_instr:
                        d_instr[str_symb_name]['instructions'][str_instr_addr] =  d_dec_instr    

        self.d_instr[str_file_name] = d_instr


    def _set_comm(self, str_file_name):

        str_file_path = self.d_files[str_file_name]
        elf = ElfFile(str_file_path)
        l_comm = elf.get_comment()
        
        self.d_comm[str_file_name] = l_comm

    def _check_constr_prod(self, d_constr):

        d_constr_result = {}

        str_type = d_constr['type']

        if SwCsdApConst.SW_CONST_CSD_AP_SRC_ADA_LC == str_type:
            d_constr_result = self._check_src_ada_lc(d_constr)
        else:
            pass
            
        return d_constr_result

    def _check_src_ada_lc(self, d_constr_csd_ap_lc):

        d_result = {'result': {'types': {}, 'chains': {}}, 'lc': {} }

        l_chains = d_constr_csd_ap_lc['lc']['chains']
        i_nb_chains = len(d_constr_csd_ap_lc['lc']['chains'])
        l_sign_chains = [ [ [] for idx_chain in range(i_nb_chains)] for idx_inst in range(self.i_nb_sw_inst)]
        
        for str_lc, l_func_const_file in d_constr_csd_ap_lc['lc']['types'].items():

            d_result['lc'][str_lc] = [None] * self.i_nb_sw_inst
            d_result['result']['types'][str_lc] = False

            l_sign_type = []
            for idx_sw_inst, d_func_const_file in enumerate(l_func_const_file):

                if 'archive' in d_func_const_file:
                    str_archive_file_name = d_func_const_file['archive']
                    str_arch_file_path = self.d_files[str_archive_file_name]
                    if ArchiveFile.is_archive_file(str_arch_file_path):
                        str_file_path = d_func_const_file['file_path']
                        str_extract_dir_path = os.path.dirname(str_arch_file_path)
                        str_file_path = ArchiveFile.extract_file(str_arch_file_path, str_file_path, str_extract_dir_path)
                    else:
                        str_file_path = None
                else:
                    str_file_name = d_func_const_file['file']
                    str_file_path = self.d_files[str_file_name]


                l_sign = []
                if 'function' in d_func_const_file:
                    str_function_name = d_func_const_file['function']
                    str_return = SrcAdaFile.get_return(str_file_path, str_function_name)
                    l_C1C2 = SrcAdaFile.get_list_from_1Darray(str_return)
                    l_sign.append(l_C1C2)

                elif 'constant' in d_func_const_file:
                    str_constant_name = d_func_const_file['constant']
                    str_constant = SrcAdaFile.get_constant(str_file_path, str_constant_name)
                    l_sign = SrcAdaFile.get_list_from_2Darray(str_constant)

                d_result['lc'][str_lc][idx_sw_inst] = l_sign
                l_sign_type.extend(l_sign)

                for idx_chain in range(i_nb_chains):
                    if str_lc in l_chains[idx_chain]:
                        if l_sign_chains[idx_sw_inst][idx_chain] is None:
                            l_sign_chains[idx_sw_inst][idx_chain] = l_sign
                        else:
                            l_sign_chains[idx_sw_inst][idx_chain].extend(l_sign)
            
        
            b_unicity_type = self._check_src_ada_lc_sign(l_sign_type)
            d_result['result']['types'][str_lc] = b_unicity_type

        for idx_chain in range(i_nb_chains):
            str_chain = ' - '.join(l_chains[idx_chain])
            l_results = [False] * self.i_nb_sw_inst
            for idx_inst in range(self.i_nb_sw_inst):
                b_unicity_chain = self._check_src_ada_lc_sign(l_sign_chains[idx_inst][idx_chain])
                l_results[idx_inst] = b_unicity_chain
            d_result['result']['chains'][str_chain] = l_results                 

        return d_result


    def _check_src_ada_lc_sign(self, l_sign):

        b_result = False
        b_twice_C1C2 = False

        d_C1C2 = {}
        for l_C1C2 in l_sign:
            str_C1 = l_C1C2[0]
            str_C2 = l_C1C2[1]
            if str_C1 in d_C1C2:
                if str_C2 in d_C1C2[str_C1]:
                    b_twice_C1C2 = True
                    break
                else:
                    d_C1C2[str_C1].append(str_C2)
            else:
                d_C1C2[str_C1] = [str_C2]

        if not b_twice_C1C2:
            b_result = True

        return b_result

