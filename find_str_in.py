#!/usr/bin/python3

import getopt
import sys
import re
import os.path


def check_and_get_input(argv):

    '''
    Check the input and create dictinary
    :param argv: mandatory: expression , optinal: files underline color machine
    :return: Dictinary
    '''

    dict = {}
    try:
        opts, args = getopt.getopt(argv, "e:f:cmuh", ["regex=", "files=", "underline", "color", "machine"])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)

    if not argv:
        usage('Need at least two parameters: 1- ("-e", "--regex") and 2- One or more then ("-c", "--color") ("-u", "--underline) ("-m", "--machine")]')

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()

    for opt, arg in opts:
        if opt in ("-e", "--regex"):
            expression = arg
            dict['expression'] = expression
    if 'expression' not in locals():
        usage('Need parameter string to search: ("-e", "--regex")')

    for opt, arg in opts:
        if opt in ("-u", "--underline"):
            underline = ""
            dict['underline'] = underline
        elif opt in ("-c", "--color"):
            color = ""
            dict['color'] = color
        elif opt in ("-m", "--machine"):
            machine = ""
            dict['machine'] = machine
    if 'underline' not in locals() and 'color' not in locals() and 'machine' not in locals():
        usage('Need at least one of the parameters: ("-c", "--color") ("-u", "--underline) ("-m", "--machine")]')

    for opt, arg in opts:
        if opt in ("-f", "--files"):
            files = arg
    if 'files' not in locals():
        files = get_str()
    dict['files'] = files
    return dict


def usage(msg=""):
    '''
    Show usage in case of error print information and usage line
    :param msg:
    :return: N/A
    '''
    exit_program = 0
    print()
    if msg != "":
        print(f"{msg}")
    must = '-e <string> --regex <string>'
    nice = '-f [filesnames] --files [filesnames] [ -u --underline | -c --color | -m --machine ]'
    print(f"{sys.argv[0]} {must} {nice}\n")
    if msg == "":
        exit_program = 1
    sys.exit(exit_program)


def get_str():
    '''
    In case that command line doesn't include files it ask to get it from STDIN
    :return: File name
    '''

    input_file ='/tmp/STDIN'
    line_str = input("Enter string: ")
    with open(input_file, 'w') as in_file:
        in_file.write(line_str)
        in_file.write('\n')
        print()
    return input_file


def check_files_exist(files):
    '''
    Check that input files from command line are exist
    :param : Files list
    :return:N/A
    '''
    for file in files.split():
        if not os.path.isfile(file):
            print(f"\n***ERROR: File '{file}' not exist\n")
            exit(1)


def search_string_in_file_mode_machine(file, expression):
    '''
    Run function for output the mode 'machine'
    :param file:
    :param expression: Get files and mode
    :return: N/A
    '''

    with open(file, 'r') as in_file:
        line_number = 0
        for line in in_file:
            line_number += 1
            line = line.rstrip()
            if re.search(r'\b' + expression + r'\b', line):
                print(f"Line number: '{line_number}' Line string:'{line}'")


def search_string_in_file_mode_color(file, expression):
    '''
    Run function for output the mode 'color'
    :param file:
    :param expression: Get files and mode
    :return: N/A
    '''

    with open(file, 'r') as f:
        text = f.read()
    if expression in text:
        print(text.replace(expression, '\033[44;33m{}\033[m'.format(expression)))


def search_string_in_file_mode_underline(file, expression):
    '''
     Run function for output the mode 'undeline'
     :param file:
     :param expression: Get files and mode
     :return: N/A
     '''

    with open(file, 'r') as in_file:
        for line in in_file:
            line = line.rstrip()
            print(f"{line}")
            if re.search(r'\b' + expression + r'\b', line):
                p = line.index(expression)
                len_str = len(expression)
                spaces = ' ' * p
                cerssore = '^' * len_str
                print(f"{spaces}{cerssore}")


def run_search(dict, mode):
    '''
    Run function for searching according to modes
    :param dict: Get dictinary
    :param mode:
    :return: N/A
    '''
    files = dict['files']
    expression = dict['expression']
    for file in files.split():
        print(f"\nFILE:'{file}'")
        if mode == 'underline':
            search_string_in_file_mode_underline(file, expression)
        if mode == 'color':
            search_string_in_file_mode_color(file, expression)
        if mode == 'machine':
            search_string_in_file_mode_machine(file, expression)


def main():
    '''
    Run function according to modes
    :return: N/A
    '''

    dict = check_and_get_input(sys.argv[1:])
    files = dict['files']
    check_files_exist(files)
    if 'underline' in dict.keys():
        run_search(dict, 'underline')
    if 'machine' in dict.keys():
        run_search(dict, 'machine')
    if 'color' in dict.keys():
        run_search(dict, 'color')
    print('\n')


############################
# main
if __name__ == "__main__":
    main()
