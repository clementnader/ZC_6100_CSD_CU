# -*-coding:utf-8 -*
import subprocess
import sys
import re
import os
import stat
import json

# from disassemble import DisasmTarget, Disassembler

class ElfFile(object):

    str_file_path = None

    str_objdump_path = 'C:/GNATPRO/6.1.2/bin/powerpc-wrs-vxworks-objdump.exe'
    # str_objdump_path = 'C:/GNATPRO/7.2.2/bin/powerpc-wrs-vxworks-objdump.exe'
    # str_objdump_path = 'C:/Tornado/host/x86-win32/bin/objdumpppc.exe'
    # str_objdump_path = 'C:/Users/itoua/Documents/Software/MobaXterm/_home/slash/bin/objdump.exe'

    def __init__(self, str_file_path):
        self.str_file_path = str_file_path

    def get_mapping(self):

        d_map = {}

        re_symb_addr_val = '(?P<symb_addr_val>[0-9a-z]{8})'
        re_flag_char1 = '(?P<flag_char1>[l|g|u|!|\s])'
        re_flag_char2 = '(?P<flag_char2>[w|\s])'
        re_flag_char3 = '(?P<flag_char3>[C|\s])'
        re_flag_char4 = '(?P<flag_char4>[W|\s])'    
        re_flag_char5 = '(?P<flag_char5>[I|i|\s])'
        re_flag_char6 = '(?P<flag_char6>[d|D|\s])'
        re_flag_char7 = '(?P<flag_char7>[f|F|O|\s])'

        re_sect_name = '(?P<sect_name>.*)'
        re_symb_size_align = '(?P<symb_size_align>[0-9a-z]{8})'

        re_symb_name = '(?P<symb_name>.*)'

        re_symb_tab_line = '^' + re_symb_addr_val + '\s'
        re_symb_tab_line += re_flag_char1 + re_flag_char2 + re_flag_char3 + re_flag_char4 
        re_symb_tab_line += re_flag_char5 + re_flag_char6 + re_flag_char7
        re_symb_tab_line += '\s' + re_sect_name + '[\s|\t]+' + re_symb_size_align + '\s' + re_symb_name + '$'

        str_elf_dir_path = os.path.dirname(self.str_file_path)
        os.chdir(str_elf_dir_path)
        
        str_txt_file_path = self.str_file_path.replace('.elf','_elf_map.txt')

        with open(str_txt_file_path, 'w', encoding='latin-1') as workfile:
            objdump_process = subprocess.Popen([self.str_objdump_path, '-t', self.str_file_path], stdout=workfile)
            objdump_process.wait()

        b_symb = False

        with open(str_txt_file_path, 'r', encoding='latin-1') as workfile:
            for str_line in workfile:

                if b_symb:
                    if str_line in ('\n', '\r\n'):
                        b_symb = False
                    else:
                        match = re.search(re_symb_tab_line, str_line)
                        if None != match:
                            str_sect_name = match.group('sect_name')
                            if str_sect_name not in d_map:
                                d_map[str_sect_name] = {}


                            str_symb_addr_val = match.group('symb_addr_val')

                            if str_symb_addr_val not in d_map[str_sect_name]:
                                d_map[str_sect_name][str_symb_addr_val]= []

                            d_symb = {}
                            d_symb['name'] = match.group('symb_name')

                            d_symb['size_align'] = match.group('symb_size_align')

                            d_flags = {}
                            d_flags['flag_char1'] = match.group('flag_char1')
                            d_flags['flag_char2'] = match.group('flag_char2')
                            d_flags['flag_char3'] = match.group('flag_char3')
                            d_flags['flag_char4'] = match.group('flag_char4')
                            d_flags['flag_char5'] = match.group('flag_char5')
                            d_flags['flag_char6'] = match.group('flag_char6')
                            d_flags['flag_char7'] = match.group('flag_char7')

                            d_symb['flags'] = d_flags

                            d_map[str_sect_name][str_symb_addr_val].append(d_symb)
    
                else:
                    if str_line.startswith('SYMBOL TABLE:'):
                        b_symb = True

        
        os.chmod(str_txt_file_path, stat.S_IWRITE)
        os.remove(str_txt_file_path)
        
        return d_map     


    def get_instructions(self):

        d_instr = {}

        re_symb_addr = '(?P<address>[0-9a-z]{8})'
        re_symb_name = '<(?P<symbol>\S*)>:'
        re_symb = '^' + re_symb_addr + '\s' + re_symb_name

        re_instr_addr = '(?P<address>[0-9a-z]*)'
        re_instr_bytes = '(?P<bytes>\S{2}\s\S{2}\s\S{2}\s\S{2})'
        re_instr_mnem = '(?P<mnemonic>\S*)'
        re_instr = '^\s*' + re_instr_addr + ':\s' + re_instr_bytes + '\s*' + re_instr_mnem

        b_symb = False
        str_curr_symb_name = ''

        str_elf_dir_path = os.path.dirname(self.str_file_path)
        os.chdir(str_elf_dir_path)

        str_txt_file_path = self.str_file_path.replace('.elf','_elf_instr.txt')

        with open(str_txt_file_path, 'w', encoding='latin-1') as workfile:
            objdump_process = subprocess.Popen([self.str_objdump_path, '-d', self.str_file_path], stdout=workfile)
            objdump_process.wait()

        with open(str_txt_file_path, 'r', encoding='latin-1') as workfile:
            for str_line in workfile:
                if b_symb:
                    if str_line in ('\n', '\r\n'):
                        b_symb = False
                    else:
                        match = re.search(re_instr, str_line)
                        if None != match:
                            str_instr_addr = match.group('address')
                            str_instr_bytes = match.group('bytes')
                            str_instr_bytes = str_instr_bytes.replace(' ', '')
                            d_instr[str_curr_symb_name]['instructions'][str_instr_addr] = str_instr_bytes  
                
                else:
                    match = re.search(re_symb, str_line)
                    if None != match:
                        str_symb_name = match.group('symbol')
                        str_symb_addr = match.group('address')

                        d_instr[str_symb_name] = {'address': str_symb_addr, 'instructions': {} } 

                        str_curr_symb_name = str_symb_name
                        b_symb = True

        os.chmod(str_txt_file_path, stat.S_IWRITE)
        os.remove(str_txt_file_path)

        return d_instr

    def get_comment(self):

        l_comm = []
        re_comm_line = '^\s[0-9a-f]{1,8}[0-9a-f|\s]{38}(.*)$'

        str_elf_dir_path = os.path.dirname(self.str_file_path)
        os.chdir(str_elf_dir_path)
        
        str_txt_file_path = self.str_file_path.replace('.elf','_elf_comm.txt')

        with open(str_txt_file_path, 'w', encoding='latin-1') as workfile:
            objdump_process = subprocess.Popen([self.str_objdump_path, '-sj', '.comment', self.str_file_path], stdout=workfile)
            objdump_process.wait()

        str_comm = ''

        with open(str_txt_file_path, 'r', encoding='latin-1') as workfile:
            for str_line in workfile:
                match = re.search(re_comm_line, str_line)
                if None != match:
                    str_comm_line = match.group(1)
                    str_comm += str_comm_line

        l_comm = str_comm.split('..')
        l_comm[0] = l_comm[0][1:]

        re_dot_spaces = '(.*)\.\s*'
        match = re.search(re_dot_spaces, l_comm[-1])
        if match is not None:
            l_comm[-1] = match.group(1)

        os.chmod(str_txt_file_path, stat.S_IWRITE)
        os.remove(str_txt_file_path)
                
        return l_comm



