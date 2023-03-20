# [Imports] (This version needs crosshell.lib.filesys)
from assets.lib.filesys import filesys as fs
from assets.lib.conUtils import *
import os
import sys
import hashlib
import datetime

# [Arguments]
cparser = argparse.ArgumentParser(prog="FSman",exit_on_error=False,add_help=False)
cparser.add_argument('-h', '--help', action='store_true', default=False, help='Shows help menu.')
cparser.add_argument('--exhelp', action='store_true', default=False, help='Shows help then exits.')
# Options
cparser.add_argument('--libinfo', dest="libinfo", action='store_true', help="Shows library information")
# Package (Comsume al remaining arguments)
cparser.add_argument('args', nargs='*', help="Auto-consume arguments")
# Create main arguments object
try: argus = cparser.parse_args(argv)
except: argus = cparser.parse_args()
if argus.help: cparser.print_help()
if argus.exhelp: cparser.print_help(); exit()

# [Defines]
infoAuthor = "Simon Kalmi Claesson"
infoVersion = "1.0"
infoHeader = "FSman is a simple file manager written in Powershell"

licenseFile = f"{CSScriptRoot}{os.sep}license.txt"

lastError = ""
prefix_input = "[cd/op]: "
prefix_operation = "-"
prefix_command = "/"
opt_editor = "notepad.exe"
operations = {
    "re": "Deletes a file/folder (Takes: <path>)",
    "cp": "Copies a file/folder (Takes: <oldpath> <newpath>)",
    "mi": "Creates a file (Takes: <path>)",
    "md": "Creates a folder (Takes: <path>)",
    "st": "Executes a file (Takes: <path>)",
    "ed": "Opens a file in selected editor (Takes: <path>) [%opt_editor%]",
    "rn": "Renames a file/folder (Takes: <path>)",
    "zi": "Creates a zip of a file/folder (Takes: <path>)",
    "uz": "Unzips a zip archive (Takes: <path>)",
    "xp": "Opens a folder in the host's filemanager. (Takes: <path>)",
    "rd": "Shows the content of a file (Takes: <path>)",
    "ex": "Exits FSman"
}
commands = {
    "opt": "Opens Settings",
    "info": "Shows information about FSman",
    "help": "Shows this help info",
    "lice": "Shows the FSman license"
}
opt_hashes = False
opt_hashFormats = ["sha256"]
opt_outputType = "Default" # 'Default', 'Table'
opt_colorTheme = {
    "error": "\033[31m",
    "title": "\033[92m",
    "help_key": "\033[32m",
    "help_val": "\033[94m",
    "size_dir": "\033[34m",
    "size_file": "\033[91m",
    "modtime": "\033[93m",
    "hash": "\033[95m",
    "name_dir": "\033[94m",
    "name_file": "\033[92m",
    "reset": "\033[0m",
    "typeColors": {
        ".zip": "\033[32m",
        "tag:exe": "\033[35m"
    }
}

# [Hashlib implementation]
def getHash(filepath=str()) -> dict():
    global opt_hashFormats,opt_colorTheme
    # Define formats
    md5_ene, sha1_ene, sha256_ene = False,False,False
    if "md5" in opt_hashFormats:    md5_ene = True
    if "sha1" in opt_hashFormats:   sha1_ene = True
    if "sha256" in opt_hashFormats: sha256_ene = True
    # Define objects
    md5 = hashlib.md5()
    sha1 = hashlib.sha1()
    sha256 = hashlib.sha256()
    # Computate hash in chunks, Source: https://stackoverflow.com/a/22058673
    BUF_SIZE = 65536  # lets read stuff in 64kb chunks!
    try:
        with open(filepath, 'rb') as f:
            while True:
                data = f.read(BUF_SIZE)
                if not data:
                    break
                if md5_ene == True: md5.update(data)
                if sha1_ene == True: sha1.update(data)
                if sha256_ene == True: sha256.update(data)
    except PermissionError:
        return f"{opt_colorTheme['error']}<--------------------- Permission Denied ---------------------->{opt_colorTheme['reset']}"
    # Build return
    returnDict = dict()
    if md5_ene == True:
        returnDict["md5"] = md5.hexdigest()
    if sha1_ene == True:
        returnDict["sha1"] = sha1.hexdigest()
    if sha256_ene == True:
        returnDict["sha256"] = sha256.hexdigest()
    if returnDict != {}:
        return returnDict
    else:
        return None

