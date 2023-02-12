# Crosshell verification tool (service)
# Author: Simon Kalmi Claeson
version = 1.0
#


# [Imports]
import os
import socket
import json
from assets.lib.drawlib.internal import drawlib_internal_printmemsprite
from assets.lib.drawlib.linedraw import draw_point,fill_terminal
from assets.lib.conUtils import *
from assets.lib.pantryapi import pantryapireq
from assets.lib.crypto import *
from assets.lib.netwa import netwa

# [Prepare]
KRYPTOKEY = GenerateKey("CROSSHELL VERIFIER TOOLKIT jja18aj1a SIGNED IT BIT")
PANTRYKEY = 'c96b7120-d350-4ac1-af69-1bee5f3554d3'
has_verified_file = f"{os.path.dirname(__file__)}{os.sep}assets{os.sep}hasverified.state"
HelpText = [
            "This information is collected to allow the author -",
            " to have a list of people using the app,",
            "this is only needed since the app is in development -",
            " and will be removed later.",
            "To opt out simply don't write your name and press enter.",
            "Although it is appriciated if you opt in.",
            "Note! Only name and computer-name is send,",
            "and no other data will ever be collected,",
            "as a part of this tool.",
            "Note! If other data at some point is collected -",
            " it's sepparate, and will be informed about!",
            "THIRD PARTY COLLECTION IS NOT HANDLED BY THIS -",
            " TOOL AND DOSEN'T HAVE TO COMPLY WITH ABOVE!!"
            ]

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
    draw_point("\033[31m", 0, 0)
    char = "█"
    for i in range(rows-1):
        print(char * columns)
    draw_point("\033[0m", 0, 0)
    print("\033[{};{}H{}".format(rows, 0, f"\033[33mCrosshell verification tool! Version: {version}\033[0m"), end="")

# [Collect stuff]
columns, rows = os.get_terminal_size()
computer = socket.gethostname()

# [Check if user has been saved]
try:
    requestAnsw = pantryapireq(key=PANTRYKEY,mode='get',basket='CrosshellVerifierNameList')
except:
    # Check if user is verified
    if not os.path.exists(has_verified_file):
        print("\033[31mError: No internet connection, please connect to internet and continue!\033[0m")
        exit()
try:
    UsersSaved_Dict = json.loads(requestAnsw.content.decode())
    UsersSaved = encdec_dict(key=KRYPTOKEY, dictionary=UsersSaved_Dict,mode='dec')
except:
    UsersSaved = {}

if UsersSaved.get(computer) == None:

    # [Drawing]
    middleX = (columns//2)-1
    middleY = (rows//2)-1
    draw_background()
    print("\033[4;38H\033[41;97mWho is going to be using this install?")
    print("\033[5;38H\033[41;97m▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔")
    print(f"\033[6;38H\033[101;97mComputer: {computer}")
    drawlib_internal_printmemsprite(HelpText,37,13,colorcode="41;91")
    name = inputAtCords(38, 7, text="User of this install: ", color="101;97")

    UserData = {f"{computer}":f"{name}"}
    UserData = encdec_dict(key=KRYPTOKEY, dictionary=UserData, mode='enc')
    ans = pantryapireq(key=PANTRYKEY,mode='append',basket='CrosshellVerifierNameList',json=UserData)

    fill_terminal(" ")
    print(f"\033[1;1H\033[32mVerified\033[0m")
    # Write output
    try:
        if os.path.exists(has_verified_file): os.remove(has_verified_file)
        f = open(has_verified_file, "w", encoding='utf-8')
        f.write("1")
        f.close()
    except: pass