import os
from termcolor import colored


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


def print_invalid_files(text, files_list):
    if len(files_list) == 0:
        return

    print('\n------------------------------------------------------------')
    print(colored(f'\n{text} ({len(files_list)} found):', 'white', attrs=['bold']))
    for invalid_file in files_list:
        print('- ' + invalid_file)


def scan():
    required_prefix = ask_user_prefix()
    print('')

    scan_src = os.getcwd()
    folders = get_folders(scan_src)
    print(f'Scanning {scan_src}...')

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
                missing_prefix.append(colored(required_prefix, 'red') + file_name)

            # Capitals check.
            words = file_name.split('_')
            for word in words:
                if not word:  # Asset name first character is an underscore.
                    continue
                if word[0].islower() and word[0].isalpha():
                    colored_file_name = ''
                    for i in range(len(words)):
                        w = words[i]
                        w = w if not w[0].islower() else colored(w[0], 'red') + w[1:]
                        colored_file_name += w + ('_' if i < len(words) - 1 else '')
                    invalid_caps.append(colored_file_name)
                    break

    print_invalid_files(f'Missing \"{required_prefix}\" prefix', missing_prefix)
    print_invalid_files('Invalid capitals', invalid_caps)


if __name__ == "__main__":
    enable_terminal_coloring()

    try:
        scan()
    except Exception as e:
        print(e)

    input()
