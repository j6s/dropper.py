from src import *
import os
import json

__author__ = 'thephpjo'


#
# Folder Object: Represents a Folder _in the Dropbox_
#
class Folder:

    #
    # The constructor expects the following arguments:
    # - dropbox: A instance of DropboxWrapper
    # - path: The remote path _in Dropbox_
    # - local_prefix: The Folder, that is mapped to the root folder
    #
    def __init__(self, dropbox, path, local_prefix, settings):
        self.settings = settings
        print_status("indexing",path)

        self.local_path = local_prefix + path + "/"

        self.path = path
        self.remote_meta = dropbox.getMeta(path)
        self.__create_local_dir()
        self.local_meta = self.__get_local_meta()

        self.children = []

        # Iterate over the contents array given by the Dropbox API
        # For each Element create a Folder (or File) Object

        if self.__has_remote_changes():
            for item in self.remote_meta["contents"]:
                _path = item["path"]
                _rev = item["revision"]

                if item["is_dir"]:
                    self.children.append(Folder(dropbox, _path, local_prefix, settings))
                else:
                    self.children.append(File(dropbox, _path, local_prefix, _rev, settings))

        print_status("--- DONE INDEXING ---")

    def __get_local_meta(self):
        """
            Gets the local metadata from the .dropper_data.json file in his directory and returns it
        """

        # Again, much encoding stuff. I wish i could get rid of this ****
        path = self.local_path.lower();
        file = path + "/.dropper_data.json"
        file = file.encode("ascii","ignore")

        # If the configuration file does not exist, create it
        # This is done because the file is read just below
        # But more importantly: File Objects in this Folder expect
        # this File to exist
        if not os.path.exists(file):
            with open(file, "w") as out:
                out.write("{}")

        # Get the new configuration
        with open(file) as f:
            meta = json.load(f)

        return meta

    def __create_local_dir(self):
        """
            Creates the directory locally.
        """
        path = self.local_path.lower().encode("ascii","ignore")

        if not os.path.exists(path):
            print_status("mkdir",path)
            os.makedirs(path)

    def __has_remote_changes(self):
        if self.settings["force"]:
            return True

        """
        returns True if the saved hash is different from the online hash,
        return False, if not
        """
        try:
            if not self.local_meta['.'] == self.remote_meta["hash"]:
                return True
            else:
                return False
        except KeyError:
            return True

    def __save_local_meta_with_new_hash(self):
        """
            saves reloads the metadata from .dropper_data.json, adds the current's directory hash and
            saves it again
        """
        path = self.local_path.lower()
        file = path + "/.dropper_data.json"
        file = file.encode("ascii","ignore")


        self.local_meta = self.__get_local_meta()
        self.local_meta["."] = self.remote_meta["hash"]

        with open(file,"w") as f:
            json.dump(self.local_meta,f)

    def download(self, __meta):
        """
            Downloads the directory, if it has changes
        """
        if self.__has_remote_changes():
            for item in self.children:
                item.download(self.local_meta)
        else:
            print_status("no changes",self.path)

        self.__save_local_meta_with_new_hash()