if '__main__' == __name__:

    str_script_filepath = os.path.abspath(__file__)
    str_script_dirpath = os.path.dirname(str_script_filepath)

    # disassembler = Disassembler(DisasmTarget.TARGET_PPC_MPC7457)

    # str_elf_dir_path = 'C:/_Ansaldo/Produits/CSD_PPC/Sw_LCAP/d_Code/CSD_LCAP_MVME6100_4.6.1_7/csd_lcap_mvme6100_master/csd_lcap_mvme6100_dev/00csd_lcap1_mvme6100'
    str_elf_dir_path = 'C:/_Ansaldo/Outils/rtpc/rtpc_data/scm/CBTC_ZC_KCR_LCAP_BSITE_3.4.1_38/3'
    str_elf_file = 'x00981_pas_lcap3_mv6100.elf'
    str_file_path =  str_elf_dir_path + '/' + str_elf_file
    elf_file = ElfFile(str_file_path)

    d_map = elf_file.get_mapping()
    str_json_file = str_elf_file.replace('.elf','_map.json')
    str_json_file_path = str_script_dirpath + '/' + str_json_file

    with open(str_json_file_path, 'w', encoding='utf-8') as jsonfile:  
        json.dump(d_map, jsonfile, indent=4)

    # d_instr = elf_file.get_instructions()

    # d_dec_all_instr = {}
    # for str_symb_name in d_instr:
    #     if '_CHECKSUM' != str_symb_name and 'csd_ppc_signature' != str_symb_name:
    #         str_symb_addr = d_instr[str_symb_name]['address']
    #         d_dec_all_instr[str_symb_name] = {'address': str_symb_addr, 'instructions': {}}

    #         for str_instr_addr, str_instr_bytes in d_instr[str_symb_name]['instructions'].items():
    #             b_instr, d_dec_instr = disassembler.decode_instr(int(str_instr_bytes,16))
    #             if b_instr:
    #                 d_dec_all_instr[str_symb_name]['instructions'][str_instr_addr] =  d_dec_instr

    # str_json_file = str_elf_file.replace('.elf','_instr.json')
    # str_json_file_path = str_script_dirpath + '/' + str_json_file

    # with open(str_json_file_path, 'w', encoding='utf-8') as jsonfile:  
    #     json.dump(d_dec_all_instr, jsonfile, indent=4)

    # d_csd_ppc_cu = {}
    # d_csd_ppc_cu['CSD_PPC_CU71'] = {}
    # d_csd_ppc_cu['CSD_PPC_CU79'] = {}

    # for str_symb_name in d_dec_all_instr:
    #     for str_instr_addr, d_instr in d_dec_all_instr[str_symb_name]['instructions'].items():
    #         if 'dcba' == d_instr['mnemonic']:
    #             if str_symb_name not in d_csd_ppc_cu['CSD_PPC_CU71']:
    #                 d_csd_ppc_cu['CSD_PPC_CU71'][str_symb_name] = {'address': str_symb_addr, 'instructions': {}}
    #             d_csd_ppc_cu['CSD_PPC_CU71'][str_symb_name]['instructions'][str_instr_addr] = d_instr

    #         if 'bx' == d_instr['mnemonic'] or 'bcx' == d_instr['mnemonic']:
    #             if 1 == d_instr['fields']['AA']:
    #                 if str_symb_name not in  d_csd_ppc_cu['CSD_PPC_CU79']:
    #                     d_csd_ppc_cu['CSD_PPC_CU79'][str_symb_name] = {'address': str_symb_addr, 'instructions': {}}
    #                 d_csd_ppc_cu['CSD_PPC_CU79'][str_symb_name]['instructions'][str_instr_addr] = d_instr

    # print(d_csd_ppc_cu)

