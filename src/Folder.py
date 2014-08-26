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
    def __init__(self, dropbox, path, local_prefix):
        print_status(path)

        self.local_path = local_prefix + path + "/"

        self.path = path
        self._meta = dropbox.getMeta(path)

        self.children = []

        # Iterate over the contents array given by the Dropbox API
        # For each Element create a Folder (or File) Object
        # @TODO Make this nicer (Factory pattern maybe?)
        for item in self._meta["contents"]:
            # @TODO rename these variables to _path and _rev, making clear that they are just temporary. Maybe clear them after everything is done?
            new_path = item["path"]
            online_rev = item["revision"]

            if item["is_dir"]:
                self.children.append(Folder(dropbox, new_path, local_prefix))
            else:
                self.children.append(File(dropbox, new_path, local_prefix, online_rev))

    #
    # (private) Get the (local) metadata from the .dropper_data.json file
    #
    # @TODO Change the name to something, that makes clear that this is the local metadata
    def __get_meta(self):

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
        # @TODO Convert to the `with open` Syntax
        json_data = open(file)
        meta = json.load(json_data)
        json_data.close()

        return meta

    #
    # (private) Create a the file on the local disk
    #
    # @TODO rename this to __create_local, cause it is private
    #       (is this really the only way to mark stuff as private?)
    def create_local(self):
        path = self.local_path.lower().encode("ascii","ignore")

        print("{0} \n \t creating locally".format(path))
        if not os.path.exists(path):
            os.makedirs(path)

        # this gets called here, because right here is the first moment, where we can be shure, that the folder exists
        self.meta = self.__get_meta()

    #
    # (private) This was a expriment where i tried checking the revision number
    #           Of the folder rather than each file individually.
    #           It turns out, that the revision number does not always increase, if
    #           There are new revs of Files inside this folder
    # currently not used
    #
    # @TODO double check if there is a way to check folders rather than individual files. This would increase setup time drastically
    def __has_changes(self,folder,online_rev):
        try:
            # checks if the revision-numbers differ
            if self.meta[folder] != online_rev:
                return True
            else:
                return False
        except KeyError:
            # the KeyError gets thrown, if a Key in the .dropper_data.json does not exist
            # that happens, if the file is new on the server, so it has to be downloaded as well
            return True

    #
    # (public) Download the contents of this folder (if there are newer Versions on Dropbox)
    #
    def download(self, __meta):
        self.create_local()

        for item in self.children:
            item.download(self.meta)
