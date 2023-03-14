# [Imports]
from assets.lib.tqdm_ui import *
from assets.lib.netwa import simpleDownload
from assets.lib.filesys import filesys as fs
from assets.lib.importa import *
import argparse
import requests
import json
import os

# [Importa imports]
globals().update( fromPathAA(f"{CSScriptRoot}{os.sep}.helperfuncs.py") )

cparser = argparse.ArgumentParser(prog="Packagehand",exit_on_error=False,add_help=False)
cparser.add_argument('-h', '--help', action='store_true', default=False, help='Shows help menu.')
cparser.add_argument('--exhelp', action='store_true', default=False, help='Shows help then exits.')
# Options
cparser.add_argument('-version', dest="package_version", help="The version of the package to install, non-numerical. Ex: LTS or Latest")
cparser.add_argument('-repoOverwrt','-rover', dest="repoOverwrite", help="Your own repository file to load instead of the installed ones.")
cparser.add_argument('-repoVerFile','-rverf', dest="overwriteRepoVerFile", help="The filepath to the overwrite repositories versionInfo file. (VersionCheckFile)")
cparser.add_argument('-repoVerUrl','-rveru', dest="overwriteRepoVerUrl", help="The url to the overwrite repositories versionInfo file. (VersionCheckFile)")
cparser.add_argument('-repoUpdate','-rupd', dest="overwriteRepoUpdate", help="Updates the overwrite repository, must be used with -repoOverwrt and update URL supplied")
# Actions
cparser.add_argument('--install','--add','--a','--i', dest="install", action='store_true', help="Install switch")
cparser.add_argument('--ignoreFormat','--if', dest="ignoreFormat", action='store_true', help="Ignores repository format version")
cparser.add_argument('--skipLocalUpdate','--skiplup', dest="skipLocalUpdate", action='store_true', help="Skips to update the local repositories")
# Package (Comsume al remaining arguments)
cparser.add_argument('package', nargs='*', help="The package id (author.package) ór (author.package.version)")
# Create main arguments object
try: argus = cparser.parse_args(argv)
except: argus = cparser.parse_args()
if argus.help: cparser.print_help()
if argus.exhelp: cparser.print_help(); exit()

# ===============================[Handle repository version]===============================


# [Setup/Declarations]
ph_ProtectedPackages = []
ph_LocalFormatVersion = 1 # The format version this version of packagehand expects
ph_repoURL = "https://github.com/simonkalmiclaesson/packagehand_repository/raw/main/crosshell_zedix/repo.jsonc"
ph_verfURL = "https://github.com/simonkalmiclaesson/packagehand_repository/raw/main/crosshell_zedix/repo.verf"
ph_cacheDir = f"{CSScriptRoot}{os.sep}cached"
ph_repoDir = f"{CSScriptRoot}{os.sep}repos"
ph_repoFile = f"{ph_cacheDir}{os.sep}officialRepo.jsonc"
ph_verfFile = f"{ph_cacheDir}{os.sep}officialRepo.verf"

# [Create missing folders]
if not os.path.exists(ph_cacheDir): os.mkdir(ph_cacheDir)
if not os.path.exists(ph_repoDir): os.mkdir(ph_repoDir)

# [Ensure official repository]
# Check if local repo should be downloaded
if not os.path.exists(ph_repoFile):
    print("Local repo not found, downloading...")
    simpleDownload(ph_repoURL,ph_repoFile)
    if os.path.exists(ph_verfFile): os.remove(ph_verfFile)
    simpleDownload(ph_verfURL,ph_verfFile)
    print("Done!")
# Check if local repo should be updated
else:
    ph_ret = updateRepositoryFile(repoFile=ph_repoFile,versionCheck=True,ignoreFormat=bool(argus.ignoreFormat),skipOnEmptyURL=False,verfFile=ph_verfFile,repoURL=ph_repoURL,verfURL=ph_verfURL,localFormatVersion=ph_LocalFormatVersion)
    if ph_ret == "ERR": exit() # HandleStuff

# ====================================[Handle actions]====================================

