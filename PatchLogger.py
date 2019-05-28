'''
Created on Feb 27, 2019

@author: Dejan
'''

############################################################################
############################## PATCH EXAMPLE ###############################
############################################################################

'''/* <patch team="<team>" by="<eDDK>" approved="True" reason="<reason>">'''

'''/* </patch> */'''

############################################################################
############################################################################
############################################################################

############################################################################
########################### ENVIRONMENT VARIABLES ##########################
############################################################################

TAG = 'patch team="APP"'
APPROVED_TAG = 'approved="True"'

PATCHED_BY_REGEX = 'by="[^"]*"'
PATCH_REASON_REGEX = 'reason="[^"]*"'

SUPP_EXT = ['.c', '.h']

############################################################################
############################################################################
############################################################################

import os
import re
import time
import argparse
from datetime import datetime

ignore_approved = False
verbose = 1


def find_patches():
    search_dir = raw_input("Enter directory path to search (example: D:\\Projects\\<project_name>):")
    if not os.path.isdir(search_dir):
        raise IOError("path \'" + search_dir + "\' does not exist")
    print 'SEARCHING...\n'
    current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = open("PatchLog_" + current_time + ".txt", 'w')
    log_file.write("Patched files:\n\n")
    for dir_name, dir_names, file_names in os.walk(search_dir):
        for file_name in file_names:
            path = os.path.join(dir_name, file_name)
            for i in range(2, 10):
                if path[-i:] in SUPP_EXT:
                    find_patches_in_file(path, log_file)
    log_file.close()


def find_patches_in_file(path, log_file):
    file_name = open(path, 'r')
    line_no = 0
    patch_found = False
    for line in file_name:
        line_no += 1
        if TAG in line:
            if not(ignore_approved and APPROVED_TAG in line):
                if verbose == '0' and not patch_found:
                    print path
                    log_file.write(path + '\n')
                elif verbose == '1':
                    if not patch_found:
                        log_file.write('FILE: ' + path + '\n')
                        print path
                    log_file.write('LINE: ' + str(line_no) + '\n')
                elif verbose == '2':
                    patched_by = re.search(PATCHED_BY_REGEX, line).group(0)
                    patch_reason = re.search(PATCH_REASON_REGEX, line).group(0)
                    if not patch_found:
                        log_file.write('FILE: ' + path + '\n')
                        print path
                    out = 'LINE: {:7} BY: {:9}'.format(str(line_no), patched_by[4:-1])
                    if not ignore_approved and APPROVED_TAG in line:
                        out += 'APPROVED '
                    out += 'REASON: ' + patch_reason[8:-1]
                    log_file.write(out + '\n')
            patch_found = True
    if patch_found and not verbose == '0':
        log_file.write('\n')
        return
    file_name.close()


if __name__ == '__main__':
    start_time = time.time()
    parser = argparse.ArgumentParser()
    parser.add_argument('-ia', '--ignore_approved',
                        action='store_true',
                        help='Ignore approved patches')
    parser.add_argument('-v', '--verbose',
                        default='0',
                        choices=['0', '1', '2'],
                        help='Verbosity level: [0] - Print pathced file path only [1] - Print patched files and lines only [2] - All')
    args = parser.parse_args()
    ignore_approved = args.ignore_approved
    verbose = args.verbose
    find_patches()
    stop_time = time.time()
    print '\nDone.' + str(round(stop_time - start_time, 2)) + 's'
