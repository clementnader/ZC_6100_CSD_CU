# -*-coding:utf-8 -*
import sys
import os
import json
import pprint

from enum import Enum

from core.file.file import *
from core.file.arch import ArchiveFile
from core.file.log import LogFile


class SwConst:

    SW_CONST_EXE_MAP_LIM_SECT = 'EXE_MAP_LIM_SECT'
    SW_CONST_EXE_MAP_OFF_SECT = 'EXE_MAP_OFF_SECT'
    SW_CONST_EXE_MAP_OCCUR_SYMB = 'EXE_MAP_OCCUR_SYMB'
    SW_CONST_EXE_INSTR_MAND = 'EXE_INSTR_MAND'
    SW_CONST_EXE_INSTR_FORB = 'EXE_INSTR_FORB'
    SW_CONST_EXE_INSTR_OCCUR = 'EXE_INSTR_OCCUR'
    SW_CONST_EXE_INSTR_OFF = 'EXE_INSTR_OFF'
    SW_CONST_EXE_COMM_STR = 'EXE_COMM_STR'
    SW_CONST_LOG_COMP_OPT = 'LOG_COMP_OPT'
    SW_CONST_LOG_OCCUR_WARN = 'LOG_OCCUR_WARN'

    d_text = {
        SW_CONST_EXE_MAP_LIM_SECT: 'Executable file(s) - Mapping limits of sections',
        SW_CONST_EXE_MAP_OFF_SECT: 'Executable file(s) - Mapping offsets of sections',
        SW_CONST_EXE_MAP_OCCUR_SYMB: 'Executable file(s) - Mapping of specific symbols',
        SW_CONST_EXE_INSTR_MAND: 'Executable file(s) - Mandatory instructions',
        SW_CONST_EXE_INSTR_FORB: 'Executable file(s) - Forbidden instructions',
        SW_CONST_EXE_INSTR_OCCUR: 'Executable file(s) - Occurences of specific instructions',
        SW_CONST_EXE_INSTR_OFF: 'Executable file(s) - Offset between instructions addresses',
        SW_CONST_EXE_COMM_STR: 'Executable file(s) - Comment strings',
        SW_CONST_LOG_COMP_OPT: 'Log file(s) - Compilation options',
        SW_CONST_LOG_OCCUR_WARN: 'Log file(s) - Compilation of warnings'
    }

    @classmethod
    def get_tuple(cls):
        return ((str_type, str_text) for str_type, str_text in cls.d_text.items())

    @classmethod
    def get_text(cls, str_type):
        return cls.d_text[str_type]


class SwConstResult(Enum):
    SW_CONST_RESULT_OK = 'OK'
    SW_CONST_RESULT_NOK = 'NOK'
    SW_CONST_RESULT_TBA = 'TBA'


