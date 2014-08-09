__author__ = 'thephpjo'
import dropbox
import webbrowser
import json
import os
import logging
import ntpath


remote_path = "/"
local_path = "./dropbox_data/"


# this is a quickfix for handling german umlauts
def enc_path(path):
    path = path.replace("ä","ae")
    path = path.replace("Ä","Ae")
    path = path.replace("ö","oe")
    path = path.replace("Ö","Oe")
    path = path.replace("ü","ue")
    path = path.replace("Ü","Ue")
    return path


# ################################################

class Dropbox:
    def __init__(self, access_token):
        self.dropbox = dropbox.client.DropboxClient(access_token)

    def getMeta(self, path):
        return self.dropbox.metadata(path)

    def download(self, path, local_path):
        f, metadata = self.dropbox.get_file_and_metadata(path)

        with open(local_path, "wb") as out:
            out.write(f.read())
        return metadata


class Folder:
    def __init__(self, dropbox, path, local_prefix):
        print(path)
        self.local_path = local_prefix + path + "/"
        self.local_path = self.local_path.lower();
        self.local_path = enc_path(self.local_path)

        self.path = path
        self._meta = dropbox.getMeta(path)
        # print(self._meta)

        self.create_local()
        self.meta = self.get_meta()

        self.children = []
        for item in self._meta["contents"]:
            new_path = item["path"]
            online_rev = item["revision"]
            if item["is_dir"]:
                if self.has_changes(new_path,online_rev):
                    self.children.append(Folder(dropbox, new_path, local_prefix))
                    self.meta[new_path] = online_rev;
                    with open(self.local_path + ".dropper_data.json","w") as out:
                        json.dump(self.meta,out);
            else:
                self.children.append(File(dropbox, new_path, local_prefix, self.meta, online_rev))

    def get_meta(self):
        if not os.path.exists(self.local_path + ".dropper_data.json"):
            with open(self.local_path + ".dropper_data.json", "w") as out:
                out.write("{}")

        json_data = open(self.local_path + ".dropper_data.json")
        meta = json.load(json_data)
        json_data.close()
        # print(meta)
        return meta


    def create_local(self):
        if not os.path.exists(self.local_path):
            os.makedirs(self.local_path)

    def has_changes(self,folder,online_rev):
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


class File:
    def __init__(self, dropbox, path, local_prefix, meta, online_rev):

        self.folder_meta = meta
        self.filename = ntpath.basename(path)
        self.dropbox = dropbox
        print(path)
        self.local_path = local_prefix + path;
        self.local_path = self.local_path.lower()
        self.local_path = enc_path(self.local_path)

        self.path = path;
        # self._meta = dropbox.getMeta(path);
        self.revision = online_rev

        self.download_if_needed();

    def needs_download(self):
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

    def download_if_needed(self):
        if self.needs_download():
            print("needs download")
            new_meta = self.dropbox.download(self.path, self.local_path);
            self.write_meta(new_meta)
        else:
            print("no need for downloading")

    def write_meta(self, new_meta):
        tmp = {}
        p = ntpath.dirname(self.local_path) + "/.dropper_data.json"

        with open(p, "r") as out:
            tmp = json.load(out)

        tmp[self.filename] = new_meta["revision"]

        with open(p, "w") as out:
            json.dump(tmp, out)


######################################################


def do_authorization():
    flow = dropbox.client.DropboxOAuth2FlowNoRedirect(config["app_key"], config["app_secret"])
    authorize_url = flow.start()
    webbrowser.open_new(authorize_url)
    print(authorize_url)

    code = input("auth code: ")
    config["access_token"], config["user_id"] = flow.finish(code)

    with open(".dropper.json", "w") as out:
        json.dump(config, out)


def authorize():
    load_configuration()
    logging.info(config);
    if not config["access_token"] or not config["user_id"]:
        do_authorization();


def load_configuration():
    global config

    json_data = open(".dropper.json")
    config = json.load(json_data)
    json_data.close()


####################################################

authorize()
drop = Dropbox(config["access_token"])

root_folder = Folder(drop, remote_path, local_path);