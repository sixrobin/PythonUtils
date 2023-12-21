import os
from termcolor import colored


WHITE, RED, GREEN, YELLOW, CYAN, BLUE = 'white', 'red', 'green', 'yellow', 'cyan', 'blue'
BOLD, UNDERLINE, REVERSE = 'bold', 'underline', 'reverse'
UNDERSCORE = '_'


def enable_terminal_coloring():
    os.system('color')


def get_folders(scan_src):
    folders = []
    for r, d, f in os.walk(scan_src):
        for folder in d:
            folders.append(os.path.join(r, folder))
    return folders


def print_space_line():
    print('------------------------------------------------------------')


def print_total_errors(errors_count):
    print('\n')
    print_space_line()
    print('\n')

    if errors_count == 0:
        print(colored('No error found!', GREEN))
    else:
        print(colored(f'{str(errors_count)} error(s) found!', RED))


def print_invalid_files(text, files_list):
    if len(files_list) == 0:
        return 0

    print('\n')
    print_space_line()

    print(colored(f'\n{text} ({len(files_list)} found):', WHITE, attrs=[BOLD]))
    for invalid_file in files_list:
        print('- ' + invalid_file)

    return len(files_list)
