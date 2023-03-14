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
from assets.lib.tabledraw import drawTable

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
def matchPackage(mainRepoFile,repoFolder,pack_name,pack_version,pack_repo,localFormatVersion,ignoreFormat):
    #TODO if package found in locals show info and ask user to choose one by writing a number (1,2.. depending on amount of packages) use tabledraw, this list will also include official repo data. otherwise check if in normal repository and if not say message to user.
    #TODO then if no versio is given as argument show al avaliable versions in the selected repository and ask user to choose.
    #TODO return source data
    # Split name
    split = pack_name.split(".")
    if len(split) > 2:
        pack_repo = split[0]
        author = split[1]
        name = split[2]
    else:
        author = split[0]
        name = split[1]
    # Main repo data
    mainRepoData = getRepositoryData(mainRepoFile,localFormatVersion,ignoreFormat)
    if mainRepoData == "ERR": exit()
    # Assemble repoFolder Packages
    localPackages = dict()
    for file in os.listdir(repoFolder):
        file = repoFolder + os.sep + file
        content = getRepositoryData(file,localFormatVersion,ignoreFormat)
        if content != "ERR":
            for package in content["Repository"]["Entries"]:
                key = list(package.keys())[0]
                if key == name:
                    package[key]["repoFile"] = file
                    package[key]["repoType"] = "local"
                    if localPackages.get(key) == None: localPackages[key] = list()
                    localPackages[key].append( package[key] )
    # exist at al?
    if name in list(localPackages.keys()):
        findings = localPackages.copy()
        # Add official repository packages
        for package in mainRepoData["Repository"]["Entries"]:
                key = list(package.keys())[0]
                package[key]["repoFile"] = mainRepoFile
                package[key]["repoType"] = "official"
                if findings.get(key) == None: findings[key] = list()
                findings[key].append( package[key] )
        # Amnt exist
        amount = len(findings[name])
        # no repo defined
        if pack_repo != "" and pack_repo != None:
            found = False
            for packageDict in findings[name]:
                repoFileN = os.path.basename(packageDict["repoFile"])
                repoFileN = repoFileN.split(".")[0]
                if repoFileN == pack_repo:
                    choosenRepoData = packageDict
                    found = True
            # If not found return empty results
            if found == False:
                return False,{}
        else:
            if amount > 1 :
                # prep table
                table = dict()
                table["ID"] = list()
                table["Name"] = list()
                table["Author"] = list()
                table["Version"] = list()
                table["RepoType"] = list()
                table["RepoFile"] = list()
                # Populate table
                counter = 1
                for packVer in findings[name]:
                    table["ID"].append( counter )
                    table["Name"].append( name )
                    table["Author"].append( packVer["Author"] )
                    versions = [list(item.keys())[0] for item in packVer["Versions"]]
                    table["Version"].append( ','.join( versions ) )
                    table["RepoType"].append( packVer["repoType"] )
                    repoFileN = os.path.basename(packVer["repoFile"])
                    repoFileN = repoFileN.split(".")[0]
                    table["RepoFile"].append( repoFileN )
                    # increment counter
                    counter = counter + 1
                # Choose one
                print(f"\033[33mThe package '{name}' by '{author}' was found in multiple repositories\033[0m")
                drawTable(table)
                c_id = input("\033[33mWhat repository do you want to use? id: \033[0m")
                # get id
                choosenRepoData = findings[name][int(c_id)-1]
            else:
                choosenRepoData = findings[name][0]
        # Amount of versions?
        versions = [list(item.keys())[0] for item in choosenRepoData["Versions"]]
        amntVersions = len(versions)
        # Version defined
        if pack_version != "" and pack_version != None:
            found = False
            for version in choosenRepoData["Versions"]:
                key = list(version.keys())[0]
                if key.lower() == key.lower():
                    choosenVersion = version
                else:
                    choosenVersion = choosenRepoData["Versions"][0]
            if found == False:
                choosenVersion = choosenRepoData["Versions"][0]
        # Version not defined
        else:
            if amntVersions > 1:
                # prep table
                table = dict()
                table["Version"] = list()
                table["NumVersion"] = list()
                table["Description"] = list()
                # populate table
                for version in choosenRepoData["Versions"]:
                    key = list(version.keys())[0]
                    table["Version"].append( key )
                    table["NumVersion"].append( version[key]["VersionNumerical"] )
                    table["Description"].append( version[key]["Description"] )
                # print table
                drawTable(table)
                c_ver = input(f"\033[33mThere are multiple versions of {name} in the choosen repository, which one do you want to use?\033[0m ")
                versionsLOW = [version.lower() for version in versions]
                if c_ver.lower() in versionsLOW:
                    found = False
                    for version in choosenRepoData["Versions"]:
                        key =  list(version.keys())[0]
                        if key.lower() == c_ver.lower():
                            choosenVersion = version
                            found = True
                    if found == False:
                        choosenVersion = choosenRepoData["Versions"][0]
                else:
                    choosenVersion = choosenRepoData["Versions"][0]
            else:
                choosenVersion = choosenRepoData["Versions"][0]
        return choosenVersion
    # Search default
    else:
        entries = [ list(entry.keys())[0] for entry in mainRepoData["Repository"]["Entries"] ]
        entriesLOW = [ entry.lower() for entry in entries ]
        if name.lower() in entriesLOW:
            print(name)
        else:
            return False,{}
    # Version if the version of the package to match for if not found use latest and inform user
    # check through mainrepo then get al data from al repoFolders note theese should get updated :( then match for al occurences of package name and collect list of al version avaliable throughout al repos. If multiple latest versions are given then ask the user to choose one, showing the url to the repo.
    pass

# Function to handle depedencies
def handleDependencies(deps=dict()):
    pass