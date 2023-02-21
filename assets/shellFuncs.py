# Functions for crosshell (Zedix Core)
# Author: Simon Kalmi Claesson

# [Imports]
import os
import re

# [Local imports]
from assets.lib.conUtils import *
from assets.coreFuncs import *
from assets.paletteText import *
from assets.lib.filesys import filesys as fs


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
def cs_writeProfile(basedir,globalInput,cs_palette):
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
                line = pt_format(cs_palette,line)
                eval(f"print('{line}')")
    # If non of the above is found create the file
    else:
        fs.writeToFile("",msgProfileFile,autocreate=True)
        #print(pt_format(cs_palette,"\033[33mOBS! No profile file, please add: '/assets/profile.msg'\033[0m"))

# Function to write the welcome message
def cs_writeWelcome(versionData=dict(),basedir=str(),globalInput=dict(),cs_palette=dict()):
    hasMoreLines = False
    # Channel Messages (Version Channel)
    channel = versionData.get("channel")
    # Release/Stable (No message)
    if channel != "Release" and channel != "Stable":
        hasMoreLines = True
    # Development
    if channel == "Development":
        print(pt_format(cs_palette,"\033[31mYou are running a development version of crosshell, bugs may occure and some features migth be missing.\033[0m"))
    # Alpha
    elif channel == "Alpha":
        print(pt_format(cs_palette,"\033[33mYou are running a alpha version of crosshell, bugs may occure and some features migth be missing.\033[0m"))
    # Beta
    elif channel == "Beta":
        print(pt_format(cs_palette,"\033[33mYou are running a beta version of crosshell, although these are stabler then alpha versions buggs may still occure.\033[0m"))
    # Viva
    elif channel == "Viva":
        print(pt_format(cs_palette,"\033[33mYou are running the current version of Crosshell-VIVA, these are generally stable but may contain bugs.\033[0m"))
    # No channel defined
    else:
        print(pt_format(cs_palette,"\033[31mThe version channel of your crosshell installation is not reconized, this may be a bug\033[0m"))
    # If has more lines line are True print out an empty line to separate the above lines with the lower.
    if hasMoreLines == True: print("")
    # Write out the profile using a function
    # cs_writeProfile(<basedir>,<globalVariables>)
    cs_writeProfile(basedir,globalInput,cs_palette)
    # Show welcomme message depending if a file has been showed
    hasShownGuideStateFile = os.path.realpath(f"{basedir}{os.sep}assets{os.sep}hasshownguide.state")
    # If a file exists dont inform of the guide
    if os.path.exists(hasShownGuideStateFile):
        print(pt_format(cs_palette,"\033[32mWelcome, write 'help' for help. To add messages to here edit: /assets/profile.msg\033[0m"))
    # Otherwise do inform of a guide and create a state file to let crosshell know it has shown the guide message
    else:
        print(pt_format(cs_palette,"\033[32mWelcome, for a guide on how to use crosshell write 'guide' or for command help write 'help'.\033[0m"))
        _ = open(hasShownGuideStateFile, "x")

# Function to save a title using the setConTitle function and loading from persistance
def saveTitle(title=str(),filepath=str()):
    cs_persistance("set","cs_title",filepath,title)
    # setConTitle(<title>)
    setConTitle(title)

    
# Function to handle commonparameters from input and return the correct values
def cs_handleCommonParameters(cmd=str(),params=list()):
    if len(params) != 0:
        lastParam = str(params[-1])
        # Help
        if lastParam == "/help" or lastParam == "/?" or lastParam == "-?" or lastParam == "/h" or lastParam == "/Help" or lastParam == "/H":
            params.pop(-1)
            params = [cmd,*params]
            cmd = "get-help"
        # Search
        if lastParam == "/search" or lastParam == "/Search":
            params.pop(-1)
            params = [cmd,*params]
            cmd = "help"
        # Webi
        if lastParam == "/webi" or lastParam == "/Webi":
            params.pop(-1)
            params = [cmd,*params]
            cmd = "webi"
        # Calc
        if lastParam == "/calc" or lastParam == "/Calc":
            params.pop(-1)
            params = [cmd,*params]
            cmd = "calc"
    return cmd,params


# Define a basic calculator function
def cs_Is_math_expression(expression):
    # Build a regular expression pattern to match digits, arithmetic operators, parentheses
    pattern = r"^[0-9\.\+\-\*\/\(\)\s]*$"
    # Use the search function to check if the expression matches the pattern
    match = re.search(pattern, expression)
    return match is not None
def cs_basiccalculate(expression):
    # Check if the expression is valid
    if cs_Is_math_expression(expression):
        return eval(expression)