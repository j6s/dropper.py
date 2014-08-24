__author__ = 'thephpjo'

import curses
import os
import atexit

global COLS
__rows, COLS = os.popen('stty size', 'r').read().split()

def print_status(text):
    print("{0:<{1}}\r".format(text,COLS)),


from src.File import File
from src.DropboxWrapper import DropboxWrapper
from src.Folder import Folder