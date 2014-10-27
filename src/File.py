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
    def __init__(self, dropbox, path, local_prefix, online_rev, settings):
        self.settings = settings
        print_status("indexing",path)
        self.dropbox = dropbox

        # Detrmine the local path and the filename
        self.filename = ntpath.basename(path)
        self.local_path = local_prefix + path

        self.path = path
        self.revision = online_rev

    def __has_remote_changes(self):
        if self.settings["force"]:
            return True

        """
            Checks, if the remote has changes, returns True if so, False if not
        """

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

    def __download_if_needed(self):
        """
            Downloads the file, if there is a newer Version online
        """
        if self.__has_remote_changes():
            print_status("downloading",self.path)
            new_meta = self.dropbox.download(self.path, self.local_path);
            self.__write_local_meta(new_meta)

    def __write_local_meta(self, new_meta):
        """
            Writes the new metadata from the dropbox API to the local .dropper_data.json file
            expects a dropbox metadata object with set revision attribute as new_meta
        """
        tmp = {}
        p = ntpath.dirname(self.local_path) + "/.dropper_data.json"
        p = p.lower().encode("ascii","ignore")

        with open(p, "r") as out:
            tmp = json.load(out)

        tmp[self.filename] = new_meta["revision"]

        with open(p, "w") as out:
            json.dump(tmp, out)

    def download(self, meta):
        """
            Download the file (if needed)
        """
        self.folder_meta = meta
        self.__download_if_needed()