# -*-coding:utf-8 -*
import sys
import re


def is_prep_dir_def(str_prep_dir, str_filepath):

    b_result = False

    re_prep_dir_def = '(#define\s+' + str_prep_dir + ')'

    with open(str_filepath, 'r', encoding="latin-1") as workFile:

        b_bloc_comm = False

        # For each line in source file
        for (idx_line, str_line) in enumerate(workFile):
            # If any occurence of // in line
            if '//' in str_line:
                # Match eveything before first occurence of //
                match = re.search('^(.*?)//', str_line)
                if match is not None:
                    str_line = match.group(1)

            # Delete any occurence of /* */ in line
            str_uncomm_slash_star = re.sub('(/\*.+\*/)', '', str_line)

            # If bloc comment not started and /* in line after /* */ deletion
            if not b_bloc_comm and '/*' in str_uncomm_slash_star:
                # Start of bloc comment in line
                b_bloc_comm = True

                # Match everything before /*
                match = re.search('^(.*?)/\*', str_line)
                if match is not None:
                    # Match #define before /*
                    match = re.search(re_prep_dir_def, match.group(1))
                    if match is not None:
                        b_result = True
                        break

            # If bloc comment already started and */ in line after /* */ deletion
            elif b_bloc_comm and '*/' in str_uncomm_slash_star:
                # End of bloc comment in line
                b_bloc_comm = False

                # # Match everything after */
                # match = re.search('\*/(.*?)$', str_line)
                # if match != None :
                #     # Match #define after */
                #     match = re.search(re_prep_dir_def,match.group(1))
                #     if match != None :
                #         b_result = True
                #         break
            else:
                # Just match #define
                match = re.search(re_prep_dir_def, str_uncomm_slash_star)
                if match is not None:
                    b_result = True
                    break

    return b_result
