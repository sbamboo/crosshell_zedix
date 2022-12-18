import os
import requests
import hashlib
cs_devmode_valid = False
if os.path.exists(os.path.realpath(f"{csbasedir}{os.sep}devmode.key")):
    if str(hashlib.sha256(open(os.path.realpath(f"{csbasedir}{os.sep}devmode.key"),"r").read().encode()).hexdigest()).strip() == str(requests.get("https://github.com/simonkalmiclaesson/crosshell_zedix/raw/main/assets/online_devmode.hkey").text.strip("\n")).strip():
        cs_devmode_valid = True