# [Libinfo]
if argus.libinfo:
    print( fs.help(ret=True) )
    exit()

# [Functions]
def timeFormatter(unix_timestamp) -> str():
    utc_datetime = datetime.datetime.utcfromtimestamp(unix_timestamp)
    return utc_datetime.strftime('%Y-%m-%d %H:%M:%S')

def getDirData(directory=str()) -> dict():
    # define
    data = {
        "dir": directory
    }
    # handle
    entries = os.listdir(directory)
    # populate
    for entry in entries:
        entry = directory + os.sep + entry
        if fs.isDir(entry): _type = "folders"
        elif fs.isFile(entry): _type = "files"
        # get data
        _name = os.path.basename(entry)
        _modtime = os.path.getmtime(entry)
        _size = os.path.getsize(entry)
        if _type == "files": _hashes = getHash(entry)
        else:                _hashes = None
        # setkeys
        data[_name] = dict()
        data[_name]["path"] = entry
        data[_name]["type"] = _type
        data[_name]["modtime"] = timeFormatter(_modtime)
        data[_name]["size"] = _size
        data[_name]["hashes"] = _hashes
    # return
    return data

def renderTitle(curDir=str(),conSize=tuple()) -> None:
    global prefix_command,prefix_input,opt_colorTheme
    print(f"Write '{prefix_command}opt' for settings, '{prefix_command}help' for help or '{prefix_command}info' for for info.")
    print("-"*conSize[0])
    print(f"CurrentDir: {opt_colorTheme['title']}{curDir}{opt_colorTheme['reset']}\n")

def format_size(size):
    suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB']
    suffix_index = 0
    while size >= 1024 and suffix_index < len(suffixes)-1:
        suffix_index += 1   # increment the index of the suffix
        size /= 1024.0      # apply the division
    return f"{size:.2f}{suffixes[suffix_index]}"

def handleTypeColors(filepath=str(),default=str()) -> str():
    global opt_colorTheme
    fileExt = os.path.splitext(filepath)[1]
    isExe = fs.isExecutable(filepath=filepath)
    if "tag:exe" in list(opt_colorTheme["typeColors"].keys()) and isExe == True:
        return opt_colorTheme["typeColors"]["tag:exe"]
    if fileExt in list(opt_colorTheme["typeColors"].keys()):
        return opt_colorTheme["typeColors"][fileExt]
    else:
        return opt_colorTheme[default]


def default_viewFormatter(file_dict=dict(), hashType=str()):
    global opt_colorTheme,opt_hashes
    # initialize lists for files and folders
    folders = dict()
    files = dict()
    # separate files and folders
    for name, data in file_dict.items():
        if data["type"] == "folders":
            folders[name] = data
        else:
            files[name] = data
    # sort by name
    folders = dict(sorted(folders.items()))
    files = dict(sorted(files.items()))
    file_dict = folders | files
    # format output string
    output = ""
    for name, data in file_dict.items():
        if data["type"] == "folders":
            size = "<Dir>"
            sizeFormat = opt_colorTheme["size_dir"]
            nameFormat = opt_colorTheme["name_dir"]
        else:
            sizeFormat = opt_colorTheme["size_file"]
            nameFormat = handleTypeColors(filepath=data["path"],default="name_file")
            size = format_size(data["size"])
            size = size.replace(".00","")
        if opt_hashes and hashType:
            if type(data["hashes"]) == dict:
                hash_val = data["hashes"][hashType]
            elif type(data["hashes"]) == str:
                hash_val = data["hashes"]
            else:
                hash_val = "                                                                "
            output += f"{sizeFormat}{size:<8}  {opt_colorTheme['hash']}{hash_val}  {opt_colorTheme['modtime']}{data['modtime']}  {nameFormat}{name}\n"
        else:
            output += f"{sizeFormat}{size:<8}  {opt_colorTheme['modtime']}{data['modtime']}  {nameFormat}{name}\n"
    return output + opt_colorTheme['reset']

