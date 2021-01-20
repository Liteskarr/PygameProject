"""
Данный инструмент предназначен для быстрого подсчета строк в проекте.
"""

import os


SRC_PATH = '../src'


def is_full_string(string: str) -> bool:
    return not string.startswith('from') and not string.startswith('import') and string.rstrip()


def count_strings_in_file(filepath: str) -> int:
    result = 0
    with open(filepath, 'r', encoding='utf-8') as file:
        for string in file.readlines():
            if is_full_string(string):
                result += 1
    return result


def recursive_traversal(folder_path: str) -> int:
    result = 0
    for name in os.listdir(folder_path):
        if os.path.isfile(f'{folder_path}/{name}'):
            if name.endswith('.py'):
                result += count_strings_in_file(f'{folder_path}/{name}')
        else:
            result += recursive_traversal(f'{folder_path}/{name}')
    return result


def main():
    print(recursive_traversal(SRC_PATH))


if __name__ == '__main__':
    main()
