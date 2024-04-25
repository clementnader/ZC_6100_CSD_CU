
from rtpc_core.prod.sw import SwConstTypes

class ReporterXlsx(object):

    str_dir_path = None

    def __init__(self, str_dir_path):
        self.str_dir_path = str_dir_path

    def report_constr(self, d_sw_constr, d_sw_constr_result):

        for str_const_id in d_sw_constr:

            str_type = d_sw_constr[str_const_id]['type']

            if SwConstTypes.SW_CONST_EXE_MAP_LIM_SECT.value == str_type:
                d_result[str_const_id] = self._report_constr_map_lim_sect(d_sw_constr[str_const_id], d_sw_constr_result[str_const_id])
            elif SwConstTypes.SW_CONST_EXE_MAP_OFF_SECT.value == str_type:
                d_result[str_const_id] = self._report_constr_map_off_sect(d_sw_constr[str_const_id], d_sw_constr_result[str_const_id])
            elif SwConstTypes.SW_CONST_EXE_MAP_OCCUR_SYMB.value == str_type:
                d_result[str_const_id] = self._report_constr_map_occur_symb(d_sw_constr[str_const_id], d_sw_constr_result[str_const_id])
            elif SwConstTypes.SW_CONST_EXE_INSTR_MAND.value == str_type :
                d_result[str_const_id] = self._report_constr_instr_mand(d_sw_constr[str_const_id], d_sw_constr_result[str_const_id])
            elif SwConstTypes.SW_CONST_EXE_INSTR_FORB.value == str_type :
                d_result[str_const_id] = self._report_constr_instr_forb_occur(d_sw_constr[str_const_id], d_sw_constr_result[str_const_id])
            elif SwConstTypes.SW_CONST_EXE_INSTR_OCCUR.value == str_type:
                d_result[str_const_id] = self._report_constr_instr_forb_occur(d_sw_constr[str_const_id], d_sw_constr_result[str_const_id])
            elif SwConstTypes.SW_CONST_EXE_INSTR_OFF.value == str_type:
                d_result[str_const_id] = self._report_constr_instr_off(d_sw_constr[str_const_id], d_sw_constr_result[str_const_id])
            elif SwConstTypes.SW_CONST_EXE_COMM_STR.value == str_type:
                d_result[str_const_id] = self._report_constr_comm_str(d_sw_constr[str_const_id], d_sw_constr_result[str_const_id])
            elif SwConstTypes.SW_CONST_LOG_COMP_OPT.value == str_type:
                d_result[str_const_id] = self._report_constr_log_comp_opt(d_sw_constr[str_const_id], d_sw_constr_result[str_const_id])
            elif SwConstTypes.SW_CONST_LOG_OCCUR_WARN.value == str_type:
                d_result[str_const_id] = self._report_constr_log_occur_warn(d_sw_constr[str_const_id], d_sw_constr_result[str_const_id])                 
            else:
                d_result[str_const_id] = self._report_constr_prod(d_sw_constr[str_const_id], d_sw_constr_result[str_const_id])


    def _report_constr_instr_mand(self, d_sw_constr, d_sw_constr_result):

        for str_symb_name, i_addr_off in d_sw_constr['instr'].items():
            
