# Imports
import os
import yaml
import argparse
import traceback
from assets.lib.netwa import simpleDownload
from assets.lib.filesys import filesys as fs
from assets.lib.gitAPI import *

# Setup
temporaryFolder = f"{csbasedir}{os.sep}.temp"
localVersionFile = cs_versionFile
onlineVersionUrl = "https://github.com/simonkalmiclaesson/crosshell_zedix/raw/main/assets/version.yaml"

# Argument handling
cparser = argparse.ArgumentParser(prog="Update",exit_on_error=False,add_help=False)
cparser.add_argument('-h', '--help', action='store_true', default=False, help='Shows help menu.')
cparser.add_argument('--exhelp', action='store_true', default=False, help='Shows help then exits.')
# Params
cparser.add_argument('--force','--f', dest="force", action='store_true', help="Forces update to install an update.")
cparser.add_argument('--gitapi','--g', dest="gitapi", action='store_true', help="Uses gitapi update system.")
cparser.add_argument('-gittoken', dest="AuthGitToken", help="A github token to use for authentication. (allowes more then one update per hour)")
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
    print(pt_format(cs_palette,"\033[33mNote! The update system is still in development so errors may arise, please always manualy backup your data/install before updating.\033[0m"))
    _ = input("Press any button to continue...")
    if argus.gitapi != True:
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
                fs.copyFile(f"{root}{File}",f"{temporaryFolder}{os.sep}{File}")
        # Backup Folders
        for Folder in FoldersToBackup:
            if not os.path.exists(f"{temporaryFolder}{os.sep}{Folder}"):
                fs.copyFolder2(f"{root}{Folder}",f"{temporaryFolder}{os.sep}{Folder}")
        print("Done!")
        print("Removing current data (Not the backup)...")
        # Remove current version of data
        for File in FilesToBackup:
            if os.path.exists(f"{temporaryFolder}{os.sep}{File}") and os.path.exists(f"{root}{File}"):
                os.remove(f"{root}{File}")
                pass
        # Remove things from folders
        for Folder in FoldersToBackup:
            folderpath = f"{root}{Folder}"
            entries = fs.scantree(folderpath)
            for file in entries:
                if "__pycache__" not in file.path:
                    if os.path.isfile(file.path):
                        os.remove(file.path)
                    else:
                        os.rmdir(file.path)
            entries = fs.scantree(folderpath)
            for file in entries:
                try: os.rmdir(file.path)
                except: pass
        print("Done!")
        print("Downloading files... This can take awhile!")
        simpleDownload("https://github.com/simonkalmiclaesson/crosshell_zedix/archive/refs/heads/main.zip",f"{temporaryFolder}{os.sep}update_temp.zip")
        print("Unpacking downloaded files...")
        from zipfile import ZipFile
        if not os.path.exists(f"{temporaryFolder}{os.sep}update_temp"): os.mkdir(f"{temporaryFolder}{os.sep}update_temp")
        with ZipFile(f"{temporaryFolder}{os.sep}update_temp.zip", 'r') as zObject:
            zObject.extractall(path=f"{temporaryFolder}{os.sep}update_temp")
        fs.copyFolder2(f"{temporaryFolder}{os.sep}update_temp{os.sep}crosshell_zedix-main{os.sep}assets",f"{root}assets")
        fs.copyFile(f"{temporaryFolder}{os.sep}update_temp{os.sep}crosshell_zedix-main{os.sep}crosshell.py",f"{root}crosshell.py")
        print("Done!")
        print("Moving back user files...")
        # Copy back user data
        if os.path.exists(f"{temporaryFolder}{os.sep}settings.yaml"): fs.copyFile(f"{temporaryFolder}{os.sep}settings.yaml",f"{root}settings.yaml")
        if os.path.exists(f"{temporaryFolder}{os.sep}assets{os.sep}persistance.yaml"): fs.copyFile(f"{temporaryFolder}{os.sep}assets{os.sep}persistance.yaml",f"{root}assets{os.sep}persistance.yaml")
        if os.path.exists(f"{temporaryFolder}{os.sep}assets{os.sep}profile.msg"): fs.copyFile(f"{temporaryFolder}{os.sep}assets{os.sep}profile.msg",f"{root}assets{os.sep}profile.msg")
        if os.path.exists(f"{temporaryFolder}{os.sep}assets{os.sep}profile.py"): fs.copyFile(f"{temporaryFolder}{os.sep}assets{os.sep}profile.py",f"{root}assets{os.sep}profile.py")
        if os.path.exists(f"{temporaryFolder}{os.sep}assets{os.sep}.history"): fs.copyFile(f"{temporaryFolder}{os.sep}assets{os.sep}.history",f"{root}assets{os.sep}.history")
        print("Done!")
        print("Cleaning up, removing backuped data...")
        # Remove backups
        fs.deleteDirNE(temporaryFolder)
        print("Done!")
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
                fs.copyFile(f"{root}{File}",f"{temporaryFolder}{os.sep}{File}")
        # Backup Folders
        for Folder in FoldersToBackup:
            if not os.path.exists(f"{temporaryFolder}{os.sep}{Folder}"):
                fs.copyFolder2(f"{root}{Folder}",f"{temporaryFolder}{os.sep}{Folder}")
        print("Done!")
        print("Removing current data (Not the backup)...")
        # Remove current version of data
        for File in FilesToBackup:
            if os.path.exists(f"{temporaryFolder}{os.sep}{File}") and os.path.exists(f"{root}{File}"):
                os.remove(f"{root}{File}")
                pass
        # Remove things from folders
        for Folder in FoldersToBackup:
            folderpath = f"{root}{Folder}"
            entries = fs.scantree(folderpath)
            for file in entries:
                if "__pycache__" not in file.path:
                    if os.path.isfile(file.path):
                        os.remove(file.path)
                    else:
                        os.rmdir(file.path)
            entries = fs.scantree(folderpath)
            for file in entries:
                try: os.rmdir(file.path)
                except: pass
        print("Done!")

        # Download new assets
        print("Downloading assets...")
        try:
            if argus.AuthGitToken: gitFolderDownRecurse("https://api.github.com/repos/simonkalmiclaesson/crosshell_zedix/contents/assets",resultDir=f"{root}assets",Authorization=str(argus.AuthGitToken))
            else:                  gitFolderDownRecurse("https://api.github.com/repos/simonkalmiclaesson/crosshell_zedix/contents/assets",resultDir=f"{root}assets")
            simpleDownload("https://github.com/simonkalmiclaesson/crosshell_zedix/raw/main/crosshell.py",f"{root}crosshell.py")
            print("Done!")
            print("Moving back user files...")
            # Copy back user data
            if os.path.exists(f"{temporaryFolder}{os.sep}settings.yaml"): fs.copyFile(f"{temporaryFolder}{os.sep}settings.yaml",f"{root}settings.yaml")
            if os.path.exists(f"{temporaryFolder}{os.sep}assets{os.sep}persistance.yaml"): fs.copyFile(f"{temporaryFolder}{os.sep}assets{os.sep}persistance.yaml",f"{root}assets{os.sep}persistance.yaml")
            if os.path.exists(f"{temporaryFolder}{os.sep}assets{os.sep}profile.msg"): fs.copyFile(f"{temporaryFolder}{os.sep}assets{os.sep}profile.msg",f"{root}assets{os.sep}profile.msg")
            if os.path.exists(f"{temporaryFolder}{os.sep}assets{os.sep}profile.py"): fs.copyFile(f"{temporaryFolder}{os.sep}assets{os.sep}profile.py",f"{root}assets{os.sep}profile.py")
            if os.path.exists(f"{temporaryFolder}{os.sep}assets{os.sep}.history"): fs.copyFile(f"{temporaryFolder}{os.sep}assets{os.sep}.history",f"{root}assets{os.sep}.history")
            print("Done!")
            print("Cleaning up, removing backuped data...")
            # Remove backups
            shutil.rmtree(temporaryFolder)
            print("Done!")
        except Exception:
            print("Download failed, reverting changes...")
            print("Revering: Removing downloaded data...")
            # Remove things from folders
            for Folder in FoldersToBackup:
                folderpath = f"{root}{Folder}"
                entries = fs.scantree(folderpath)
                for file in entries:
                    if "__pycache__" not in file.path:
                        if os.path.isfile(file.path):
                            os.remove(file.path)
                        else:
                            os.rmdir(file.path)
                entries = fs.scantree(folderpath)
                for file in entries:
                    try: os.rmdir(file.path)
                    except: pass
            # UnBackup files
            for File in FilesToBackup:
                if os.path.exists(f"{temporaryFolder}{os.sep}{File}"):
                    fs.copyFile(f"{temporaryFolder}{os.sep}{File}",f"{root}{File}")
            print("Reverting: Done removing data!")
            print("Reverting: Copy back user data...")
            # Copy back user data
            if os.path.exists(f"{temporaryFolder}{os.sep}settings.yaml"): fs.copyFile(f"{temporaryFolder}{os.sep}settings.yaml",f"{root}settings.yaml")
            if os.path.exists(f"{temporaryFolder}{os.sep}assets{os.sep}persistance.yaml"): fs.copyFile(f"{temporaryFolder}{os.sep}assets{os.sep}persistance.yaml",f"{root}assets{os.sep}persistance.yaml")
            if os.path.exists(f"{temporaryFolder}{os.sep}assets{os.sep}profile.msg"): fs.copyFile(f"{temporaryFolder}{os.sep}assets{os.sep}profile.msg",f"{root}assets{os.sep}profile.msg")
            if os.path.exists(f"{temporaryFolder}{os.sep}assets{os.sep}profile.py"): fs.copyFile(f"{temporaryFolder}{os.sep}assets{os.sep}profile.py",f"{root}assets{os.sep}profile.py")
            if os.path.exists(f"{temporaryFolder}{os.sep}assets{os.sep}.history"): fs.copyFile(f"{temporaryFolder}{os.sep}assets{os.sep}.history",f"{root}assets{os.sep}.history")
            # UnBackup Folders
            for Folder in FoldersToBackup:
                if os.path.exists(f"{temporaryFolder}{os.sep}{Folder}"):
                    fs.copyFolder2(f"{temporaryFolder}{os.sep}{Folder}",f"{root}{Folder}")
            print("Done reverting!")
            print("Traceback:")
            print(f"\033[31m{ traceback.format_exc() }\033[0m")
            if input("The /.temp folder still exists and contains the backup data incase reverting didn't work, do you want to remove it? [Y/N] ").lower() == "Y": shutil.rmtree(temporaryFolder)