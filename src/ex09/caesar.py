#!/usr/bin/python3

import sys


def correctness_input() -> None:
    if len(sys.argv) != 4 or sys.argv[1] not in ['encode', 'decode']:
        print("Usage: caesar.py encode|decode <string> <shift>")
        sys.exit()
    elif not sys.argv[3].isdigit():
        raise Exception("Incorrect shift")
    elif not sys.argv[2].isascii():
        raise ValueError("This script doesn't support your language")

def caesar_cipher() -> list:
    string = sys.argv[2]
    mode = sys.argv[1]
    shift = int(sys.argv[3])

    shift = shift if mode == 'encode' else -shift

    result_string = []
    for letter in string:
        if not letter.isalpha():
            result_string.append(letter)
            continue
        start_letter = 'a' if letter.islower() else 'A'
        letter = (ord(letter) - ord(start_letter) + shift) % 26
        result_string.append(chr(letter + ord(start_letter)))
    
    return ''.join(result_string)


if __name__ == '__main__':
    correctness_input()
    print(caesar_cipher())