import os
from termcolor import colored


def enable_terminal_coloring():
    os.system('color')


def get_folders(scan_src):
    folders = []
    for r, d, f in os.walk(scan_src):
        for folder in d:
            folders.append(os.path.join(r, folder))
    return folders


def scan():
    scan_src = os.getcwd()
    folders = get_folders(scan_src)
    print(f'Scanning {scan_src}...')

    for folder in folders:
        os.chdir(folder)
        for file in os.listdir():
            if file.endswith('.meta'):
                continue

            file_name = file.split('.')[0]
            print(file_name)


if __name__ == "__main__":
    enable_terminal_coloring()

    try:
        scan()
    except Exception as e:
        print(e)

    input()
