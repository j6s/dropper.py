__author__ = 'thephpjo'

import dropbox
import webbrowser
import json
import logging

from src import *


#
# Dropper Class:
#   This shall be the "front facing" side of the logic:
#   Everything is tied together here
#
# If dropper is used anywhere, it should be used as a Object of the Class Dropper
#
class Dropper:

    #
    # The constructor receives the folder names of the Local and the remote root / starting path
    #
    def __init__(self, remote, local, force=False):
        self.remote = remote
        self.local = local

        # The .dropper.json is the main config-file. The following is the minimal content:
        #
        # ```
        # {
        #     "app_key": "abcdefghijk",
        #     "app_secret": "123456789"
        # }
        # ```
        #
        # `app_key` and `app_secret` are received, by registering a Application in the Dropbox dev console:
        # https://www.dropbox.com/developers/apps
        #
        # @TODO Change this to the nicer looking `with open(path) as variable` Syntax
        with open(".dropper.json") as f:
            self.config = json.load(f)

        # Make shure the person is authorized by dropbox and initialize the DropboxWrapper Object
        self.authorize()
        self.dropbox = DropboxWrapper(self.config["access_token"])

        # Print a nice block of text telling the User what's happening right now
        print("Initializing Dropbox folders")
        print("\n\r\tThis will __NOT__ download anything")
        print("\r\tThe running time depends on the number of Elements in your Dropbox")
        print("\r\tyou can see the status below \n")

        # Initialized the root folder Object.
        # It in turn will initialize a Folder (or File) Object,
        # cascading all the way down
        settings = {
            "force": force
        }
        self.root = Folder(self.dropbox,remote,local,settings)

    #
    # Start the Dropbox user authorization proccess
    #
    # @TODO Move this to the DropboxWrapper
    # @TODO Catch the case if app_key or app_secret are not set
    def do_authorization(self):
        flow = dropbox.client.DropboxOAuth2FlowNoRedirect(  self.config["app_key"],
                                                            self.config["app_secret"])
        authorize_url = flow.start()

        # The user must visit the following URL to authorize the application.
        # It will open a browserwindow and navigate a URL and will output the
        # URL to the Command Line for Browserless or Remote Systems (such as a rpi)
        webbrowser.open_new(authorize_url)
        print(authorize_url)

        # The user has to paste the auth code, that the authorization proccess in the browser
        # outputted.
        # The resulting access_token and user_id are now stored in the config array
        # @TODO Explain what's happening to the user, not just bombard him with URLs and input prompts
        code = input("auth code: ")
        self.config["access_token"], self.config["user_id"] = flow.finish(code)

        # As a last step the Configuation array is persisted to the .dropper.json
        # @TODO Create a variable for the config file to have more control
        with open(".dropper.json", "w") as out:
            json.dump(self.config, out)

    #
    # If there is no access_token or user_id in the config array, start
    # the authorization proccess
    #
    # @TODO Check the validity of the access_token
    def authorize(self):
        logging.info(self.config)

        try:
            if not self.config["access_token"] or not self.config["user_id"]:
                self.do_authorization()
        except KeyError:
            self.do_authorization()

    #
    # (public) This downloads everything (only if needed)
    #
    # @TODO Make the rest of Functions here private
    def download_only(self):
        self.root.download([])
