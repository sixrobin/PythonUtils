import os
from termcolor import colored


WHITE, RED, GREEN, YELLOW, CYAN, BLUE = 'white', 'red', 'green', 'yellow', 'cyan', 'blue'
BOLD, UNDERLINE, REVERSE = 'bold', 'underline', 'reverse'
UNDERSCORE = '_'


def enable_terminal_coloring():
    os.system('color')


def get_folders(scan_src):
    folders = []
    for root, dirs, _ in os.walk(scan_src):
        for folder in dirs:
            folders.append(os.path.join(root, folder))

    return folders


def ask_user_prefix():
    return input('Enter a prefix to check in asset names (leave blank not to check prefixes): ')


def print_space_line():
    print('------------------------------------------------------------')


def print_invalid_files(text, files_list):
    if len(files_list) == 0:
        return 0

    print_space_line()
    print(colored(f'\n{text} ({len(files_list)} found):', WHITE, attrs=[BOLD]))
    for invalid_file in files_list:
        print('- ' + invalid_file)

    return len(files_list)


def scan():
    required_prefix = ask_user_prefix()
    print('')

    scan_src = os.getcwd()
    folders = get_folders(scan_src)
    print(f'Scanning {colored(scan_src, WHITE, attrs=[BOLD])}...')

    missing_prefix = []
    invalid_caps = []

    for folder in folders:
        os.chdir(folder)
        for file in os.listdir():
            if file.endswith('.meta'):
                continue

            file_name = file.split('.')[0]

            # Prefix check.
            if required_prefix and not file_name.startswith(required_prefix):
                missing_prefix.append(colored(required_prefix, RED) + file_name)

            # Capitals check.
            words = file_name.split(UNDERSCORE)
            for word in words:
                if not word:  # Asset name first character is an underscore.
                    continue
                if word[0].islower() and word[0].isalpha():
                    colored_file_name = ''
                    for i in range(len(words)):
                        w = words[i]
                        w = w if not w[0].islower() else colored(w[0], RED) + w[1:]
                        colored_file_name += w + (UNDERSCORE if i < len(words) - 1 else '')
                    invalid_caps.append(colored_file_name)
                    break

    errors_count = 0
    errors_count += print_invalid_files(f'Missing \"{required_prefix}\" prefix', missing_prefix)
    errors_count += print_invalid_files('Invalid capitals', invalid_caps)

    print('\n')
    print_space_line()
    print('\n')

    if errors_count == 0:
        print(colored('No error found!', GREEN))
    else:
        print(colored(f'{str(errors_count)} error(s) found!', RED))


if __name__ == "__main__":
    enable_terminal_coloring()

    try:
        scan()
    except Exception as e:
        print(e)

    input()
