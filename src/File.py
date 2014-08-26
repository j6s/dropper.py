__author__ = 'thephpjo'

from src import *

import ntpath
import json


# The File Object represents a File _in Dropbox_
class File:

    #
    # The constructor expects a lot of arguments:
    # - dropbox: A Instance of DropboxWrapper
    # - path: The _remote_ path of the file
    # - local_prefix: The part of the path that is added to the path.
    #   If dropper is called with `dropper.py dlo / dropbox`
    #   the local prefix is "dropbox/"
    # - online_rev: The revision number from the Dropbox API
    #   This is used to determine, if the file shall be downloaded or not
    #
    def __init__(self, dropbox, path, local_prefix, online_rev):
        print_status(path)
        self.dropbox = dropbox

        # Detrmine the local path and the filename
        self.filename = ntpath.basename(path)
        self.local_path = local_prefix + path

        self.path = path
        self.revision = online_rev

    #
    # (private) Returns true, if the file in Dropbox is newer than the local
    #           Version or if the file was created
    def __needs_download(self):
        try:
            # checks if the revision-numbers differ
            if self.revision != self.folder_meta[self.filename]:
                return True
            else:
                return False
        except KeyError:
            # the KeyError gets thrown, if a Key in the .dropper_data.json does not exist
            # that happens, if the file is new on the server, so it has to be downloaded as well
            return True

    #
    # (private) Check if the file needs to be downloaded. If yes, download it
    #
    def __download_if_needed(self):
        if self.__needs_download():
            new_meta = self.dropbox.download(self.path, self.local_path);
            self.__write_meta(new_meta)

    #
    # (private) Write new metadata to the .dropper.json of that path
    #           This is used every time a File was downloaded and the revision number increases
    #           By one
    #
    def __write_meta(self, new_meta):
        tmp = {}
        p = ntpath.dirname(self.local_path) + "/.dropper_data.json"
        p = p.lower().encode("ascii","ignore")

        with open(p, "r") as out:
            tmp = json.load(out)

        tmp[self.filename] = new_meta["revision"]

        with open(p, "w") as out:
            json.dump(tmp, out)

    #
    # (public) Download a file (if needed) - Maps 1:1 to __download_if_needed
    #
    def download(self, meta):
        self.folder_meta = meta
        self.__download_if_needed()