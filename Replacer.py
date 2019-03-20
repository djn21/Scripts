'''
Created on Mar 20, 2019

@author: Dejan
'''

############################################################################
########################### ENVIRONMENT VARIABLES ##########################
############################################################################

SUPP_EXT = ['.ini']

############################################################################
############################################################################
############################################################################

import os, fileinput, argparse

def find_files(replace, replace_with):
    search_dir = raw_input('Enter directory path (example: D:\\Projects\\<project_name>):')
    if not os.path.isdir(search_dir):
        raise IOError("path \'" + search_dir + "\' does not exist")
    print 'Replacing...'
    for dir_name, dir_names, file_names in os.walk(search_dir):
        for file_name in file_names:
            path = os.path.join(dir_name, file_name)
            for i in range(2, 10):
                if path[-i:] in SUPP_EXT:
                    find_lines(path, replace, replace_with)
    print 'Done.'


def find_lines(path, replace, replace_with):
	print path
	file = fileinput.FileInput(path, inplace=True)
	for line in file:
		if replace in line:
			print line.replace(replace, replace_with),
		else:
			print line,
	file.close()


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('replace', help='Text to replace')
	parser.add_argument('replace_with', help='Replacement text')
	args = parser.parse_args()
	find_files(args.replace, args.replace_with)