__author__ = 'thephpjo'

from src.Dropper import Dropper
import sys
import itertools
import os

# Helperfunction to output the usage information
def print_usage():
    print("\n\n")
    with open("USAGE") as out:
        print(out.read())
    print("\n\n")


# Helperfunction for errors
def error(msg):
    print("\nError: {0}".format(msg))
    print_usage()

# get the arguments: The first one is the action
try:
    action = sys.argv[1]
    args = []
    for arg in itertools.islice(sys.argv,2,len(sys.argv)):
        args.append(arg)



    # switch depending on the usage
    if  "download_only" in action or "dlo" in action:
        if len(args) < 2:
            error("download_only needs 2 arguments, {0} given".format(len(args)))
        else:
            drop = Dropper(args[0],args[1])
            drop.download_only()
    else:
        error("Action {0} not found".format(action))
except IndexError:
    error("Action or Argument missing")