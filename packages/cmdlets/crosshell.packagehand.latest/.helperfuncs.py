# [EnsurePIPPack]
import os
from assets.lib.importa import *
globals().update( fromPathAA(f"{os.path.dirname(__file__)}{os.sep}.ensurePIPPack.py") )

# [Imports]
import platform
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

# Function to download repositoryVerfFile
def downloadRepositoryVerfFile(verfFile=str(), verfURL=str()):
    try:
        if os.path.exists(verfFile): os.remove(verfFile)
        simpleDownload(verfURL,verfFile)
    except:
        print("\033[31m[Packagehand.helper] Error arised apon downloading verf file!\033[0m")
        return "ERR"


# Function to update a repository
def updateRepositoryFile(repoFile=str(),versionCheck=bool(),skipOnEmptyURL=False,ignoreFormat=False,verfFile=None,repoURL=None,verfURL=None,localFormatVersion=None):
    repoName = os.path.basename(repoFile)
    # Check if repo file exists
    if not os.path.exists(repoFile):
        # Skip update on empty URL?
        if skipOnEmptyURL == True and repoURL == "": return "EXIT"
        # Check if user given Url
        if repoURL != None:
            simpleDownload(repoURL,repoFile)
            # Download verf file if needed
            if versionCheck == True:
                if verfFile != None and verfURL != None:
                    if os.path.exists(verfFile): os.remove(verfFile)
                    simpleDownload(verfURL,verfFile)
        else:
            print("\033[31m[Packagehand.helper] Error: No repo file found and no repoURL argument passed, no url to download with!\033[0m")
            return "EXIT"
    # Should be updated
    else:
        # VersionCheck
        if versionCheck == True:
            # Has verfFile
            if verfFile == None:
                c = input("\033[33m[Packagehand.helper] No verfFile provided, can't check for updates. Do you want to update anyway? [y/n] \033[0m")
                if c.lower() == "n":
                    return "EXIT"
            elif verfURL == None:
                c = input("\033[33m[Packagehand.helper] No verfURL provided, can't check for updates. Do you want to update anyway? [y/n] \033[0m")
                if c.lower() == "n":
                    return "EXIT"
            # Get Id info
            ph_localVerf_id = "Unknown"
            ph_localVerf_ver = -2
            print("\033[33mChecking repository version...\033[0m")
            ph_localVerf_raw = fs.readFromFile(verfFile)
            ph_onlineVerf_raw = simpleDownload(verfURL,"").decode()
            # Get localVerfInfo
            for line in ph_localVerf_raw.split("\n"):
                prop = line.split(".")[0]
                data = line.split(".")[1]
                if prop == "id": ph_localVerf_id = str(data)
                elif prop == "version": ph_localVerf_ver = int(data)
            # Get onlineVerfInfo
            for line in ph_onlineVerf_raw.split("\n"):
                if line != "":
                    prop = line.split(".")[0]
                    data = line.split(".")[1]
                    if prop == "id": ph_onlineVerf_id = str(data)
                    elif prop == "version": ph_onlineVerf_ver = int(data)
            # Compare and update if needed
            ph_localVerf_id = (ph_localVerf_id.lower()).strip()
            ph_onlineVerf_id = (ph_onlineVerf_id.lower()).strip()
            if ph_localVerf_id != ph_onlineVerf_id:
                c = input("\033[33mYour local repository's id dosen't match the one in the versionFile, can't check for updates. Do you want to update anyway? [y/n] \033[0m")
                if c.lower() == "n":
                    return "EXIT"
            if ph_localVerf_ver > ph_onlineVerf_ver:
                print("Your local repository is newer then the one online, will continue without changes...")
                return "EXIT"
            elif ph_localVerf_ver < ph_onlineVerf_ver:
                print("Your local repository is outdated, downloading the latest one...")
            else:
                print(f"\033[34mRepository {repoName} up to date!\033[0m")
                return "EXIT"
        # Retrive repoURL
        if repoURL == None:
            content = getRepositoryData(repoFile=repoFile,localFormatVersion=localFormatVersion,ignoreFormat=True)
            repoURL = content["Repository"]["Meta"]["RepositoryUrl"]
        # Skip update on empty URL?
        if skipOnEmptyURL == True and repoURL == "": pass
        else:
            # Download repofile
            ret = downloadRepositoryFile(repoFile=repoFile,repoURL=repoURL,ignoreFormat=ignoreFormat)
            if ret == "ERR": return "ERR"
            # Update identifier
            if versionCheck == True:
                ret = downloadRepositoryVerfFile(verfFile,verfURL)
                if ret == "ERR": return "ERR"
        # Finish
        print(f"\033[32mUpdated {repoName}!\033[0m")
        return "DONE"

