__author__ = 'thephpjo'

import dropbox
from src import *

class DropboxWrapper:
    def __init__(self, access_token):
        self.dropbox = dropbox.client.DropboxClient(access_token)

    def getMeta(self, path):
        return self.dropbox.metadata(path)

    def download(self, path, local_path):
        print(path)
        print("\t Downloading")

        local_path = local_path.lower();
        local_path = local_path.encode("ascii","ignore")

        f, metadata = self.dropbox.get_file_and_metadata(path)

        with open(local_path, "wb") as out:
            out.write(f.read())
        return metadata