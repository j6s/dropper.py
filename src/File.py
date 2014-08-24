__author__ = 'thephpjo'

from src import *

import ntpath
import json


class File:
    def __init__(self, dropbox, path, local_prefix, online_rev):
        print_status(path)

        self.filename = ntpath.basename(path)
        self.dropbox = dropbox

        # printer(1,0,path)
        self.local_path = local_prefix + path

        self.path = path
        # self._meta = dropbox.getMeta(path);
        self.revision = online_rev


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

    def __download_if_needed(self):
        if self.__needs_download():
            new_meta = self.dropbox.download(self.path, self.local_path);
            self.__write_meta(new_meta)
        # else:
        #     print(2,0,"no need for downloading")

    def __write_meta(self, new_meta):
        tmp = {}
        p = ntpath.dirname(self.local_path) + "/.dropper_data.json"
        p = p.lower().encode("ascii","ignore")

        with open(p, "r") as out:
            tmp = json.load(out)

        tmp[self.filename] = new_meta["revision"]

        with open(p, "w") as out:
            json.dump(tmp, out)

    def download(self, meta):
        self.folder_meta = meta
        self.__download_if_needed()