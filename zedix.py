# [Imports]
import os
import argparse

# [Local imports]
from assets.utils.conUtils import *
from assets.utils.utilFuncs import *
from assets.utils.formatter import *
from assets.evaluate import *
from assets.coreFuncs import *
from assets.shellFuncs import *

# [Parameters]
parser = argparse.ArgumentParser(
  prog="Crosshell (Zedix)",
  description='''Python version of crosshell!''',
  epilog="\033[31mStill in development, Made by Simon Kalmi Claesson\033[0m"
)
parser.add_argument('-c', dest="command", help='command to pass to crosshell')
parser.add_argument('--noexit', help='Starts crosshell after running a command', action='store_true')
parser.add_argument('--nocls', help='supress clearscreens', action='store_true')
parser.add_argument('--nohead', help='supress header', action='store_true')
parser.add_argument('--is_internaly_called', help='supress header', action='store_true')
parser.add_argument('--debug_args', help='supress header', action='store_true')
args = parser.parse_args()

# [Setup]
os.system("") # Enables ANSI escape sequences on Windows
allowedFileTypes = [".py",".ps1",".cmd",".bat",".exe"]
cssettings_raw = {}
csbasedir = os.path.dirname(os.path.realpath(__file__))
cs_settingsFile = os.path.realpath(f"{csbasedir}/settings.yaml")
cs_persistanceFile = os.path.realpath(f"{csbasedir}/assets/persistance.yaml")
cs_versionFile = os.path.realpath(f"{csbasedir}/assets/version.yaml")
csworking_directory = os.getcwd()
csprefix_dir = True
csprefix_enabled = True
zedix_doLoop = True

# [Settings]
# Get and set settings
cssettings_raw = cs_settings("load",cs_settingsFile,cssettings_raw)
cssettings = cssettings_raw
# Load title
perstitle = cs_persistance("get","cs_title",cs_persistanceFile)
if perstitle != "" and perstitle != None:
    saveTitle(perstitle,cs_persistanceFile)
else:
    saveTitle(cssettings["Presets"]["Title"],cs_persistanceFile)
# Load prefix
persprefix = cs_persistance("get","cs_prefix",cs_persistanceFile)
if persprefix != "" and persprefix != None:
    csshell_prefix = persprefix
else:
    csshell_prefix = cssettings["Presets"]["Prefix"]
# Load prefix_enabled
persprefix_enabled = cs_persistance("get","cs_prefix_enabled",cs_persistanceFile)
if persprefix_enabled != "" and persprefix_enabled != None:
    csprefix_enabled = persprefix_enabled
else:
    csprefix_enabled = cssettings["General"]["Prefix_Enabled"]
# Load prefix_dir
persprefix_dir = cs_persistance("get","cs_prefix_enabled_dir",cs_persistanceFile)
if persprefix_dir != "" and persprefix_dir != None:
    csprefix_dir = persprefix_dir
else:
    csprefix_dir = cssettings["General"]["Prefix_Dir_Enabled"]

# Get version data
try:
    versionData = cs_persistance_yaml("get",dict(),cs_versionFile)
except:
    versionData = {}

# [Code]

# Clear on start
if args.nocls == False:
    clear()

# Debug args
if args.debug_args == True: print(args)

# Load pathables
cspathables = cs_loadCmdlets("./packages/cmdlets",allowedFileTypes)

# Run loop
if args.nohead == False: cs_writeHead(versionData,csbasedir,globals())
while zedix_doLoop == True:
    if args.command != "" and args.command != None:
        paramCommand = True
        inputs = str(args.command)
    else:
        paramCommand = False
        if bool(csprefix_enabled) == True:
            inputs = input(formatPrefix(cs_persistance("get","cs_prefix",cs_persistanceFile),bool(csprefix_dir),bool(csprefix_enabled),csworking_directory,globals()))
        else:
            inputs = input("")
    # Has pipes
    if " | " in inputs:
        hasPipes = True
        pipeParts = inputs.split(" | ")
    else:
        hasPipes = False
        pipeParts = [inputs]
    # handle pipes
    pipeSTDOUT = ""
    for pipeIndex,pipePart in enumerate(pipeParts):
        # Handle parantheses
        if "(" in pipePart and " " not in pipePart:
            pipePart = pipePart.replace("("," ")
            pipePart = pipePart.replace(")"," ")
            pipePart = pipePart.replace(","," ")
        partials = pipePart.split(" ")
        cmd = partials[0]
        params = partials[1:]
        # Handle commonparameters
        cmd,params = cs_handleCommonParameters(cmd,params)
        # Reload command
        if cmd == "reload":
            cspathables = cs_loadCmdlets("./packages/cmdlets",allowedFileTypes)
        # Restart command
        #elif cmd == "restart":
        #    path = csbasedir + os.sep + "zedix.py"
        #    exec(open(path).read(), globals())
        # cs.getPathables Command
        elif cmd == "cs.getPathables":
            for i in cspathables:
                d = i.split(";")
                d[0] = d[0].replace(':"',': "')
                print(f"\033[33m{d[0]}\033[0m")
                for i in range(1,len(d)):
                    d[i] = d[i].replace(':"',': "')
                    d[i] = d[i].replace(':[',': [')
                    print(f"   \033[32m{d[i]}\033[0m")
                print("")
        # Al other commands
        elif cmd != "":
            if "Info:" in cs_builtins(cmd,allowedFileTypes):
                path = cs_getPathablePath(cspathables,cmd)
                if "Error:" in path:
                    print(path)
                else:
                    # Excute
                    if hasPipes == False:
                        cs_exec(path,params,globals(),False)
                    else:
                        # Handle unnice pipeElems in pipeSTDOUT
                        if "b'" in str(pipeSTDOUT):
                            str_pipeSTDOUT = str(pipeSTDOUT)
                            str_pipeSTDOUT = str_pipeSTDOUT.strip("b'")
                            str_pipeSTDOUT= str_pipeSTDOUT.rstrip("'")
                            str_pipeSTDOUT = str_pipeSTDOUT.replace("\\n","\n")
                            str_pipeSTDOUT = str_pipeSTDOUT.replace("\\r","\r")
                            pipeSTDOUT = str_pipeSTDOUT
                        # Handle pipeSTDOUT
                        if pipeSTDOUT != "" and pipeSTDOUT != None:
                            params = [pipeSTDOUT, *params]
                        if pipeIndex != (len(pipeParts)-1):
                            pipeSTDOUT = cs_exec(path,params,globals(),True)
                        else:
                            cs_exec(path,params,globals(),False)
    if paramCommand == True:
        if bool(args.noexit) == False:
            exit()
        else:
            args.command = ""