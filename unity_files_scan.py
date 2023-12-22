import os
from scan_utils import *
from termcolor import colored


IGNORED_EXTENSIONS = ['meta', 'asmdef', 'dll']
ALLOWED_CHARACTERS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-+'

missing_prefix = []
invalid_caps = []
forbidden_chars = []


def scan_prefix(n, p):
    if not n.startswith(p):
        missing_prefix.append(colored(p, RED) + n)


def scan_capitals(n):
    words = n.split(UNDERSCORE)
    for word in words:
        if not word:  # Asset name first character is an underscore.
            return
        if word[0].islower() and word[0].isalpha():
            result = ''
            for i in range(len(words)):
                w = words[i]
                w = w if not w[0].islower() else colored(w[0], RED) + w[1:]
                result += w + (UNDERSCORE if i < len(words) - 1 else '')
            invalid_caps.append(result)
            return


def scan_forbidden_chars(n):
    if not all([c in ALLOWED_CHARACTERS for c in n]):
        result = ''
        for c in n:
            attrs = [REVERSE] if c == ' ' else None
            result += c if c in ALLOWED_CHARACTERS else colored(c, RED, attrs=attrs)
        forbidden_chars.append(result)


def scan():
    required_prefix = input('Enter a prefix to check in asset names (leave blank not to check prefixes): ')
    print('')

    scan_src = os.getcwd()
    folders = get_folders(scan_src)
    print(f'Scanning {colored(scan_src, WHITE, attrs=[BOLD])}...')

    # Recursive scan.
    for folder in folders:
        os.chdir(folder)
        for file in os.listdir():
            extension = file.split('.')[-1]
            if any([extension == ext for ext in IGNORED_EXTENSIONS]):
                continue

            file_name = file.split('.')[0]

            if required_prefix:
                scan_prefix(file_name, required_prefix)

            scan_capitals(file_name)
            scan_forbidden_chars(file_name)

            # TODO: 2 digits numbers format.
            # TODO: constant numbering start (0 or 1, based on user input before scanning).
            # TODO: AOC_ prefix for .overrideController files.
            # TODO: Anim_ prefix for .anim files.
            # TODO: AnimCtrl_ prefix for .controller files.

    # Result printing.
    errors_count = 0
    errors_count += print_invalid_files(f'Missing \"{required_prefix}\" prefix', missing_prefix)
    errors_count += print_invalid_files('Invalid capitals', invalid_caps)
    errors_count += print_invalid_files('Forbidden characters', forbidden_chars)
    print_total_errors(errors_count)


if __name__ == "__main__":
    enable_terminal_coloring()

    try:
        scan()
    except Exception as e:
        print(e)

    input()
