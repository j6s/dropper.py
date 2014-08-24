__author__ = 'thephpjo'

import dropbox
import webbrowser
import json
import logging
import curses

from src import *

class Dropper:

    def __init__(self, remote, local):
        self.remote = remote
        self.local = local

        # Load configuration drop .dropper.json
        json_data = open(".dropper.json")
        self.config = json.load(json_data)
        json_data.close()

        # initialize the Dropbox API Wrapper
        self.authorize()
        self.dropbox = DropboxWrapper(self.config["access_token"])

        print("Initializing Dropbox folders")
        print("\n\r\tThis will __NOT__ download anything")
        print("\r\tThe running time depends on the number of Elements in your Dropbox")
        print("\r\tyou can see the status below \n")

        self.root = Folder(self.dropbox,remote,local)

    def do_authorization(self):
        flow = dropbox.client.DropboxOAuth2FlowNoRedirect(  self.config["app_key"],
                                                            self.config["app_secret"])
        authorize_url = flow.start()
        webbrowser.open_new(authorize_url)
        print(authorize_url)

        code = input("auth code: ")
        self.config["access_token"], self.config["user_id"] = flow.finish(code)

        with open(".dropper.json", "w") as out:
            json.dump(self.config, out)


    def authorize(self):
        logging.info(self.config)
        if not self.config["access_token"] or not self.config["user_id"]:
            self.do_authorization()

    def download_only(self):
        self.root.download([])