# [Update overwrite repo?]
if argus.overwriteRepoUpdate != None and argus.repoOverwrite:
    if argus.overwriteRepoVerFile != None and argus.overwriteRepoVerUrl != None:
        ph_ret = updateRepositoryFile(repoFile=str(argus.customrepofile),versionCheck=True,ignoreFormat=bool(argus.ignoreFormat),skipOnEmptyURL=False,verfFile=str(argus.overwriteRepoVerFile),repoURL=str(argus.updateLocalRepo),verfURL=str(argus.overwriteRepoVerUrl),localFormatVersion=ph_LocalFormatVersion)
    else:
        ph_ret = updateRepositoryFile(repoFile=str(argus.customrepofile),versionCheck=False,ignoreFormat=bool(argus.ignoreFormat),skipOnEmptyURL=False,repoURL=str(argus.updateLocalRepo),localFormatVersion=ph_LocalFormatVersion)
    if ph_ret == "ERR": exit() # HandleStuff

# [Update local repository files]
if argus.skipLocalUpdate == None or argus.skipLocalUpdate == False:
    ph_localRepoFile_shouldVerCheck = False
    ph_localRepoFiles = os.listdir(ph_repoDir)
    ph_lask_vercheck = False
    ph_localVerf_url = None
    for file in ph_localRepoFiles:
        ph_filePath = ph_repoDir + os.sep + file
        # should be verified?
        ph_verfFile = file.split(".")[0] + ".verf"
        ph_verfFile = ph_repoDir + os.sep + ph_verfFile
        if os.path.exists(ph_verfFile):
            # Get verf url
            ph_localVerf_raw = fs.readFromFile(ph_verfFile)
            for line in ph_localVerf_raw.split("\n"):
                if "url." in line:
                    line = line.replace("url.","")
                    ph_localVerf_url = line
            if ph_localVerf_url != None:
                ph_lask_vercheck = True
                ph_lask_verfile = ph_verfFile
        else:
            ph_lask_verfile = None
        ph_ret = updateRepositoryFile(repoFile=ph_filePath,versionCheck=ph_lask_vercheck,skipOnEmptyURL=True,ignoreFormat=False,verfFile=ph_lask_verfile,repoURL=ph_localVerf_url,verfURL=None,localFormatVersion=ph_LocalFormatVersion)
        if ph_ret == "ERR": exit()

# [Get data for official repo]
if argus.repoOverwrite:
    ph_mainRepoData = getRepositoryData(str(argus.repoOverwrite),ph_LocalFormatVersion,ignoreFormat=bool(argus.ignoreFormat))
    if ph_mainRepoData == "ERR": exit()
else:
    ph_mainRepoData = getRepositoryData(ph_repoFile,ph_LocalFormatVersion,ignoreFormat=bool(argus.ignoreFormat))
    if ph_mainRepoData == "ERR": exit()

# [Get package details]
if argus.package:
    # Get package version since it may be an argument or .<version> in package name
    ph_packver = None
    ph_packname = argus.package[0]
    ph_packrepo = None
    if argus.package_version != None: ph_packver = str(argus.package_version)
    ph_packnamePartials = str(ph_packname).split(".")
    # Get list of local repos
    ph_localRepoFiles = os.listdir(ph_repoDir)
    ph_localRepoFiles_2 = list()
    for file in ph_localRepoFiles:
        fname = file.split(".")
        fname.pop(-1)
        fname = '.'.join(fname)
        ph_localRepoFiles_2.append(fname)
    ph_localRepoFiles,ph_localRepoFiles_2 = ph_localRepoFiles_2,None
    # Default repo type
    if argus.repoOverwrite:
        defaultRepoType = "overwriteRepo"
        ph_localRepoFiles.append("overwriteRepo")
    else:
        defaultRepoType = "officialRepo"
        ph_localRepoFiles.append("officialRepo")
    # Repo define
    if ph_packnamePartials[0] in ph_localRepoFiles:
        ph_packrepo = ph_packnamePartials[0]
        ph_packnamePartials.pop(0)
    # Version define
    if len(ph_packnamePartials) >= 3:
        if ph_packver == None: 
            ph_packver = ph_packnamePartials[-1]
        ph_packnamePartials.pop(-1)
        ph_packname = ".".join(ph_packnamePartials)
    # Match packages
    sourcedata = matchPackage(mainRepoFile=ph_repoFile,repoFolder=ph_repoDir,pack_name=ph_packname,pack_version=ph_packver,pack_repo=ph_packrepo,localFormatVersion=ph_LocalFormatVersion,ignoreFormat=bool(argus.ignoreFormat),defaultRepoType=defaultRepoType)
    print(sourcedata)
    #TODO install package from source data using a function to handle diffrent types of source types
    installPackage(packageData=sourcedata)
    #TODO handle dependencies and write package.deps file to package final install
    handleDependencies(deps=sourcedata[list(sourcedata.keys())[0]]["Dependencies"])
    pass