import os
import json
from datetime import datetime

from core.prod.sw_csd_ap import SwCsdAp
from core.rprt.rprt_xlsx import ReporterXlsx


if __name__ == '__main__':

    start_time = datetime.now()

    # Get script file and directory paths
    str_script_filepath = os.path.abspath(__file__)
    str_script_dirpath = os.path.dirname(str_script_filepath)

    # List of software versions to check
    str_json_filepath = str_script_dirpath + '/config.json'
    with open(str_json_filepath, 'r') as json_file:
        l_sw_ver_dir_names = json.load(json_file)

    # Create dictionary for instruction set
    str_json_filepath = str_script_dirpath + '/core/prod/d_proc.json'
    with open(str_json_filepath, 'r') as json_file:
        d_hw_proc = json.load(json_file)

    # For each software version, check constraints and report
    for str_sw_ver_dir_name in l_sw_ver_dir_names:

        # Directory path for software version
        str_sw_dir_path = str_script_dirpath + '/cfg/' + str_sw_ver_dir_name

        # JSON file for constraints and associated verifications
        str_json_filepath = str_sw_dir_path + '/d_sw_const.json'
        with open(str_json_filepath, 'r') as json_file:
            d_sw_const = json.load(json_file)

        # JSON file for file localisation
        str_json_filepath = str_sw_dir_path + '/d_sw_files.json'
        with open(str_json_filepath, 'r') as json_file:
            d_sw_files = json.load(json_file)

        print('\n------------------------------------------------------------------------------------------')
        print(f'Checking constraints for software version: {str_sw_ver_dir_name}')
        print('------------------------------------------------------------------------------------------')
        sw_csd_ap = SwCsdAp(d_sw_const, d_hw_proc, str_sw_dir_path, d_sw_files)
        d_sw_constr_result = sw_csd_ap.check_const()

        # Report
        print('\n------------------------------------------------------------------------------------------')
        print('Creating report')
        print('------------------------------------------------------------------------------------------')
        reporter_xslx = ReporterXlsx(str_script_dirpath, str_sw_ver_dir_name)
        reporter_xslx.report_constr(d_sw_const, d_sw_constr_result)

    # Print elapsed time
    time_elapsed = datetime.now() - start_time
    print(f'\nTime elapsed (hh:mm:ss.ms): {time_elapsed}\n')
