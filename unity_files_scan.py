import os
from termcolor import colored


def scan():
    print(colored('Scanning...', 'green'))


if __name__ == "__main__":
    os.system('color')  # Enable terminal coloring.

    try:
        scan()
    except Exception as e:
        print(e)

    input()
