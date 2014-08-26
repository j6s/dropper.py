__author__ = 'thephpjo'

import os

# Read the amount of columns of the Terminal
# This is used to pad the status status text
global COLS
__rows, COLS = os.popen('stty size', 'r').read().split()


#
# Status printing: These messages overwrite each other
# and do not stay in the log
#
def print_status(text):
    # encode the text in ascii, because python does not like encoding stuff
    # I am shure there is a nicer way to do this, but for now, this is OK
    text = text.encode("ascii", "ignore")

    # Output the text. There is a lot going on here:
    #
    # - The text is outputted `{0}` and padded to the left to the length of COLS `:<{1}`
    #   This is needed to prevent weird overlays, if The current String is shorter than the
    #   last one
    #
    # - The \r resets the cursor back to the beginning of the line. That way
    #   the next line will overwrite the current
    #
    # - The `,` at the end is quite important: It prevents print from adding a
    #   linebreak at the end. A linebreak at the end would negate \r:
    #   Without it the next print would not overwrite the current one
    print("{0:<{1}}\r".format(text,COLS)),


# Import every part of dropper here. This is done to simplify the import section
# in the individual files:
# Now you only have to do `from src import *` to have everything imported here
# Dropper.py is missing, cause that is the 'public API' - Every command starts there
# and there are no calls of Dropper-functions inside the rest
from src.File import File
from src.DropboxWrapper import DropboxWrapper
from src.Folder import Folder
