# -*-coding:utf-8 -*
import subprocess
import sys
import re
import os
import stat
import json

from enum import Enum, auto


class Endianness(Enum):
    NO_ENDIANNESS = auto()
    BIG_ENDIAN = auto()
    LITTLE_ENDIAN = auto()


class Disasm(object):

    i_nb_bits = None
    e_endianness = Endianness.NO_ENDIANNESS

    d_prim_opcd_field = {}
    str_sec_opcd_field_name = None
    d_sec_opcd_masks = {}
    d_fields = {}
    d_forms = {}
    d_instr = {}

    def __init__(self, d_proc):

        self.i_nb_bits = d_proc['nb_bits']

        str_endianness = d_proc['endianness']
        self._set_endianness(str_endianness)
        self._set_prim_opcd_field(d_proc['prim_opcd_field'])

        if 'sec_opcd_field' in d_proc and 'sec_opcd_masks' in d_proc:
            self._set_sec_opcd_field(d_proc['sec_opcd_field'])
            self._set_sec_opcd_masks(d_proc['sec_opcd_masks'])

        self._set_fields(d_proc['fields'])
        self._set_forms(d_proc['forms'])
        self._set_instr(d_proc['instr'])

    def _set_endianness(self,str_endianness):

        if 'big-endian' == str_endianness:
            self.e_endianness = Endianness.BIG_ENDIAN
        elif "little-endian" == str_endianness:
            self.e_endianness = Endianness.LITTLE_ENDIAN
        else:
            pass

    def _set_prim_opcd_field(self, d_prim_opcd_field):

        self.d_prim_opcd_field = {}
        self.d_prim_opcd_field['name'] = d_prim_opcd_field['name']

        i_start = d_prim_opcd_field['bit_start']
        i_length = d_prim_opcd_field['bit_length']
        d_shifts = self._get_field_shifts(i_start, i_length)
        self.d_prim_opcd_field['left'] = d_shifts['left']
        self.d_prim_opcd_field['right'] = d_shifts['right']
        self.d_prim_opcd_field['bit_length'] = i_length

    def _set_sec_opcd_field(self, str_sec_opcd_field_name):
        self.str_sec_opcd_field_name = str_sec_opcd_field_name

    def _set_sec_opcd_masks(self, d_sec_opcd_masks):

        for str_mask, d_mask in d_sec_opcd_masks.items():

            i_start = d_mask['bit_start']
            i_length = d_mask['bit_length']
            d_shifts = self._get_field_shifts(i_start, i_length)
            if str_mask not in self.d_sec_opcd_masks:
                self.d_sec_opcd_masks[str_mask] = {}
            self.d_sec_opcd_masks[str_mask]['left'] = d_shifts['left']
            self.d_sec_opcd_masks[str_mask]['right'] = d_shifts['right']

                    
    def _set_fields(self, d_fields):
        self.d_fields = d_fields

    def _set_forms(self, d_forms):
        self.d_forms = d_forms
    
    def _set_instr(self, d_instr):
        self.d_instr  = d_instr

    def _get_field_shifts(self,i_start, i_length):

        if Endianness.BIG_ENDIAN == self.e_endianness:
            i_left_shift = i_start
        elif Endianness.LITTLE_ENDIAN == self.e_endianness:
            i_left_shift =  self.i_nb_bits - i_start - i_length - 1

        i_right_shift = self.i_nb_bits - i_length
        
        d_shifts = {'left': i_left_shift, 'right': i_right_shift}
        return d_shifts

    def _get_field_value(self, i_bytes, i_left, i_right):
        i_field_value = i_bytes << i_left
        i_field_value = i_field_value & 0xFFFFFFFF
        i_field_value = i_field_value >> i_right

        return i_field_value
    

    def decode_instr(self, i_bytes):

        b_instr = False
        
        d_dec_instr = {'mnemonic': {}, 'fields': {}}

        i_left = self.d_prim_opcd_field['left']
        i_right = self.d_prim_opcd_field['right']
        i_prim_opcd = self._get_field_value(i_bytes, i_left, i_right)

        str_prim_opcd_field_name = self.d_prim_opcd_field['name']
        d_dec_instr['fields'][str_prim_opcd_field_name] = i_prim_opcd

        str_prim_opcd = str(i_prim_opcd)
        if str_prim_opcd in self.d_instr:
            for str_form_name in self.d_instr[str_prim_opcd]:
                if str_form_name in self.d_forms:
                    if 'sec_opcd_mask' in self.d_forms[str_form_name]:
                        str_mask = self.d_forms[str_form_name]['sec_opcd_mask']

                        i_left = self.d_sec_opcd_masks[str_mask]['left']
                        i_right = self.d_sec_opcd_masks[str_mask]['right']
                        i_sec_opcd = self._get_field_value(i_bytes, i_left, i_right)
                        
                        str_sec_opcd = str(i_sec_opcd)
                        if str_sec_opcd in self.d_instr[str_prim_opcd][str_form_name]:

                            str_mnem = self.d_instr[str_prim_opcd][str_form_name][str_sec_opcd]
                            d_dec_instr['mnemonic'] = str_mnem
                            d_dec_instr['fields'][self.str_sec_opcd_field_name] = i_sec_opcd
                            b_instr = True                        

                    else:
                        str_mnem = self.d_instr[str_prim_opcd][str_form_name]
                        d_dec_instr['mnemonic'] = str_mnem
                        b_instr = True

                    if b_instr:
                        for str_field_name, i_bit_start in self.d_forms[str_form_name]['fields'].items():

                            i_bit_length = self.d_fields[str_field_name]
                            d_shifts = self._get_field_shifts(i_bit_start,i_bit_length)
                            i_field_value = self._get_field_value(i_bytes,d_shifts['left'], d_shifts['right'])
                            d_dec_instr['fields'][str_field_name] = i_field_value
                        break

        return b_instr, d_dec_instr
            
 

if __name__ == '__main__':

    str_script_filepath = os.path.abspath(__file__)
    str_script_dirpath = os.path.dirname(str_script_filepath)
    str_json_filepath = str_script_dirpath + '/proc_tests.json'

    with open(str_json_filepath, 'r') as json_file:
        d_proc = json.load(json_file)

    disassembler = Disasm(d_proc)

    l_instr = []
    l_instr.append('38600384')
    l_instr.append('3d200011')
    l_instr.append('38095f78')
    l_instr.append('7c0803a6')
    l_instr.append('4e800021')

    for str_instr in l_instr:
        d_dec_instr = disassembler.decode_instr(int(str_instr,16))
        print(d_dec_instr)

    

    