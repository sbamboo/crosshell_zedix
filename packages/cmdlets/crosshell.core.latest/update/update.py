# Imports
import yaml
import argparse
from assets.lib.copylib import *

# Setup
temporaryFolder = f"{csbasedir}{os.sep}.temp"
localVersionFile = cs_versionFile
onlineVersionUrl = "https://github.com/simonkalmiclaesson/crosshell_zedix/raw/main/assets/version.yaml"

# Argument handling
cparser = argparse.ArgumentParser(prog="Update",exit_on_error=False,add_help=False)
cparser.add_argument('-h', '--help', action='store_true', default=False, help='Shows help menu.')
cparser.add_argument('--exhelp', action='store_true', default=False, help='Shows help then exits.')
# Force
cparser.add_argument('--force','--f', dest="force", action='store_true', help="Forces update to install an update.")
# Create main arguments object
try: argus = cparser.parse_args(argv)
except: argus = cparser.parse_args()
if argus.help: cparser.print_help()
if argus.exhelp: cparser.print_help(); exit()

# Get local version id
with open(localVersionFile, "r") as yamli_file:
    localVersionid = int(yaml.safe_load(yamli_file)["vid"])
# Get online version id
invalid = False
try: onlineVersionid = int(yaml.safe_load((requests.get(onlineVersionUrl).content).decode())["vid"])
except: invalid = True
# Validate versionid
if str(onlineVersionid) == "" or onlineVersionid == None: invalid = True
if invalid == True: print(pt_format(cs_palette,"\033[31mUpdate error: Can't reach online host (github) check your connection.\033[0m"))
# Check if versions needs update
if localVersionid == onlineVersionid and argus.force != True:
    print(pt_format(cs_palette,"\033[33mUpdate canceled: The current version of crosshell is the newest avaliable. To update anyway use the '--force' parameter.\033[0m"))
elif localVersionid > onlineVersionid and argus.force != True:
    print(pt_format(cs_palette,"Update canceled: The current version of crosshell is newer then the latest avaliable online. To update anyway use the '--force' parameter.\033[0m"))
# Update
else:
    # Make temporary folder
    if not os.path.exists(temporaryFolder):
        os.mkdir(temporaryFolder)
    # Backup data to temporary folder
    root = f"{csbasedir}{os.sep}"
    print("Backing up data...")
    FilesToBackup = ["crosshell.py","settings.yaml"]
    FoldersToBackup = [f"assets"]
    # Backup files
    for File in FilesToBackup:
        if not os.path.exists(f"{temporaryFolder}{os.sep}{File}"):
            CopyFile(f"{root}{File}",f"{temporaryFolder}{os.sep}{File}")
    # Backup Folders
    for Folder in FoldersToBackup:
        if not os.path.exists(f"{temporaryFolder}{os.sep}{Folder}"):
            CopyFolder(f"{root}{Folder}",f"{temporaryFolder}{os.sep}{Folder}")
    print("Done!")
    # Remove current version of data
    for File in FilesToBackup:
        if os.path.exists(f"{temporaryFolder}{os.sep}{File}") and os.path.exists(f"{root}{File}"):
            os.remove(f"{root}{File}")
            pass
    # List files and folders
    for Folder in FoldersToBackup:
        folderpath = f"{root}{Folder}"
        entries = scantree(folderpath)
        for file in entries:
            if "__pycache__" not in file.path:
                if os.path.isfile(file.path):
                    os.remove(file.path)
                else:
                    os.rmdir(file.path)
        entries = scantree(folderpath)
        for file in entries:
            try: os.rmdir(file.path)
            except: pass