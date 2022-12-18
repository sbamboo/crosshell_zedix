# [Imports]
import os
import argparse
import re


# [Local imports]
# Core
from assets.evaluate import *
from assets.coreFuncs import *
from assets.shellFuncs import *
# Utils
from assets.utils.conUtils import *
from assets.utils.utilFuncs import *
from assets.utils.formatter import *
# Ui
from assets.uilib.tqdm_ui import *


# [Parameters]
# Define Help
parser = argparse.ArgumentParser(
  prog="Crosshell (Zedix)",
  description='''Python version of crosshell!''',
  epilog="\033[31mStill in development, Made by Simon Kalmi Claesson\033[0m"
)
# Add in arguments
parser.add_argument('-c', dest="command", help='command to pass to crosshell')
parser.add_argument('--noexit', help='Starts crosshell after running a command', action='store_true')
parser.add_argument('--nocls', help='supress clearscreens', action='store_true')
parser.add_argument('--nohead', help='supress header', action='store_true')
parser.add_argument('--is_internaly_called', help='supress header', action='store_true')
parser.add_argument('--debug_args', help='supress header', action='store_true')
# Create main arguments object
args = parser.parse_args()

# ==========================================================[Setup code]========================================================== #

# [Setup]
# Python
os.system("") # Enables ANSI escape sequences on Windows
# Core
csbasedir = os.path.dirname(os.path.realpath(__file__))
cs_versionFile = os.path.realpath(f"{csbasedir}/assets/version.yaml")
# Settings, Persistance files
cs_settingsFile = os.path.realpath(f"{csbasedir}/settings.yaml")
cs_persistanceFile = os.path.realpath(f"{csbasedir}/assets/persistance.yaml")
# Defaults
cssettings_raw = {}
csprefix_dir = True
csprefix_enabled = True
crosshell_doLoop = True
csworking_directory = os.getcwd()
allowedFileTypes = [".py",".ps1",".cmd",".bat",".exe"]
persPrintCmdletDebug = False


# [Settings]
# Get and set settings
cssettings_raw = cs_settings("load",cs_settingsFile,cssettings_raw)
cssettings = cssettings_raw
# Load title from persistance otherwise from settings
perstitle = cs_persistance("get","cs_title",cs_persistanceFile)
if perstitle != "" and perstitle != None:
    saveTitle(perstitle,cs_persistanceFile)
else:
    saveTitle(cssettings["Presets"]["Title"],cs_persistanceFile)
# Load prefix from persistance otherwise from settings
persprefix = cs_persistance("get","cs_prefix",cs_persistanceFile)
if persprefix != "" and persprefix != None:
    csshell_prefix = persprefix
else:
    csshell_prefix = cssettings["Presets"]["Prefix"]
# Load prefix_enabled from persistance otherwise from settings
persprefix_enabled = cs_persistance("get","cs_prefix_enabled",cs_persistanceFile)
if persprefix_enabled != "" and persprefix_enabled != None:
    csprefix_enabled = persprefix_enabled
else:
    csprefix_enabled = cssettings["General"]["Prefix_Enabled"]
# Load prefix_dir from persistance otherwise from settings
persprefix_dir = cs_persistance("get","cs_prefix_enabled_dir",cs_persistanceFile)
if persprefix_dir != "" and persprefix_dir != None:
    csprefix_dir = persprefix_dir
else:
    csprefix_dir = cssettings["General"]["Prefix_Dir_Enabled"]
# Load printcmdletdebug setting
persPrintCmdletDebug = bool(cssettings["General"]["PrintCmdletDebug"])

# Get version data
try:
    versionData = cs_persistance_yaml("get",dict(),cs_versionFile)
except:
    versionData = {}


# =========================================================[Main app code]========================================================= #

# [Load and handle arguments]

# Clear on start if enabled thru arguments
if args.nocls == False: clear()

# Debug args
if args.debug_args == True: print(args)

# Load pathables
cspathables = cs_loadCmdlets(os.path.realpath(f"{csbasedir}/packages/cmdlets"),allowedFileTypes)

# [Main Loop]

# Write header if enabled from settings
if args.nohead == False: cs_writeHead(versionData,csbasedir,globals())