def showHelp() -> None:
    global operations,prefix_command,prefix_operation,opt_colorTheme
    clear()
    print("FSman Help:")
    print('-'*conSize[0])
    max_key_length = max(len(key) for key in operations | commands)
    # iterate over the dictionary and print each key-value pair with padding
    for key, value in operations.items():
        padding = ' ' * (max_key_length - len(key))
        print(f"{opt_colorTheme['help_key']}{prefix_operation}{key}{padding} {opt_colorTheme['reset']}:  {opt_colorTheme['help_val']}{value}{opt_colorTheme['reset']}")
    print()
    # iterate over the dictionary and print each key-value pair with padding
    for key, value in commands.items():
        padding = ' ' * (max_key_length - len(key))
        print(f"{opt_colorTheme['help_key']}{prefix_command}{key}{padding} {opt_colorTheme['reset']}:  {opt_colorTheme['help_val']}{value}{opt_colorTheme['reset']}")
    print('-'*conSize[0])
    print("Press any key to continue...")
    pause()



def showOpt() -> None:
    pass

def runOperations(command=str(),arguments=str()) -> None:
    # Exit
    if command == "ex": exit()

def renderDirData(data=dict()) -> None:
    global opt_outputType,opt_hashFormats
    data.pop("dir")
    # Default
    if opt_outputType == "Default":
        print( default_viewFormatter(file_dict=data,hashType=opt_hashFormats[0]))

def handleOperations(data=dict(),command=str(),conSize=tuple()):
    global prefix_command,prefix_input,infoHeader,infoAuthor,infoVersion,operations
    matched = True
    # Info
    if f"{prefix_command}info" == command: 
        clear()
        print(f"FSman Info:\n{'-'*conSize[0]}\n{infoHeader}\nMade by: {infoAuthor}\nVersion: {infoVersion}\n\nFSman_binPath: {CSScriptRoot}\n{'-'*conSize[0]}\n")
        print("Press any button to continue...")
        pause()
    # Help
    elif f"{prefix_command}help" == command:
        showHelp()
    # Opt
    elif f"{prefix_command}opt" == command:
        showOpt()
    # Licence
    elif f"{prefix_command}lice" == command:
        clear()
        print( fs.readFromFile(licenseFile) )
        print("Press any key to continue...")
        pause()
    else:
        matched = False
    # Run operations
    if " " in command: scommand = (command.split(" "))[0]
    else: scommand = command
    scommand = scommand.lstrip(prefix_operation)
    if scommand in list(operations.keys()) and command[0] == prefix_operation:
        acommand = command.replace(scommand,"")
        acommand = acommand.strip()
        matched = True
        runOperations(command=scommand,arguments=acommand)
    # No match
    if matched == False:
        return command

# [Savedir & Loaddir]
olddir = os.getcwd()
currentDir = olddir

# [Mainloop]
mainloop = True
while mainloop == True:
    # prep
    columns,lines = os.get_terminal_size()
    conSize = (columns,lines)
    currentDir = os.getcwd()
    # Print title
    clear()
    renderTitle(curDir=currentDir, conSize=conSize)
    # Get data
    dirData = getDirData(directory=currentDir)
    # Render dir data
    renderDirData(data=dirData)
    # Show errors
    if lastError != "":
        print(lastError)
        lastError = ""
    else: print("")
    # Get operation from player
    op = input(prefix_input)
    # handleOperation
    outDir = handleOperations(data=dirData,command=op,conSize=conSize)
    try:
        if outDir != None:
            if os.path.isabs(outDir):
                os.chdir(outDir)
            else:
                os.chdir(os.path.join(currentDir, outDir))
    except FileNotFoundError:
        lastError = f"{opt_colorTheme['error']}Directory '{outDir}' not found!{opt_colorTheme['reset']}"