# Function that matches package in multiple repos
def matchPackage(mainRepoFile,repoFolder,pack_name,pack_version,pack_repo,localFormatVersion,ignoreFormat,defaultRepoType):
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
                package[key]["repoType"] = defaultRepoType
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
                try:
                    choosenRepoData = findings[name][int(c_id)-1]
                except:
                    choosenRepoData = findings[name][0]
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
                if pack_version.lower() == key.lower():
                    found = True
                    choosenVersion = version
            if found == False:
                print(f"\033[33mThe version '{pack_version}' was not found under '{list(choosenRepoData.keys())[0]}' so defaulting to 'Latest'\033[0m")
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
        return True,choosenVersion
    # Search default
    else:
        entries = [ list(entry.keys())[0] for entry in mainRepoData["Repository"]["Entries"] ]
        entriesLOW = [ entry.lower() for entry in entries ]
        if name.lower() in entriesLOW:
            found = False
            for package in mainRepoData["Repository"]["Entries"]:
                key = list(package.keys())[0]
                if key.lower() == name.lower():
                    choosenRepoData = package[name]
                    found = True
            if found == False:
                choosenRepoData = mainRepoData["Repository"]["Entries"][0][name]
            # Amount of versions?
            versions = [list(item.keys())[0] for item in choosenRepoData["Versions"]]
            amntVersions = len(versions)
            # Version defined
            if pack_version != "" and pack_version != None:
                found = False
                for version in choosenRepoData["Versions"]:
                    key = list(version.keys())[0]
                    if pack_version.lower() == key.lower():
                        found = True
                        choosenVersion = version
                if found == False:
                    print(f"\033[33mThe version '{pack_version}' was not found under '{list(choosenRepoData.keys())[0]}' so defaulting to 'Latest'\033[0m")
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
            return True,choosenVersion
        else:
            print(f"\033[31mPackage '{name}' not found in officialRepo!\033[0m")
            return False,{}

# Function to handle depedencies
def handleDependencies(deps=dict(),destinationFolder=str()):
    for depedency in deps:
        # Parse
        _type = depedency["Type"]
        _source = depedency["Source"]
        # Inform
        _sourceName = _source.split(" ")[0]
        print(f"[\033[96mph.DepMan\033[0m]: \033[33mInstalling depencency '{_sourceName}' of type '{_type}'...\033[0m")
        # PipPackage
        if _type == "pipinstall":
            try:
                ensurePipPack("python3",_source)
                print(f"[\033[96mph.DepMan\033[0m]: \033[32mInstalled depencency '{_sourceName}'!\033[0m")
            except:
                print(f"[\033[96mph.DepMan\033[0m]: \033[31mInstallation of '{_sourceName}' failed!\033[0m")
        # Package
        elif _type == "package":
            print(f"[\033[96mph.DepMan\033[0m]: \033[31mSkipped install of '{_sourceName}', dependency type not implemented!\033[0m")
    # Print deps to destinationFolder
    depsFile = destinationFolder + os.sep + "deps.json"
    with open(depsFile, "w") as outfile:
        json.dump(deps, outfile)

# Function to get platformType
def getPlatformType():
    platformv = platform.system()
    if platformv == "Linux":
        return "lnx"
    elif platformv == "Darwin":
        return "mac"
    elif platformv == "Windows":
        return "win"
    else:
        return "unknown"

# Function to rename a package file
def renamePackageFile(filepath=str(),fileending=str()):
    # package
    if fileending.lower() == "package":
        oldname = os.path.basename(filepath)
        newname_s = oldname.split(".")
        newname_s.pop(-1)
        newname = '.'.join(newname_s) + ".zip"
        newFilepath = filepath.rstrip(oldname)
        newFilepath = newFilepath + newname
    else:
        newFilepath = filepath
    return newFilepath