# Run Loop if the "crosshell_doLoop" is enabled
while crosshell_doLoop == True:
    # Handle the command argument and if a command is given set it as the input
    if args.command != "" and args.command != None:
        paramCommand = True
        inputs = str(args.command)
    # If no command argument was given ask the user for input
    else:
        paramCommand = False
        # If prefix is enabled ask the user for input with prefix otherwise don't render the prefix
        if bool(csprefix_enabled) == True:
            # formatPrefix(<prefix-rawtext>,<prefix-dir-enabled>,<prefix-enabled><working-directory><globalVariables>)
            inputs = input(formatPrefix(cs_persistance("get","cs_prefix",cs_persistanceFile),bool(csprefix_dir),bool(csprefix_enabled),csworking_directory,globals()))
        else:
            inputs = input("")
    # Check if the input has pipes and if so set the hasPipes bool variable accoringlt and split the input by the pipe syntax " | "
    if " | " in inputs: # Has pipes
        hasPipes = True
        pipeParts = inputs.split(" | ")
    else: # No pipes
        hasPipes = False
        pipeParts = [inputs]
    # Handle pipe parts and pipeSTDOUT passing
    pipeSTDOUT = ""
    # Enumerate through the pipeParts
    for pipeIndex,pipePart in enumerate(pipeParts):
        # Handle parantheses in command/pipePart
        if "(" in pipePart and " " not in pipePart:
            pipePart = pipePart.replace("("," ")
            pipePart = pipePart.replace(")"," ")
            pipePart = pipePart.replace(","," ")
        # Handle hardcoded string elements '"<string>"'
        # regex
        foundStrings = re.finditer(r'".*?"',pipePart)
        # Add the hardcoded print command to the pipePart/input
        for m in foundStrings:
            if str(m.group()) == str(pipePart):
                pipePart = "print " + str(pipePart).strip('"')
        # Handle spaces inside string and replace them with a temporary placeholder "§!i_space!§" before split by space so spaces inside string elements are kept
        for m in foundStrings:
            o = str(m.group()).replace(" ","§!i_space!§")
            pipePart = pipePart.replace(str(m.group()),o)
        # Split pipePart/input by space to command and parameters
        partials = pipePart.split(" ")
        # Set command
        cmd = partials[0]
        # Replace space temporary placeholder in command
        cmd = cmd.replace("§!i_space!§"," ")
        # Set parameters to send to command
        params = partials[1:]
        # Replace space temporary placeholder in parameters by enumerating through them
        for i,param in enumerate(params):
            params[i] = str(params[i]).replace("§!i_space!§"," ")
        # Handle commonparameters with the function
        # cs_handleCommonParameters(<command>,<parameters>)
        cmd,params = cs_handleCommonParameters(cmd,params)

        # Handle built in reload command
        if cmd == "reload":
            # cs_loadCmdlets(<cmdlets-folder-path>,<allowedFileTypes>)
            cspathables = cs_loadCmdlets(os.path.realpath(f"{csbasedir}/packages/cmdlets"),allowedFileTypes)

        # Handle built in restart command
        #elif cmd == "restart":
        #    path = csbasedir + os.sep + "zedix.py"
        #    exec(open(path).read(), globals())

        # Handle built in cs.getPathables Command wich shows and parses the pathables dictionary/list
        elif cmd == "cs.getPathables":
            # Iterate through pathables
            for i in cspathables:
                # Parse out pathable data by semicolons for diffrent properties and colons for name/data of said property
                d = i.split(";")
                d[0] = d[0].replace(':"',': "')
                # Print Name
                print(f"\033[33m{d[0]}\033[0m")
                # iterate through data and print it out (check for [] as a list or " for strings)
                for i in range(1,len(d)):
                    d[i] = d[i].replace(':"',': "')
                    d[i] = d[i].replace(':[',': [')
                    # Print data
                    print(f"   \033[32m{d[i]}\033[0m")
                # Print empty line
                print("")

        # Handle non hardcoded-builtin commands if command is not Empty or None
        elif cmd != "" and cmd != None:
            # Check for non hardcoded builtin commads
            # cs_builtins(<command>,<parameters>,<allowedFileTypes>)
            if "Info:" in cs_builtins(cmd,params,allowedFileTypes):
                # Get cmdlet path with a function
                # cs_getPathablePath(<pathables>,<command>)
                path = cs_getPathablePath(cspathables,cmd)
                # If the above function returned an error print it out
                if "Error:" in path:
                    print(path)
                # Otherwise execute the cmdlet
                else:
                    # If no pipes are present execute the cmdlet without requesting STDOUT
                    if hasPipes == False:
                        # cs_exec(<path-to-cmdlet>,<parameter>,<globalVariables>,<passSTDOUT>,<printCmdletDebug>)
                        cs_exec(path,params,globals(),False,persPrintCmdletDebug)
                    # If pipes are present execute the cmdlet and handle pipeSTDOUT
                    else:
                        # Hardcoded parsing of byteType string (non decoded/encoded string) from pipeSTDOUT
                        if "b'" in str(pipeSTDOUT):
                            str_pipeSTDOUT = str(pipeSTDOUT)
                            str_pipeSTDOUT = str_pipeSTDOUT.strip("b'")
                            str_pipeSTDOUT= str_pipeSTDOUT.rstrip("'")
                            str_pipeSTDOUT = str_pipeSTDOUT.replace("\\n","\n")
                            str_pipeSTDOUT = str_pipeSTDOUT.replace("\\r","\r")
                            pipeSTDOUT = str_pipeSTDOUT
                        # Handle pipeSTDOUT by adding it to the end of the parameters list that later would get sent. If pipeSTDOUT is not empty or None
                        if pipeSTDOUT != "" and pipeSTDOUT != None:
                            params = [*params,pipeSTDOUT]
                        # If the current pipe aren't the last one request the STDOUT to the pipeSTDOUT variable
                        if pipeIndex != (len(pipeParts)-1):
                            # cs_exec(<path-to-cmdlet>,<parameter>,<globalVariables>,<passSTDOUT>,<printCmdletDebug>)
                            pipeSTDOUT = cs_exec(path,params,globals(),True,persPrintCmdletDebug)
                        # If it is the last one don't request STDOUT so the last pipeElem's output dosen't get captured, which is not needed
                        else:
                            # cs_exec(<path-to-cmdlet>,<parameter>,<globalVariables>,<passSTDOUT>,<printCmdletDebug>)
                            cs_exec(path,params,globals(),False,persPrintCmdletDebug)
    # If a command argument is given check if the console should exit post command execution
    if paramCommand == True:
        # If the noexit argument is not given exit
        if bool(args.noexit) == False:
            exit()
        # Else stay but reset the command argument so it dosen't loop the execution of it
        else:
            args.command = ""