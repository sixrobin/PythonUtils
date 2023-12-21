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


def scan():
    scan_src = os.getcwd()
    folders = get_folders(scan_src)
    print(f'Scanning {scan_src}...')

    invalid_caps = []

    for folder in folders:
        os.chdir(folder)
        for file in os.listdir():
            if file.endswith('.meta'):
                continue

            file_name = file.split('.')[0]

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

    print(colored(f'\n{'Invalid capitals'} ({len(invalid_caps)} found):'))
    for invalid_file in invalid_caps:
        print('- ' + invalid_file)


if __name__ == "__main__":
    enable_terminal_coloring()

    try:
        scan()
    except Exception as e:
        print(e)

    input()
