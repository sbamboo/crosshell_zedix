inputs = (' '.join(argv)).strip(" ")

import os
from assets.lib.configlib import useYaml
from assets.lib.conUtils import *

raw_data = dict()
version_file = f"{csbasedir}{os.sep}assets{os.sep}version.yaml"
version = "1.0"
lpt_file = f"{csbasedir}{os.sep}packages{os.sep}cmdlets{os.sep}crosshell.legacyPassThru.latest{os.sep}dir.cfg"
if IsWindows() == True: platformName = "Windows"
elif IsLinux() == True: platformName = "Linux"
elif IsMacOS() == True: platformName = "MacOS"
else:           platformName = "Unknown"

# Get raw data
if os.path.exists(version_file):
    raw_data = useYaml(mode="get", yamlFile=version_file)
else: raw_data = {}


# Load gui
if "-g" in inputs or "gui" in inputs:
    # [Imports]
    from assets.lib.drawlib.legacy import drawlib_internal_printmemsprite
    from assets.lib.drawlib.linedraw import draw_point,fill_terminal
    from assets.lib.conUtils import *
    # [Functions]
    def inputAtCords (posX, posY, text=None, color=None):
        # Save cursorPos
        print("\033[s")
        # Set ansi prefix
        ANSIprefix = "\033[" + str(posY) + ";" + str(posX) + "H" + "\033[" + str(color) + "m"
        inp = input(str(ANSIprefix + str(text)))
        print("\033[0m")
        # Load cursorPos
        print("\033[u\033[2A")
        return inp
    def draw_background():
        global platformName
        draw_point("\033[34m", 0, 0)
        char = "█"
        for i in range(rows-1):
            print(char * columns)
        draw_point("\033[0m", 0, 0)
        print("\033[{};{}H{}".format(rows, 0, f"\033[33mCrosshell version assistant, Version: {version}\033[0m"), end="")
        print("\033[7;40H\033[104;97mVersion information for crosshell?")
        print("\033[8;40H\033[104;97m----------------------------------")
        name = raw_data['name'] + (24-len(raw_data['name']))*" "
        print(f"\033[9;40H\033[104;97mName:     {name}")
        _id = raw_data['id'] + (24-len(raw_data['id']))*" "
        print(f"\033[10;40H\033[104;97mId:       {_id}")
        vid = raw_data['vid'] + (24-len(raw_data['vid']))*" "
        print(f"\033[11;40H\033[104;97mVid:      {vid}")
        channel = raw_data['channel'] + (24-len(raw_data['channel']))*" "
        print(f"\033[12;40H\033[104;97mChannel:  {channel}\033[0m")
        platformName = platformName + (24-len(platformName))*" "
        print(f"\033[13;40H\033[104;97mPlatform: {platformName}\033[0m")
    def ScrapeVersionData(coreFile=str()):
        content = open(coreFile,'r',encoding="utf-8").read()
        tmp = content.split("crosshell_versionID")[1]
        tmp = tmp.split("\n")[0]
        tmp = tmp.replace(" ","")
        tmp = tmp.replace("=","")
        tmp = tmp.replace('"',"")
        versionID = tmp.replace("'","")
        tmp = content.split("crosshell_versionChannel")[1]
        tmp = tmp.split("\n")[0]
        tmp = tmp.replace(" ","")
        tmp = tmp.replace("=","")
        tmp = tmp.replace('"',"")
        versionChannel = tmp.replace("'","")
        return {"VersionID":versionID,"VersionChannel":versionChannel}


    # [Collect stuff]
    columns, rows = os.get_terminal_size()
    # [Draw]
    draw_background()
    # [LegacyPassThrough]
    if os.path.exists(lpt_file):
        lpt_path = "Nan"
        try:
            path = open(lpt_file,'r',encoding="utf-8").read()
            if os.path.exists(path):
                lpt_path = path
        except: pass
        lpt_path_t = lpt_path + (24-len(lpt_path))*" "
        s1 = "Legacy Passthrough:               "
        s2 = "----------------------------------"
        s1 = s1 + " "*(len(f"Path:    {lpt_path_t}") - len(s1))
        s2 = s2 + "-"*(len(f"Path:    {lpt_path_t}") - len(s2))
        print(f"\033[15;40H\033[104;97m{s1}")
        print(f"\033[16;40H\033[104;97m{s2}")
        print(f"\033[17;40H\033[104;97mPath:    {lpt_path_t}\033[0m")
        if os.path.exists(f"{lpt_path_t}{os.sep}core{os.sep}core.ps1"):
            verData = ScrapeVersionData(f"{lpt_path_t}{os.sep}core{os.sep}core.ps1")
            verId = str(verData["VersionID"]) + " "*(len(s1) - len(f'VerID:   {verData["VersionID"]}'))
            verCh = str(verData["VersionChannel"]) + " "*(len(s1) - len(f'Channel: {verData["VersionChannel"]}'))
            print(f"\033[18;40H\033[104;97mVerID:   {verId}\033[0m")
            print(f"\033[19;40H\033[104;97mChannel: {verCh}\033[0m")
    pause()
    # [Reset]
    fill_terminal(" ")
    print(f"\033[2;2H\033[32m \033[0m")
# Load info only
else:
    for key in raw_data:
        value = raw_data[key]
        print(f"{key}: {value}")
    print(f"Platform: {platformName}")
