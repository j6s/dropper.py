__author__ = 'thephpjo'

import dropbox
from src import *


#
# A simple Wrapper around the Dropbox API
# This is done to simplify everything
# and to have a single point to make changes
#
class DropboxWrapper:

    #
    # Everything is initialized with the access_token of the API
    #
    # @TODO Move authorization proccess here
    def __init__(self, access_token):
        # Initialize the "real" Dropbox Object
        self.dropbox = dropbox.client.DropboxClient(access_token)

    #
    # Returns a Metadata Object for the given Path
    # More information:

    # https://www.dropbox.com/developers/core/docs#metadata-details
    #
    def getMeta(self, path):
        return self.dropbox.metadata(path)

    #
    # Download the given remote path to the given local path
    #
    def download(self, path, local_path):
        # Print out the filename and the fact, that it is Downloading,
        # So the user knows what is happening
        print(path.encode("ascii","ignore"))
        print("\t Downloading")

        # The local path is converted to lowercase to prevent some errors
        # from happening.
        #
        # In some cases it can happen, that the Casing of the Dropbox metadata is not
        # consistent. The following could happen:
        #   SAMPLE/Folder
        #       creating Folder
        #   sample/Folder/image.jpg
        #       Downloading
        # This would break everything on a case sensitive file system, such as ext4
        # I have created a ticket for this bug but have not yet received an answer
        # @TODO Respect the casing of paths.
        local_path = local_path.lower()
        # Everything outside the ascii standard is ignored for now
        # Without, the script throws errors over errors when encountering specialchars
        # such as german umlauts.
        # This is far from optimal and is just a quick hack for now. Will fix in the future
        # @TODO Support Special Characters / Chars outside of ASCII
        local_path = local_path.encode("ascii","ignore")

        # get the file from the API and write it to the local_path
        f, metadata = self.dropbox.get_file_and_metadata(path)
        with open(local_path, "wb") as out:
            out.write(f.read())

        # Return the new metadata of the file
        return metadata