class Sw(object):

    i_nb_sw_inst = None
    d_const = {}

    d_proc = {}

    d_instr = {}
    d_map = {}
    d_comm = {}

    str_sw_dirpath = None
    d_files = {}

    def __init__(self, d_sw_const, d_hw_proc, str_sw_dirpath, d_sw_files):

        self.d_const = d_sw_const
        self.d_proc = d_hw_proc

        # self.str_sw_dirpath = str_sw_dirpath
        for str_file_name in d_sw_files:
            str_file_path = str_sw_dirpath
            str_file_path += '/' + str(d_sw_files[str_file_name])
            str_file_path += '/' + str_file_name
            self.d_files[str_file_name] = str_file_path

    def _set_instr(self, str_file_path):
        pass

    def _set_map(self, str_file_name):
        pass

    def _set_comm(self, str_file_name):
        pass

    def _get_map_symb_addr_val_size_align(self, str_file_name, str_symb_sect, str_symb_name):

        i_symb_addr_val = None
        i_symb_size_align = None

        for str_symb_addr_val, l_symb in self.d_map[str_file_name][str_symb_sect].items():
            for d_symb in l_symb:
                if str_symb_name == d_symb['name']:
                    i_symb_addr_val = int(str_symb_addr_val, 16)
                    i_symb_size_align = int(d_symb['size_align'], 16)
            if i_symb_addr_val is not None:
                break

        return i_symb_addr_val, i_symb_size_align

    def check_const(self):

        d_result = {}

        for str_const_id in self.d_const:

            str_type = self.d_const[str_const_id]['type']

            d_result[str_const_id] = {}

            if SwConst.SW_CONST_EXE_MAP_LIM_SECT == str_type or SwConst.SW_CONST_EXE_MAP_OFF_SECT == str_type \
                    or SwConst.SW_CONST_EXE_MAP_OCCUR_SYMB == str_type:

                for str_file_name in self.d_const[str_const_id]['files']:
                    if str_file_name not in self.d_map:
                        self._set_map(str_file_name)

            elif SwConst.SW_CONST_EXE_INSTR_MAND == str_type or SwConst.SW_CONST_EXE_INSTR_FORB == str_type \
                    or SwConst.SW_CONST_EXE_INSTR_OCCUR == str_type or SwConst.SW_CONST_EXE_INSTR_OFF == str_type:

                for str_file_name in self.d_const[str_const_id]['files']:
                    if str_file_name not in self.d_instr:
                        self._set_instr(str_file_name)

            elif SwConst.SW_CONST_EXE_COMM_STR == str_type:
                for str_file_name in self.d_const[str_const_id]['files']:
                    if str_file_name not in self.d_comm:
                        self._set_comm(str_file_name)

            print(f'Checking constraint: {str_const_id}, type: {str_type}')

            if SwConst.SW_CONST_EXE_MAP_LIM_SECT == str_type:
                d_result[str_const_id] = self._check_constr_map_lim_sect(self.d_const[str_const_id])
            elif SwConst.SW_CONST_EXE_MAP_OFF_SECT == str_type:
                d_result[str_const_id] = self._check_constr_map_off_sect(self.d_const[str_const_id])
            elif SwConst.SW_CONST_EXE_MAP_OCCUR_SYMB == str_type:
                d_result[str_const_id] = self._check_constr_map_occur_symb(self.d_const[str_const_id])
            elif SwConst.SW_CONST_EXE_INSTR_MAND == str_type:
                d_result[str_const_id] = self._check_constr_instr_mand(self.d_const[str_const_id])
            elif SwConst.SW_CONST_EXE_INSTR_FORB == str_type:
                d_result[str_const_id] = self._check_constr_instr_forb_occur(self.d_const[str_const_id])
            elif SwConst.SW_CONST_EXE_INSTR_OCCUR == str_type:
                d_result[str_const_id] = self._check_constr_instr_forb_occur(self.d_const[str_const_id])
            elif SwConst.SW_CONST_EXE_INSTR_OFF == str_type:
                d_result[str_const_id] = self._check_constr_instr_off(self.d_const[str_const_id])
            elif SwConst.SW_CONST_EXE_COMM_STR == str_type:
                d_result[str_const_id] = self._check_constr_comm_str(self.d_const[str_const_id])
            elif SwConst.SW_CONST_LOG_COMP_OPT == str_type:
                d_result[str_const_id] = self._check_constr_log_comp_opt(self.d_const[str_const_id])
            elif SwConst.SW_CONST_LOG_OCCUR_WARN == str_type:
                d_result[str_const_id] = self._check_constr_log_occur_warn(self.d_const[str_const_id])
            else:
                d_result[str_const_id] = self._check_constr_prod(self.d_const[str_const_id])

        return d_result

    def _check_constr_prod(self, d_constr):
        pass

    def _check_constr_map_off_sect(self, d_constr_map_off_sect):

        b_result = True

        d_result_map_off_sect = {}

        for str_sect_name, d_off_sect in d_constr_map_off_sect['sect'].items():
            str_ref_file_name = d_off_sect['ref']

            if 'excl' in d_constr_map_off_sect['sect'][str_sect_name]:
                l_excl_symb_names = d_constr_map_off_sect['sect'][str_sect_name]['excl']
            else:
                l_excl_symb_names = None

            d_result_map_off_sect[str_sect_name] = []

            for str_symb_addr, l_symb in self.d_map[str_ref_file_name][str_sect_name].items():

                d_symb_addr_names = {}

                b_incl_symb_addr = True
                if l_excl_symb_names is not None:
                    for d_symb in l_symb:
                        if d_symb['name'] in l_excl_symb_names:
                            b_incl_symb_addr = False
                            break

                if b_incl_symb_addr:

                    l_symb_names = []
                    for d_symb in l_symb:
                        l_symb_names.append(d_symb['name'])

                    d_symb_addr_names['symb_names'] = l_symb_names
                    d_symb_addr_names['symb_addr'] = {}
                    d_symb_addr_names['symb_addr'][str_ref_file_name] = '0x' + str_symb_addr
                    d_symb_addr_names['off'] = True

                    i_symb_addr = int(str_symb_addr, 16)

                    for str_file_name, str_addr_off in d_off_sect['off'].items():

                        i_symb_addr_with_off = i_symb_addr + int(str_addr_off, 16)
                        str_symb_addr_with_off = '%08x' % i_symb_addr_with_off

                        if str_symb_addr_with_off in self.d_map[str_file_name][str_sect_name]:
                            b_symb_off = True
                            l_symb_off = self.d_map[str_file_name][str_sect_name][str_symb_addr_with_off]

                            l_symb_off_names = []
                            for d_symb_off in l_symb_off:
                                l_symb_off_names.append(d_symb_off['name'])

                            if len(l_symb_names) == len(l_symb_off_names):
                                for str_symb_name in l_symb_names:
                                    if str_symb_name not in l_symb_off_names:
                                        b_symb_off = False
                                        break
                            else:
                                b_symb_off = False
                        else:
                            b_symb_off = False

                        d_symb_addr_names['symb_addr'][str_file_name] = '0x' + str_symb_addr_with_off
                        if b_result and not b_symb_off:
                            b_result = False

                if d_symb_addr_names:
                    d_result_map_off_sect[str_sect_name].append(d_symb_addr_names)

        if b_result:
            e_result = SwConstResult.SW_CONST_RESULT_OK
        else:
            e_result = SwConstResult.SW_CONST_RESULT_NOK

        d_result = {'result': e_result, 'map_off_sect': d_result_map_off_sect}

        return d_result

    def _check_constr_map_lim_sect(self, d_constr_map_lim_sect):

        b_result = True
        d_result_map_lim_sect = {}

        for str_file_name in d_constr_map_lim_sect['files']:
            d_result_map_lim_sect[str_file_name] = {}

            for str_sect_name, d_lim in d_constr_map_lim_sect['sect'].items():

                d_result_map_lim_sect[str_file_name][str_sect_name] = {}

                # Start limit to check ?
                if 'start' in d_lim:
                    b_start = True
                    str_symb_sect = d_lim['start']['symb_sect']
                    str_symb_name = d_lim['start']['symb_name']
                    i_start_addr, i_size_align = self._get_map_symb_addr_val_size_align(
                        str_file_name, str_symb_sect, str_symb_name)

                    if 'symb_off_sect' in d_lim['start'] and 'symb_off_name' in d_lim['start']:
                        str_symb_sect = d_lim['start']['symb_off_sect']
                        str_symb_name = d_lim['start']['symb_off_name']
                        i_start_addr_off, i_size_align = self._get_map_symb_addr_val_size_align(
                            str_file_name, str_symb_sect, str_symb_name)
                        i_start_addr += i_start_addr_off

                    b_start_addr_inc = d_lim['start']['symb_addr_incl']
                else:
                    b_start = False
                    i_start_addr = 0

                # End limit to check ?
                if 'end' in d_lim:

                    b_end = True
                    str_symb_sect = d_lim['end']['symb_sect']
                    str_symb_name = d_lim['end']['symb_name']
                    i_end_addr, i_size_align = self._get_map_symb_addr_val_size_align(
                        str_file_name, str_symb_sect, str_symb_name)

                    if 'symb_off_sect' in d_lim['end'] and 'symb_off_name' in d_lim['end']:
                        str_symb_sect = d_lim['end']['symb_off_sect']
                        str_symb_name = d_lim['end']['symb_off_name']
                        i_end_addr_off, i_size_align = self._get_map_symb_addr_val_size_align(
                            str_file_name, str_symb_sect, str_symb_name)
                        i_end_addr += i_end_addr_off

                    b_end_addr_inc = d_lim['end']['symb_addr_incl']
                else:
                    b_end = False

                # Symbols to exclude?
                if 'excl' in d_lim:
                    l_excl_symb_names = d_lim['excl']
                else:
                    l_excl_symb_names = None

                i_low_addr = None
                str_symb_low_addr = None
                i_high_addr = None
                str_symb_high_addr = None

                for str_symb_addr, l_symb in self.d_map[str_file_name][str_sect_name].items():

                    b_incl_symb_addr = True
                    if l_excl_symb_names is not None:
                        for d_symb in l_symb:
                            if d_symb['name'] in l_excl_symb_names:
                                b_incl_symb_addr = False
                                break

                    if b_incl_symb_addr:
                        i_symb_addr = int(str_symb_addr, 16)

                        if b_start:
                            if i_low_addr is None or i_symb_addr < i_low_addr:
                                i_low_addr = i_symb_addr
                                str_symb_low_addr = str_symb_addr
                                if b_result:
                                    if i_start_addr == i_symb_addr and not b_start_addr_inc:
                                        b_result = False
                                    elif i_start_addr > i_symb_addr:
                                        b_result = False
                        if b_end:
                            if i_high_addr is None or i_symb_addr > i_high_addr:
                                i_high_addr = i_symb_addr
                                str_symb_high_addr = str_symb_addr
                                if b_result:
                                    if i_end_addr == i_symb_addr and not b_end_addr_inc:
                                        b_result = False
                                    elif i_end_addr < i_symb_addr:
                                        b_result = False

                if b_start:
                    l_symb_names = []
                    for d_symb in self.d_map[str_file_name][str_sect_name][str_symb_low_addr]:
                        l_symb_names.append(d_symb['name'])
                    d_result_map_lim_sect[str_file_name][str_sect_name]['start'] = {
                        'addr': '0x%08x' % i_low_addr, 'symb': l_symb_names}
                else:
                    d_result_map_lim_sect[str_file_name][str_sect_name]['start'] = {'addr': '', 'symb': ''}

                if b_end:
                    l_symb_names = []
                    for d_symb in self.d_map[str_file_name][str_sect_name][str_symb_high_addr]:
                        l_symb_names.append(d_symb['name'])
                    d_result_map_lim_sect[str_file_name][str_sect_name]['end'] = {
                        'addr': '0x%08x' % i_high_addr, 'symb': l_symb_names}
                else:
                    d_result_map_lim_sect[str_file_name][str_sect_name]['end'] = {'addr': '', 'symb': ''}

        if b_result:
            e_result = SwConstResult.SW_CONST_RESULT_OK
        else:
            e_result = SwConstResult.SW_CONST_RESULT_NOK

        d_result = {'result': e_result, 'map_lim_sect': d_result_map_lim_sect}

        return d_result

    def _check_constr_map_occur_symb(self, d_constr_map_occur_symb):

        d_result_map_occur_symb = {}

        for str_file_name in d_constr_map_occur_symb['files']:
            d_result_map_occur_symb[str_file_name] = {}

            for str_sect_name, l_symb_names in d_constr_map_occur_symb['symb'].items():
                d_result_map_occur_symb[str_file_name][str_sect_name] = {}
                for str_symb_addr, l_symb in self.d_map[str_file_name][str_sect_name].items():
                    for d_symb in l_symb:
                        if d_symb['name'] in l_symb_names:
                            d_result_map_occur_symb[str_file_name][str_sect_name][d_symb['name']] = {
                                'addr': '0x' + str_symb_addr, 'size': '0x' + d_symb['size_align']}

        e_result = SwConstResult.SW_CONST_RESULT_TBA
        d_result = {'result': e_result, 'map_occur_symb': d_result_map_occur_symb}

        return d_result

    def _check_constr_instr_mand(self, d_constr_instr_mand):

        b_result = True
        d_result_instr_mand = {}

        for str_file_name, d_symb_name_addr_off_const_instr in d_constr_instr_mand['instr'].items():
            d_result_instr_mand[str_file_name] = {}

            for str_symb_name in d_symb_name_addr_off_const_instr:

                str_symb_addr = self.d_instr[str_file_name][str_symb_name]['address']
                i_symb_addr = int(str_symb_addr, 16)

                if str_symb_name not in d_result_instr_mand[str_file_name]:
                    d_result_instr_mand[str_file_name][str_symb_name] = {'addr': "0x%08x" % i_symb_addr, 'instr': {}}

                for str_instr_addr_off, d_const_instr in d_symb_name_addr_off_const_instr[str_symb_name].items():

                    i_instr_addr_off = int(str_instr_addr_off, 16)
                    i_instr_addr = i_symb_addr + i_instr_addr_off
                    str_instr_addr = "%x" % i_instr_addr

                    b_instr_mand = False

                    if str_instr_addr in self.d_instr[str_file_name][str_symb_name]['instructions']:
                        d_instr = self.d_instr[str_file_name][str_symb_name]['instructions'][str_instr_addr]

                        str_mnem = d_const_instr['mnem']

                        if str_mnem == d_instr['mnemonic']:
                            str_instr_addr = "0x%08x" % i_instr_addr
                            d_result_instr_mand[str_file_name][str_symb_name]['instr'][str_instr_addr] = {
                                'mnem': str_mnem, 'fields': {}}

                            if 'fields' in d_const_instr:
                                b_fields = True
                                for str_field_name in d_const_instr['fields']:
                                    d_result_instr_mand[str_file_name][str_symb_name]['instr'][
                                        str_instr_addr]['fields'][str_field_name] = d_instr['fields'][str_field_name]
                                    if d_const_instr['fields'][str_field_name] != d_instr['fields'][str_field_name]:
                                        if b_fields:
                                            b_fields = False
                                if b_fields:
                                    b_instr_mand = True
                            else:
                                b_instr_mand = True
                        else:
                            b_instr_mand = False
                            d_result_instr_mand[str_file_name][str_symb_name]['instr_addr'][str_instr_addr] = d_instr

                    else:
                        b_instr_mand = False
                        d_result_instr_mand[str_file_name][str_symb_name]['instr_addr'][str_instr_addr] = None

                    if b_result and not b_instr_mand:
                        b_result = False

        if b_result:
            e_result = SwConstResult.SW_CONST_RESULT_OK
        else:
            e_result = SwConstResult.SW_CONST_RESULT_NOK

        d_result = {'result': e_result, 'instr_mand': d_result_instr_mand}

        return d_result

    def _check_constr_instr_forb_occur(self, d_constr_instr_forb_occur):

        b_result = True
        d_result_instr_forb_occur = {}
        str_sw_const_type = d_constr_instr_forb_occur['type']

        for str_file_name in d_constr_instr_forb_occur['files']:
            d_result_instr_forb_occur[str_file_name] = {}

            for d_const_instr in d_constr_instr_forb_occur['instr']:
                str_mnem = d_const_instr['mnem']

                for str_symb_name in self.d_instr[str_file_name]:
                    for str_instr_addr, d_instr in self.d_instr[str_file_name][str_symb_name]['instructions'].items():
                        b_instr_forb_occur = False

                        if str_mnem == d_instr['mnemonic']:
                            if 'fields' in d_const_instr:
                                b_fields = True
                                for str_field_name in d_const_instr['fields']:
                                    if d_const_instr['fields'][str_field_name] != d_instr['fields'][str_field_name]:
                                        b_fields = False
                                        break

                                if b_fields:
                                    b_instr_forb_occur = True
                            else:
                                b_instr_forb_occur = True

                        if b_instr_forb_occur:
                            if str_symb_name not in d_result_instr_forb_occur[str_file_name]:
                                str_symb_addr = self.d_instr[str_file_name][str_symb_name]['address']
                                i_symb_addr = int(str_symb_addr, 16)
                                d_result_instr_forb_occur[str_file_name][str_symb_name] = {
                                    'addr': "0x%08x" % i_symb_addr, 'instr': {}}

                            i_inst_addr = int(str_instr_addr,16)
                            str_instr_addr = "0x%08x" % i_inst_addr

                            if 'fields' in d_const_instr:
                                d_result_instr_forb_occur[str_file_name][str_symb_name]['instr'][str_instr_addr] = {
                                    'mnem': str_mnem, 'fields': d_const_instr['fields']}
                            else:
                                d_result_instr_forb_occur[str_file_name][str_symb_name]['instr'][str_instr_addr] = {
                                    'mnem': str_mnem}

                            if b_result and SwConst.SW_CONST_EXE_INSTR_FORB == str_sw_const_type:
                                b_result = False

        if SwConst.SW_CONST_EXE_INSTR_FORB == str_sw_const_type:
            if b_result:
                e_result = SwConstResult.SW_CONST_RESULT_OK
            else:
                e_result = SwConstResult.SW_CONST_RESULT_NOK

        elif SwConst.SW_CONST_EXE_INSTR_OCCUR == str_sw_const_type:
            e_result = SwConstResult.SW_CONST_RESULT_TBA
        else:
            e_result = SwConst.SwConstResult.SW_CONST_RESULT_NOK

        d_result = {'result': e_result, 'instr_forb_occur': d_result_instr_forb_occur}

        return d_result

    def _check_constr_instr_off(self, d_constr_instr_off):

        b_result = True
        d_result_instr_off = {}

        d_const_instr = d_constr_instr_off['instr']
        str_constr_instr_mnem1_incl = d_const_instr['incl']['mnem1']
        str_constr_instr_mnem2_incl = d_const_instr['incl']['mnem2']
        l_constr_instr_mnem1_incl = d_const_instr['excl']['mnem1']
        l_constr_instr_mnem2_incl = d_const_instr['excl']['mnem2']
        i_constr_instr_addr_off = d_const_instr['off']

        for str_file_name in d_constr_instr_off['files']:
            d_result_instr_off[str_file_name] = {}

            i_instr_addr_mnem1 = None
            i_instr_addr_mnem2 = None
            b_diff = False

            for str_symb_name in self.d_instr[str_file_name]:
                for str_instr_addr, d_instr in self.d_instr[str_file_name][str_symb_name]['instructions'].items():

                    if str_constr_instr_mnem1_incl == d_instr['mnemonic']:
                        i_instr_addr_mnem1 = int(str_instr_addr, 16)
                        b_diff = True
                    elif d_instr['mnemonic'] in l_constr_instr_mnem1_incl \
                            or d_instr['mnemonic'] in l_constr_instr_mnem2_incl:
                        b_diff = False
                    elif str_constr_instr_mnem2_incl == d_instr['mnemonic'] and b_diff:
                        b_diff = False
                        i_instr_addr_mnem2 = int(str_instr_addr, 16)

                        i_instr_addr_off = i_instr_addr_mnem2 - i_instr_addr_mnem1
                        if i_instr_addr_off == i_constr_instr_addr_off and b_instr_addr_off_inc:
                            b_instr_addr_off = True
                        elif i_instr_addr_off < i_constr_instr_addr_off:
                            b_instr_addr_off = True
                        else:
                            b_instr_addr_off = False
                            if b_result:
                                b_result = False

                        if str_symb_name not in d_result_instr_off[str_file_name]:
                            i_symb_addr = int(self.d_instr[str_file_name][str_symb_name]['address'], 16)
                            str_symb_addr = "0x%08x" % i_symb_addr
                            d_result_instr_off[str_file_name][str_symb_name] = {
                                'symb_addr': str_symb_addr, 'inst_addr': []}

                        str_instr_addr_mnem1 = "0x%08x" % i_instr_addr_mnem1
                        str_instr_addr_mnem2 = "0x%08x" % i_instr_addr_mnem2
                        str_instr_addr_off = "0x%08x" % i_instr_addr_off
                        d_instr_addr_off = {'mnem1': str_instr_addr_mnem1, 'mnem2': str_instr_addr_mnem2,
                                            'off': str_instr_addr_off}
                        d_result_instr_off[str_file_name][str_symb_name]['inst_addr'].append(d_instr_addr_off)

        if b_result:
            e_result = SwConstResult.SW_CONST_RESULT_OK
        else:
            e_result = SwConstResult.SW_CONST_RESULT_NOK

        d_result = {'result': e_result, 'instr_off': d_result_instr_off}

        return d_result

    def _check_constr_comm_str(self, d_constr_comm_str):

        b_result = True
        d_result_comm_str = {}

        for str_file_name in d_constr_comm_str['files']:

            l_comm_str = []

            idx_comm_str = 0
            str_curr_comm_str = None

            for str_comm_str in self.d_comm[str_file_name]:
                if str_comm_str == str_curr_comm_str:
                    l_comm_str[idx_comm_str]['number'] += 1
                else:
                    if str_curr_comm_str is not None:
                        idx_comm_str += 1
                    str_curr_comm_str = str_comm_str
                    d_comm_str = {'string': str_comm_str, 'number': 1}
                    l_comm_str.append(d_comm_str)

            d_result_comm_str[str_file_name] = l_comm_str

            if len(d_constr_comm_str['comm']) == len(l_comm_str):
                for idx_comm_str, d_comm_str in enumerate(d_constr_comm_str['comm']):
                    if d_comm_str['string'] == l_comm_str[idx_comm_str]['string']:
                        if d_comm_str['min']:
                            if l_comm_str[idx_comm_str]['number'] < d_comm_str['number']:
                                if b_result:
                                    b_result = False
                        else:
                            if l_comm_str[idx_comm_str]['number'] != d_comm_str['number']:
                                if b_result:
                                    b_result = False
                    else:
                        if b_result:
                            b_result = False
            else:
                b_result = False

        if b_result:
            e_result = SwConstResult.SW_CONST_RESULT_OK
        else:
            e_result = SwConstResult.SW_CONST_RESULT_NOK

        d_result = {'result': e_result, 'comm_str': d_result_comm_str}

        return d_result

    def _check_constr_log_comp_opt(self, d_constr_log_comp_opt):

        b_result = True
        d_result_log_comp_opt = {}

        str_comp = d_constr_log_comp_opt['comp_opt']['comp']
        str_lang = d_constr_log_comp_opt['comp_opt']['lang']
        d_constr_comp_opt = d_constr_log_comp_opt['comp_opt']['opt']

        for str_file_name in d_constr_log_comp_opt['files']:

            d_result_log_comp_opt[str_file_name] = {}

            str_file_path = self.d_files[str_file_name]
            d_comp_opt = LogFile.get_comp_opt(str_file_path, str_comp, str_lang)

            for str_opt, b_opt_use in d_constr_comp_opt.items():
                if b_opt_use and str_opt not in d_comp_opt:
                    if b_result:
                        b_result = False
                elif not b_opt_use and str_opt in d_comp_opt:
                    if b_result:
                        b_result = False

            d_result_log_comp_opt[str_file_name] = {'lang': str_lang, 'comp_opt': d_comp_opt}

        if b_result:
            e_result = SwConstResult.SW_CONST_RESULT_OK
        else:
            e_result = SwConstResult.SW_CONST_RESULT_NOK

        d_result = {'result': e_result, 'log_comp_opt': d_result_log_comp_opt}

        return d_result

    def _check_constr_log_occur_warn(self, d_constr_log_occur_warn):

        d_result_log_occur_warn = {}

        for str_file_name in d_constr_log_occur_warn['files']:
            str_file_path = self.d_files[str_file_name]

            d_occur_warn = LogFile.get_comp_warn(str_file_path)
            d_result_log_occur_warn[str_file_name] = d_occur_warn

        e_result = SwConstResult.SW_CONST_RESULT_TBA
        d_result = {'result': e_result, 'log_occur_warn': d_result_log_occur_warn}

        return d_result
