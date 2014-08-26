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

2. Call `python3 dropper.py` and read the USAGE information. Alternatively, read the `USAGE` file in the repository

# Limitations

For now, the Capitalization of paths is ignored, every path is converted to lowercase and ASCII.

This is caused by a bug in the Dropbox API, where somtimes files have incorrect metadata


# Note

- This is the first thing i have ever done in Python. If there is some bad code, please let me know. I have no idea, what is considered best practise in the Python world.

- This was developed using Python3.4. It should work with 3.x. However there is no 2.x support
