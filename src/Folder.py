from src import *
import os
import json


__author__ = 'thephpjo'


class Folder:
    def __init__(self, dropbox, path, local_prefix):
        print_status(path)

        self.local_path = local_prefix + path + "/"

        self.path = path
        self._meta = dropbox.getMeta(path)
        # print(self._meta)

        self.children = []
        for item in self._meta["contents"]:
            new_path = item["path"]
            online_rev = item["revision"]
            if item["is_dir"]:
                # if self.has_changes(new_path,online_rev):
                #     self.children.append(Folder(dropbox, new_path, local_prefix))
                #     self.meta[new_path] = online_rev;
                #     path = self.local_path + ".dropper_data.json";
                #     path = path.lower().encode("ascii","ignore")
                #     with open(path,"w") as out:
                #         json.dump(self.meta,out);
                self.children.append(Folder(dropbox, new_path, local_prefix))

            else:
                self.children.append(File(dropbox, new_path, local_prefix, online_rev))

    def __get_meta(self):
        path = self.local_path.lower();
        file = path + "/.dropper_data.json"
        file = file.encode("ascii","ignore")

        if not os.path.exists(file):
            with open(file, "w") as out:
                out.write("{}")

        json_data = open(file)
        meta = json.load(json_data)
        json_data.close()

        return meta

    def create_local(self):
        path = self.local_path.lower().encode("ascii","ignore")

        print("{0} \n \t creating locally".format(path))
        if not os.path.exists(path):
            os.makedirs(path)

        # this gets called here, because right here is the first moment, where we can be shure, that the folder exists
        self.meta = self.__get_meta()

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

    def download(self, __meta):
        self.create_local()

        for item in self.children:
            item.download(self.meta)
