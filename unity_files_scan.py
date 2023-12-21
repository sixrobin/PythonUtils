import os
from termcolor import colored


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
            if not file.endswith('.meta'):
                print(file)


if __name__ == "__main__":
    os.system('color')  # Enable terminal coloring.

    try:
        scan()
    except Exception as e:
        print(e)

    input()