# Function to install a package
def package_install(packageData=dict(),packAuthor=str(),packName=str(),baseFolder=str()):
    # Get data
    _verName = list(packageData.keys())[0]
    _verNumerical = packageData[_verName]["VersionNumerical"]
    _verDesc = packageData[_verName]["Description"]
    _verSources = packageData[_verName]["Sources"]
    _osPlatform = getPlatformType()
    # Choose platform
    _verSelectedSource = None
    for index,source in enumerate(_verSources):
        _sourcePlatforms = source["Platform"]
        _sourcePlatforms = [platform.lower() for platform in _sourcePlatforms] # lowercase sourcePlatforms
        if "global" in _sourcePlatforms:
            _verSelectedSource = _verSources[index]
        elif _osPlatform in _sourcePlatforms:
            _verSelectedSource = _verSources[index]
    # no found
    if _verSelectedSource == None:
        print(f"\033[31mNo sources of '{packName}.{_verName}' matches your platform '{_osPlatform}', Install aborted!\033[0m")
        return "EXIT"
    # Get more info
    _sourcePlatforms = _verSelectedSource["Platform"]
    _sourceType = _verSelectedSource["Type"]
    _sourceDotted = _verSelectedSource["Dotted"]
    _sourceFileFormat = _verSelectedSource["FileFormat"]
    _sourceSource = _verSelectedSource["Source"]
    _sourceOverwrite_main = _verSelectedSource["Overwrites"]["PropMainFile"]
    _sourceOverwrite_prop = _verSelectedSource["Overwrites"]["Properties"]
    _sourceOverwrite_wfen = _verSelectedSource["Overwrites"]["WrapperFileEnding"]
    _sourceOverwrite_wrap = _verSelectedSource["Overwrites"]["WrapperScript"]
    # Install based on type
    # UrlPackage
    if _sourceType.lower() == "urlpackage":
        # prep
        destinationFolder = baseFolder + os.sep + packAuthor + "." + packName
        # Check if already exist
        if os.path.exists(destinationFolder):
            print(f"\033[31mA package with name '{packName}' from '{packAuthor}' already seems to be installed, please uninstall it or update it instead!\033[0m")
            return "EXIT"
        # Create folder
        fs.createDir(folderpath=destinationFolder)
        # Download source
        destinationFile = destinationFolder + os.sep + os.path.basename(_sourceSource)
        simpleDownload(_sourceSource,destinationFile)
        # Rename source file
        renamedFile = renamePackageFile(filepath=destinationFile,fileending=_sourceFileFormat)
        fs.renameFile(destinationFile,renamedFile)
        # Unpack the file
        if _sourceDotted == "True" or _sourceDotted == True:
            destinationFolder_dotted = destinationFolder + os.sep + ".dotted"
            fs.createDir(folderpath=destinationFolder_dotted)
            fs.unArchive(archiveFile=renamedFile,destination=destinationFolder_dotted)
        else:
            fs.unArchive(archiveFile=renamedFile,destination=destinationFolder)
        # Handle overwrites
        if _sourceOverwrite_prop != "":
            _propFilePath = destinationFolder + os.sep + _sourceOverwrite_main + ".cfg"
            fs.writeToFile(inputs=_sourceOverwrite_prop,filepath=_propFilePath, append=False, encoding=None, autocreate=True)
        if _sourceOverwrite_wrap != "":
            _wrapFilePath = destinationFolder + os.sep + ".wrapper." + _sourceOverwrite_wfen
            fs.writeToFile(inputs=_sourceOverwrite_wrap,filepath=_wrapFilePath, append=False, encoding=None, autocreate=True)
        # write down packageDataJson
        dataFile = destinationFolder + os.sep + "package.json"
        with open(dataFile, "w") as outfile:
            json.dump(packageData, outfile)
        # Return destinationFolder
        return destinationFolder
    # UrlSourceArchive
    elif _sourceType.lower() == "urlsourcearchive":
        # prep
        destinationFolder = baseFolder + os.sep + packAuthor + "." + packName
        # Check if already exist
        if os.path.exists(destinationFolder):
            print(f"\033[31mA package with name '{packName}' from '{packAuthor}' already seems to be installed, please uninstall it or update it instead!\033[0m")
            return "EXIT"
        # Create folder
        fs.createDir(folderpath=destinationFolder)
        # Download source
        destinationFile = destinationFolder + os.sep + os.path.basename(_sourceSource)
        simpleDownload(_sourceSource,destinationFile)
        # Rename source file
        renamedFile = renamePackageFile(filepath=destinationFile,fileending=_sourceFileFormat)
        fs.renameFile(destinationFile,renamedFile)
        # Unpack the file
        destinationFolder_dotted = None
        if _sourceDotted == "True" or _sourceDotted == True:
            destinationFolder_dotted = destinationFolder + os.sep + ".dotted"
            fs.createDir(folderpath=destinationFolder_dotted)
            fs.unArchive(archiveFile=renamedFile,destination=destinationFolder_dotted)
        else:
            fs.unArchive(archiveFile=renamedFile,destination=destinationFolder)
        # Handle overwrites
        if _sourceOverwrite_prop != "":
            _propFilePath = destinationFolder + os.sep + _sourceOverwrite_main + ".cfg"
            fs.writeToFile(inputs=_sourceOverwrite_prop,filepath=_propFilePath, append=False, encoding=None, autocreate=True)
        if _sourceOverwrite_wrap != "":
            _wrapFilePath = destinationFolder + os.sep + ".wrapper." + _sourceOverwrite_wfen
            fs.writeToFile(inputs=_sourceOverwrite_wrap,filepath=_wrapFilePath, append=False, encoding=None, autocreate=True)
        # Run phbuild.py
        if destinationFolder_dotted != None:
            _phbuildFile = destinationFolder_dotted + os.sep + "phbuild.py"
        else:
            _phbuildFile = destinationFolder + os.sep + "phbuild.py"
        sentVars = {
            "ph_verName": _verName,
            "ph_verNumerical": _verNumerical,
            "ph_verDescription": _verDesc,
            "ph_verSources": _verSources,
            "ph_osPlatform": _osPlatform,
            "ph_verSelectedSource": _verSelectedSource,
            "ph_sourcePlatforms": _sourcePlatforms,
            "ph_sourceType": _sourceType,
            "ph_sourceDotted": _sourceDotted,
            "ph_sourceFileFormat": _sourceFileFormat,
            "ph_sourceSource": _sourceSource,
            "ph_sourceOverwrite_main": _sourceOverwrite_main,
            "ph_sourceOverwrite_prop": _sourceOverwrite_prop,
            "ph_sourceOverwrite_wfen": _sourceOverwrite_wfen,
            "pg_sourceOverwrite_wrap": _sourceOverwrite_wrap
        }
        exec(open(_phbuildFile,'r').open(),sentVars)
        # write down packageDataJson
        dataFile = destinationFolder + os.sep + "package.json"
        with open(dataFile, "w") as outfile:
            json.dump(packageData, outfile)
        # Return destinationFolder
        return destinationFolder
    # UrlSourceFile
    elif _sourceType.lower() == "urlsourcefile":
        # prep
        destinationFolder = baseFolder + os.sep + packAuthor + "." + packName
        # Check if already exist
        if os.path.exists(destinationFolder):
            print(f"\033[31mA package with name '{packName}' from '{packAuthor}' already seems to be installed, please uninstall it or update it instead!\033[0m")
            return "EXIT"
        # Create folder
        fs.createDir(folderpath=destinationFolder)
        # Download source
        destinationFile = destinationFolder + os.sep + os.path.basename(_sourceSource)
        simpleDownload(_sourceSource,destinationFile)
        # Handle overwrites
        if _sourceOverwrite_prop != "":
            _propFilePath = destinationFolder + os.sep + _sourceOverwrite_main + ".cfg"
            fs.writeToFile(inputs=_sourceOverwrite_prop,filepath=_propFilePath, append=False, encoding=None, autocreate=True)
        if _sourceOverwrite_wrap != "":
            _wrapFilePath = destinationFolder + os.sep + ".wrapper." + _sourceOverwrite_wfen
            fs.writeToFile(inputs=_sourceOverwrite_wrap,filepath=_wrapFilePath, append=False, encoding=None, autocreate=True)
        # write down packageDataJson
        dataFile = destinationFolder + os.sep + "package.json"
        with open(dataFile, "w") as outfile:
            json.dump(packageData, outfile)
        # Return destinationFolder
        return destinationFolder
