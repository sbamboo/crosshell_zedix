# [Imports]
import os
import json
try:
    import yaml
except:
    os.system("python3 -m pip install pyyaml")
    import yaml
from assets.lib.netwa import simpleDownload
from assets.lib.filesys import filesys as fs

# [Functions]

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
    if ignoreFormat == False and localFormatVersion != formatVer:
        print(f"The format of {repoFileName} ({formatVer}) is incompatible with this version of packagehand, update packagehand or if you are the author of the repo-file update it to format {localFormatVersion}.")
        return ""
    # Get dictionary based on format
    if formatType == "json":
        dictionary = json.loads(reporaw)
    elif formatType == "yaml":
        dictionary = yaml.safe_load(reporaw)
    return dictionary


# Function to download repositoryFile
def downloadRepositoryFile(repoFile=str(), repoURL=str()):
    try:
        if os.path.exists(repoFile): os.remove(repoFile)
        simpleDownload(repoURL,repoFile)
    except:
        print("[Packagehand.helper] Error arised apon download!")
        return 0

# Function to download repositoryIdefFile
def downloadRepositoryIdefFile(idefFile=str(), idefURL=str()):
    try:
        if os.path.exists(idefFile): os.remove(idefFile)
        simpleDownload(idefURL,idefFile)
    except:
        print("[Packagehand.helper] Error arised apon download!")
        return 0


# Function to update a repository
def updateRepositoryFile(repoFile=str(),idefFile=None,repoURL=None,idefURL=None):
    # Check if repo file exists
    if not os.path.exist(repoFile):
        # Check if user given Url
        if repoURL != None:
            simpleDownload(repoURL,repoFile)
            if idefFile != None and idefURL != None:
                simpleDownload(idefURL,idefFile)
        else:
            print("[Packagehand.helper] Error: No repo file found and no repoURL argument passed, no url to download with!")
    # Should be updated
    else:
        # Has idefFile
        if idefFile == None:
            c = input("[Packagehand.helper] No idefFile provided, can't check for updates. Do you want to update anyway? [y/n] ")
            if c.lower() != "y":
                return ""
            else:
                ret = downloadRepositoryFile(repoFile,repoURL)
                if ret == 0: return ""
        elif idefURL == None:
            c = input("[Packagehand.helper] No idefURL provided, can't check for updates. Do you want to update anyway? [y/n] ")
            if c.lower() != "y":
                return ""
            else:
                ret = downloadRepositoryFile(repoFile,repoURL)
                if ret == 0: return ""
        else:
            print("Checking repository version...")
            ph_localIdef_raw = fs.readFromFile(idefFile)
            ph_onlineIdef_raw = simpleDownload(idefURL,"")
            # Get localIdefInfo
            for line in ph_localIdef_raw.split("\n"):
                prop = line.split(".")[0]
                data = line.split(".")[1]
                if prop == "id": ph_localIdef_id = int(data)
            # Get onlineIdefInfo
            for line in ph_onlineIdef_raw.split("\n"):
                prop = line.split(".")[0]
                data = line.split(".")[1]
                if prop == "id": ph_onlineIdef_id = int(data)
            # Compare and update if needed
            if ph_localIdef_id > ph_onlineIdef_id:
                print("Your local repository is newer then the one online, will continue without changes...")
                return ""
            elif ph_localIdef_id < ph_onlineIdef_id:
                print("Your local repository is outdated, downloading the latest one...")
                # check for url in repofile
                if repoURL == None:
                    try:
                        repoURL = getRepositoryData(repoFile=repoFile,ignoreFormat=True)
                    except:
                        print("[Packagehand.helper] Error: No repoURL given as argument and no repo url found in the current version. No repo-url to use!")
                        return ""
                if repoURL == "":
                    print("[Packagehand.helper] Error: No repoURL given as argument and no repo url found in the current version. No repo-url to use!")
                    return ""
                if os.path.exists(idefFile): os.remove(idefFile)
                simpleDownload(idefURL,idefFile)
                ret = downloadRepositoryFile(repoFile,repoURL)
                if ret == 0: return ""
                print("Done!")
            else:
                print("Repository up to date!")



# Function that matches package in multiple repos
def matchPackage(mainRepo,repoFolder,version):
    # Version if the version of the package to match for if not found use latest and inform user
    # check through mainrepo then get al data from al repoFolders note theese should get updated :( then match for al occurences of package name and collect list of al version avaliable throughout al repos. If multiple latest versions are given then ask the user to choose one, showing the url to the repo.
    pass

# Function to handle depedencies
def handleDependencies(deps=dict()):
    pass