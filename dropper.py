#!/usr/bin/env python3

__author__ = 'thephpjo'
__version__ = "0.1.0"

from src.Dropper import Dropper
import sys
import itertools
import argparse


#
#
# Welcome to dropper.py
# A simple Dropbox downloader script by Johannes Hertenstein ~thephpjo
#
# At the moment functionality still is limited, but there will be more.
#
# As this is my first contact with Python, things could be a little messy.
# I tried to make up for this by writing some comments.
# It would be highly appreciated if you could take some minutes out of your day
# and provide some Feedback on the coding style, so i can improve my Python knowledge
#
#


#
# dropper.py
#   This is only the command line interface of Dropper it only parses the input
#   and redirects it to the Dropper Object found in `src/Dropper.py`
#

############### HELPER FUNCTIONS ##################
# @TODO Move these helpers to their own file to simplify this file. Here shall only be cmd interface stuff

#
# Read and print the contents of the USAGE file
# This is done, if the user gives us invalid information
#
def print_usage():
    print("\n Dropper.py {0} \n".format(__version__))
    with open("USAGE.md") as out:
        print(out.read())
    print("\n\n")

#
# If there is something wrong, output the Message as well as
# The contents of the USAGE file
#
def error(msg):
    print("\nError: {0}".format(msg))
    print_usage()

#####################################################

#
# Basic usage of dropper is like the following:
#   $ python3 dropper.py [ACTION] [ARGUMENT(s)]
#
# The first element of sys_argv is "dropper.py" itself
#

try:
    # the first argument is the action
    action = sys.argv[1]

    # every argument after the action is a argument for the Dropper Object
    # The count of them depends on the function
    #args = []
    #for arg in itertools.islice(sys.argv,2,len(sys.argv)):
    #    args.append(arg)
    #print(args);

    argparser = argparse.ArgumentParser()
    argparser.add_argument('strings',metavar="N",type=str,nargs="+")
    argparser.add_argument("--force",dest="force",action="store_const",const=True,default=False)

    args = argparser.parse_args()

    print(args)


    # switch depending on the action
    # At the moment there is only 1 Action: download_only / dlo
    if  "download_only" in args.strings[0] or "dlo" in args.strings[0]:
        # download_only requires 2 Arguments to be present:
        # a remote_path and local_path
        if len(args.strings) < 2:
            error("download_only needs 2 arguments, {0} given".format(len(args.strings)-1))

        else:
            drop = Dropper(args.strings[1],args.strings[2],args.force)
            drop.download_only()

    else:
        # Show a errormessage if input is bollox
        error("Action {0} not found".format(action))
except IndexError:
    error("Action or Argument missing")
