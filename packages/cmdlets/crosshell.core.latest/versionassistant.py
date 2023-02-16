inputs = (' '.join(argv)).strip(" ")

import os
from assets.lib.configlib import useYaml

raw_data = dict()
version_file = f"{csbasedir}{os.sep}assets{os.sep}version.yaml"
version = "1.0"

# Get raw data
if os.path.exists(version_file):
    raw_data = useYaml(mode="get", yamlFile=version_file)
else: raw_data = {}


# Load gui
if "-g" in inputs or "gui" in inputs:
    # [Imports]
    from assets.lib.drawlib.internal import drawlib_internal_printmemsprite
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
        draw_point("\033[34m", 0, 0)
        char = "█"
        for i in range(rows-1):
            print(char * columns)
        draw_point("\033[0m", 0, 0)
        print("\033[{};{}H{}".format(rows, 0, f"\033[33mCrosshell version assistant, Version: {version}\033[0m"), end="")
        print("\033[7;40H\033[104;97mVersion information for crosshell?")
        print("\033[8;40H\033[104;97m----------------------------------")
        name = raw_data['name'] + (25-len(raw_data['name']))*" "
        print(f"\033[9;40H\033[104;97mName:    {name}")
        _id = raw_data['id'] + (25-len(raw_data['id']))*" "
        print(f"\033[10;40H\033[104;97mId:      {_id}")
        vid = raw_data['vid'] + (25-len(raw_data['vid']))*" "
        print(f"\033[11;40H\033[104;97mVid:     {vid}")
        channel = raw_data['channel'] + (25-len(raw_data['channel']))*" "
        print(f"\033[12;40H\033[104;97mChannel: {channel}\033[0m")
    # [Collect stuff]
    columns, rows = os.get_terminal_size()
    # [Draw]
    draw_background()
    pause()
    # [Reset]
    fill_terminal(" ")
    print(f"\033[2;2H\033[32m \033[0m")
# Load info only
else:
    for key in raw_data:
        value = raw_data[key]
        print(f"{key}: {value}")
