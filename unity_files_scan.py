import os
import re
from scan_utils import *
from termcolor import colored


IGNORED_EXTENSIONS = ['meta', 'asmdef', 'dll']
ALLOWED_CHARACTERS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-+'

missing_prefix = []
invalid_caps = []
forbidden_chars = []
invalid_number_format = []


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


def scan_number_format(n, numbering_start):
    numbers_indices = dict((m.start(), m.group()) for m in re.finditer(r'\d+', n))
    result = n[0]
    for i in range(1, len(n)):
        c, prev_c = n[i], n[i - 1]
        if c.isalpha():
            if prev_c.isdigit():  # Missing underscore.
                result += colored(UNDERSCORE, RED)
            result += c
        elif c.isdigit():
            if prev_c.isalpha():  # Missing underscore.
                if prev_c == 'f':  # Animation frame format (_fXX).
                    if n[i - 2] != UNDERSCORE:
                        result += colored(UNDERSCORE, RED)
                else:
                    result += colored(UNDERSCORE, RED)
            if i in numbers_indices:
                if len(numbers_indices[i]) == 1:  # Invalid 2 digits format number.
                    result += colored(c, RED)
                elif numbering_start:
                    nb = int(numbers_indices[i])
                    if nb == 0 and numbering_start == '1':
                        result += colored(c, RED)  # TODO: Should color the last digit.
                    # TODO: If nb==1 and numbering_start==0, check if file with number 0 exists.
                    else:
                        result += c
                else:
                    result += c
            else:
                result += c
        else:
            result += c

    if n != result:
        invalid_number_format.append(f'{result} {colored(f'/ source file name: {n}', CYAN)}')


def scan():
    required_prefix = input('Enter a prefix to check in asset names (leave blank not to check prefixes): ')
    numbering_start = input('Enter numbering first value (0 or 1): ')
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
            scan_number_format(file_name, numbering_start)

            # TODO: AOC_ prefix for .overrideController files.
            # TODO: Anim_ prefix for .anim files.
            # TODO: AnimCtrl_ prefix for .controller files.

    # Result printing.
    errors_count = 0
    errors_count += print_invalid_files(f'Missing \"{required_prefix}\" prefix', missing_prefix)
    errors_count += print_invalid_files('Invalid capitals', invalid_caps)
    errors_count += print_invalid_files('Forbidden characters', forbidden_chars)
    errors_count += print_invalid_files('Invalid number format', invalid_number_format)
    print_total_errors(errors_count)


if __name__ == "__main__":
    enable_terminal_coloring()

    try:
        scan()
    except Exception as e:
        print(e)

    input()
