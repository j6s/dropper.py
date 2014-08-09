dropper.py
==========

__work in progress right here. Highly undocumented, may break__

Simple dropbox downsyncing script, intended for RaspberryPi use.

# How to use (for now, will simplify setup)

1. Create a file `.dropper.json`

  1.1 Add app_key and app_secret. Your .dropper.json should look like this:
  ```
  {
    "app_key": "abcdefghijk",
    "app_secret": "123456789"
  }
  ````

2. If you don't want to sync your whole dropbox or you want to change the local folder to sync to, change the variable in dropper.py (sorry for hardcoded paths, will add them to .dropper.json)

3. Call dropper.py – it will ask you to open a URL in your Browser, to grant dropper.py access to your Dropbox.
  
  3.1 After granting access you will see a access token. Copy it into the prompt.
  
4. dropper.py is set up. The first sync will take a while.

Every call of dropper.py after you have it setup will check, if dropbox contains new versions of a file. If it does, it will download them. If not, no additional traffic is produced


# Limitations

For now, the Capitalization of paths is ignored, every path is converted to lowercase.

This is caused by a bug in the Dropbox API, where somtimes files have incorrect metadata


# Note

- This is the first thing i have ever done in Python. If there is some bad code, please let me know. I have no idea, what is considered best practise in the Python world.

- This was developed using Python3.4. It should work with 3.x. However there is no 2.x support
