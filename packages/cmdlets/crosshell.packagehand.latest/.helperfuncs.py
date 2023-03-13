# [EnsurePIPPack]
import os
from assets.lib.importa import *
globals().update( fromPathAA(f"{os.path.dirname(__file__)}{os.sep}.ensurePIPPack.py") )

# [Imports]
import re
import json
try:
    import yaml
except:
    ensurePipPack("python3","pyyaml")
    import yaml
from assets.lib.netwa import simpleDownload
from assets.lib.filesys import filesys as fs

# [Functions]

# Function to strip comments out of json
def remove_comments(json_string):
    # Match and remove single-line comments that start with //
    pattern = r"(^|\s)//.*$"
    without_comments = re.sub(pattern, "", json_string, flags=re.MULTILINE)
    return without_comments

# Function to get repositorydata
def getRepositoryData(repoFile=str(),localFormatVersion=int(),ignoreFormat=False):
    reporaw = fs.readFromFile(repoFile)
    repoFileName = os.path.basename(repoFile)
    # get format info
    repoformat = (reporaw.split("[SB]")[1]).split("[EB]")[0]
    formatType = repoformat.split(".")[0]
    formatType = formatType.lower()
    formatVer = repoformat.split(".")[1]
    # Check for format incompat
    if ignoreFormat == False and localFormatVersion != int(formatVer):
        print(f"\033[31mThe format of {repoFileName} ({formatVer}) is incompatible with this version of packagehand, update packagehand or if you are the author of the repo-file update it to format {localFormatVersion}.\033[0m")
        return "ERR"
    # Get dictionary based on format
    reporaw = remove_comments(reporaw)
    if formatType == "json":
        dictionary = json.loads(reporaw)
    elif formatType == "yaml":
        dictionary = yaml.safe_load(reporaw)
    return dictionary


# Function to download repositoryFile
def downloadRepositoryFile(repoFile=str(), repoURL=str(),ignoreFormat=False):
    # check for url in repofile
    if repoURL == None or repoURL == "":
        if os.path.exists(repoFile):
            # Get data
            repoData = getRepositoryData(repoFile=repoFile,ignoreFormat=ignoreFormat)
            if repoData == "ERR": return "ERR"
            # Get url
            repoData = getRepositoryData(repoFile=repoFile,ignoreFormat=False)
            repoURL = repoData["Repository"]["Meta"].get("RepositoryUrl")
            if repoURL == None:
                print("\033[31m[Packagehand.helper] Error: No repoURL given as argument and no repo url found in the current version. No repo-url to use!\033[0m")
                return "ERR"
        else:
            print("\033[31m[Packagehand.helper] Error: No repoURL given as argument and no repo file found localy. No repo-url to use!\033[0m")
            return "ERR"
    # Download
    try:
        tmp = simpleDownload(repoURL,"").decode()
        if os.path.exists(repoFile): os.remove(repoFile)
        fs.writeToFile(inputs=tmp,filepath=repoFile,autocreate=True)
    except:
        print("\033[31m[Packagehand.helper] Error arised apon download!\033[0m")
        return "ERR"

# Function to download repositoryIdefFile
def downloadRepositoryIdefFile(idefFile=str(), idefURL=str()):
    try:
        if os.path.exists(idefFile): os.remove(idefFile)
        simpleDownload(idefURL,idefFile)
    except:
        print("\033[31m[Packagehand.helper] Error arised apon download!\033[0m")
        return "ERR"


# Function to update a repository
def updateRepositoryFile(repoFile=str(),identify=bool(),ignoreFormat=False,idefFile=None,repoURL=None,idefURL=None):
    # Check if repo file exists
    if not os.path.exists(repoFile):
        # Check if user given Url
        if repoURL != None:
            simpleDownload(repoURL,repoFile)
            if identify == True:
                if idefFile != None and idefURL != None:
                    simpleDownload(idefURL,idefFile)
        else:
            print("\033[31m[Packagehand.helper] Error: No repo file found and no repoURL argument passed, no url to download with!\033[0m")
    # Should be updated
    else:
        # Identify
        if identify == True:
            # Has idefFile
            if idefFile == None:
                c = input("\033[33m[Packagehand.helper] No idefFile provided, can't check for updates. Do you want to update anyway? [y/n] \033[0m")
                if c.lower() != "n":
                    return "EXIT"
            elif idefURL == None:
                c = input("\033[33m[Packagehand.helper] No idefURL provided, can't check for updates. Do you want to update anyway? [y/n] \033[0m")
                if c.lower() != "n":
                    return "EXIT"
            # Get Id info
            ph_localIdef_id = "Unknown"
            ph_localIdef_ver = -2
            print("Checking repository version...")
            ph_localIdef_raw = fs.readFromFile(idefFile)
            ph_onlineIdef_raw = simpleDownload(idefURL,"").decode()
            # Get localIdefInfo
            for line in ph_localIdef_raw.split("\n"):
                prop = line.split(".")[0]
                data = line.split(".")[1]
                if prop == "id": ph_localIdef_id = str(data)
                elif prop == "version": ph_localIdef_ver = int(data)
            # Get onlineIdefInfo
            for line in ph_onlineIdef_raw.split("\n"):
                prop = line.split(".")[0]
                data = line.split(".")[1]
                if prop == "id": ph_onlineIdef_id = str(data)
                elif prop == "version": ph_onlineIdef_ver = int(data)
            # Compare and update if needed
            if ph_localIdef_ver > ph_onlineIdef_ver:
                print("Your local repository is newer then the one online, will continue without changes...")
                return "EXIT"
            elif ph_localIdef_ver < ph_onlineIdef_ver:
                print("Your local repository is outdated, downloading the latest one...")
            else:
                print("Repository up to date!")
                return "EXIT"
        # Download repofile
        ret = downloadRepositoryFile(repoFile=repoFile,repoURL=repoURL,ignoreFormat=ignoreFormat)
        if ret == "ERR": return "ERR"
        # Update identifier
        if identify == True:
            ret = downloadRepositoryIdefFile(idefFile,idefURL)
            if ret == "ERR": return "ERR"
        # Finish
        print("Done!")

# Function that matches package in multiple repos
def matchPackage(mainRepoFile,repoFolder,version):
    # Version if the version of the package to match for if not found use latest and inform user
    # check through mainrepo then get al data from al repoFolders note theese should get updated :( then match for al occurences of package name and collect list of al version avaliable throughout al repos. If multiple latest versions are given then ask the user to choose one, showing the url to the repo.
    pass

# Function to handle depedencies
def handleDependencies(deps=dict()):
    pass