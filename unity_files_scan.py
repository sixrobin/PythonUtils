import os
from scan_utils import *
from termcolor import colored


IGNORED_EXTENSIONS = ['meta', 'asmdef', 'dll']
ALLOWED_CHARACTERS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-+'


def scan():
    required_prefix = input('Enter a prefix to check in asset names (leave blank not to check prefixes): ')
    print('')

    scan_src = os.getcwd()
    folders = get_folders(scan_src)
    print(f'Scanning {colored(scan_src, WHITE, attrs=[BOLD])}...')

    missing_prefix = []
    invalid_caps = []
    forbidden_chars = []

    # Recursive scan.
    for folder in folders:
        os.chdir(folder)
        for file in os.listdir():
            extension = file.split('.')[-1]
            if any([extension == ext for ext in IGNORED_EXTENSIONS]):
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

            # Forbidden characters.
            if not all([c in ALLOWED_CHARACTERS for c in file_name]):
                colored_file_name = ''
                for c in file_name:
                    attrs = [REVERSE] if c == ' ' else None
                    colored_file_name += c if c in ALLOWED_CHARACTERS else colored(c, RED, attrs=attrs)
                forbidden_chars.append(colored_file_name)

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
