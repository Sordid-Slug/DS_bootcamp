#!/usr/bin/python3

import os

if __name__ == '__main__':
    venv_path = os.environ.get('VIRTUAL_ENV')
    if venv_path:
        print(venv_path)
    else:
        print('No venv')