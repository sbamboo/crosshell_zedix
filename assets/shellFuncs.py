# Functions for crosshell (Zedix Core)
# Author: Simon Kalmi Claesson

# [Imports]
import os

# [Local imports]
from assets.utils.conUtils import *
from assets.coreFuncs import *


# [Function defines]

# Function to handle built ins.
def cs_builtins(inputs=str(),params=list(),allowedFileTypes=list()):
    # Exit command
    if inputs == "exit":
        exit()
    # Cls command (call clear function)
    elif inputs == "cls":
        clear()
    # If not a builtIn return a string informing of such
    else:
        return "\033[33mInfo: Not Built in\033[0m"
    # Return True if a command was executed
    return "True"

# Function to print out the profile
def cs_writeProfile(basedir,globalInput):
    # Set filepaths
    msgProfileFile = os.path.realpath(f"{basedir}{os.sep}assets{os.sep}profile.msg")
    pyProfileFile = os.path.realpath(f"{basedir}{os.sep}assets{os.sep}profile.py")
    # If a python Profilefile exists execute it
    if os.path.exists(pyProfileFile):
        exec(open(pyProfileFile).read(), globalInput)
    # Otherwise if a msg profileFile exists print out it's content
    elif os.path.exists(msgProfileFile):
        # Get content
        content = open(msgProfileFile,"r").read()
        # If not empty split by newlines and print out every line
        if content != "":
            for line in content.split("\n"):
                eval(f"print('{line}')")
    # If non of the above is found print out a message asking the user to add a file
    else:
        print("\033[33mOBS! No profile file, please add: '/assets/profile.msg'\033[0m")

# Function to write the header
def cs_writeHead(versionData=dict(),basedir=str(),globalInput=dict()):
    hasMoreLines = False
    # Channel Messages (Version Channel)
    channel = versionData.get("channel")
    # Release/Stable (No message)
    if channel != "Release" and channel != "Stable":
        hasMoreLines = True
    # Development
    if channel == "Development":
        print("\033[31mYou are running a development version of crosshell, bugs may occure and some features migth be missing.\033[0m")
    # Alpha
    elif channel == "Alpha":
        print("\033[33mYou are running a alpha version of crosshell, bugs may occure and some features migth be missing.\033[0m")
    # Beta
    elif channel == "Beta":
        print("\033[33mYou are running a beta version of crosshell, although these are stabler then alpha versions buggs may still occure.\033[0m")
    # Viva
    elif channel == "Viva":
        print("\033[33mYou are running the current version of Crosshell-VIVA, these are generally stable but may contain bugs.\033[0m")
    # No channel defined
    else:
        print("\033[31mThe version channel of your crosshell installation is not reconized, this may be a bug\033[0m")
    # If has more lines line are True print out an empty line to separate the above lines with the lower.
    if hasMoreLines == True: print("")
    # Write out the profile using a function
    # cs_writeProfile(<basedir>,<globalVariables>)
    cs_writeProfile(basedir,globalInput)
    # Show welcomme message depending if a file has been showed
    hasShownGuideStateFile = os.path.realpath(f"{basedir}{os.sep}assets{os.sep}hasshownguide.state")
    # If a file exists dont inform of the guide
    if os.path.exists(hasShownGuideStateFile):
        print("\033[32mWelcome, write 'help' for help. To add messages to here edit: /assets/profile.ps1\033[0m")
    # Otherwise do inform of a guide and create a state file to let crosshell know it has shown the guide message
    else:
        print("\033[32mWelcome, for a guide on how to use crosshell write 'guide' or for command help write 'help'.\033[0m") 
        _ = open(hasShownGuideStateFile, "x")

# Function to save a title using the setConTitle function and loading from persistance
def saveTitle(title=str(),filepath=str()):
    cs_persistance("set","cs_title",filepath,title)
    # setConTitle(<title>)
    setConTitle(title)