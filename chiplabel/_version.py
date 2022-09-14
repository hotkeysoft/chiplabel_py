#!/usr/bin/env python3
# _version.py
__version__ = '1.1.0'
__app__ = 'chip_label'
__author__ = 'Dominic Thibodeau'
__author_email__ = 'dev@hotkeysoft.net'
__description__ = 'Chip Label Generator'
__url__ = 'https://github.com/hotkeysoft/chiplabel_py'
__year__ = 2022

def print_version_info():
    v = f'{__app__} {__description__} version {__version__}'
    print(v)
    print('-'*len(v))
    print(f'{__year__} {__author__} {__author_email__}')
    print(__url__)
    