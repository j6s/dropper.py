__author__ = 'thephpjo'

from src.Dropper import Dropper


remote_path = "/01_EISBAEREN/"
local_path = "./dropbox_data/01_EISBAEREN/"



drop = Dropper(remote_path,local_path)
drop.download_only()