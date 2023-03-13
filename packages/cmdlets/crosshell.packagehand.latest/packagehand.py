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
cparser.add_argument('-repofile', dest="customrepofile", help="Your own repository file to load instead of the installed ones.")
cparser.add_argument('-version', dest="package_version", help="The version of the package to install, non-numerical. Ex: LTS or Latest")
# Actions
cparser.add_argument('--install','--add','--a','--i', dest="install", action='store_true', help="Install switch")
cparser.add_argument('--ignoreFormat','--if', dest="ignoreFormat", action='store_true', help="Ignores repository format version")
cparser.add_argument('-updateLocalRepo','-uprep', dest="updateLocalRepo", help="Updates the local repository, must be used with -repofile and supply update URL")
cparser.add_argument('-repoIdef','-ridef', dest="customrepoIdefFile", help="The filepath to the custom repositories identifier file.")
cparser.add_argument('-repoIdefURL','-rideu', dest="customrepoIdefUrl", help="The url to the custom repositories identifier file.")
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
ph_idefURL = "https://github.com/simonkalmiclaesson/packagehand_repository/raw/main/crosshell_zedix/repo.idef"
ph_cacheDir = f"{CSScriptRoot}{os.sep}cached"
ph_repoDir = f"{CSScriptRoot}{os.sep}repos"
ph_repoFile = f"{ph_cacheDir}{os.sep}officialRepo.jsonc"
ph_idefFile = f"{ph_cacheDir}{os.sep}officialRepo.idef"

# [Create missing folders]
if not os.path.exists(ph_cacheDir): os.mkdir(ph_cacheDir)
if not os.path.exists(ph_repoDir): os.mkdir(ph_repoDir)

# [Ensure official repository]
# Check if local repo should be downloaded
if not os.path.exists(ph_repoFile):
    print("Local repo not found, downloading...")
    simpleDownload(ph_repoURL,ph_repoFile)
    if os.path.exists(ph_idefFile): os.remove(ph_idefFile)
    simpleDownload(ph_idefURL,ph_idefFile)
    print("Done!")
# Check if local repo should be updated
else:
    ph_ret = updateRepositoryFile(repoFile=ph_repoFile,identify=True,ignoreFormat=bool(argus.ignoreFormat),idefFile=ph_idefFile,repoURL=ph_repoURL,idefURL=ph_idefURL)
    if ph_ret == "ERR": exit() # HandleStuff

# ====================================[Handle actions]====================================

# [Update local file?]
if argus.updateLocalRepo != None and argus.customrepofile:
    if argus.customrepoIdefFile != None and argus.customrepoIdefUrl != None:
        ph_ret = updateRepositoryFile(repoFile=str(argus.customrepofile),identify=True,ignoreFormat=bool(argus.ignoreFormat),idefFile=str(argus.customrepoIdefFile),repoURL=str(argus.updateLocalRepo),idefURL=str(argus.customrepoIdefUrl))
    else:
        ph_ret = updateRepositoryFile(repoFile=str(argus.customrepofile),identify=False,ignoreFormat=bool(argus.ignoreFormat),repoURL=str(argus.updateLocalRepo))
    if ph_ret == "ERR": exit() # HandleStuff

# [Get data for official repo]
if argus.customrepofile:
    ph_mainRepoData = getRepositoryData(str(argus.customrepofile),ph_LocalFormatVersion,ignoreFormat=bool(argus.ignoreFormat))
    if ph_mainRepoData == "ERR": exit()
else:
    ph_mainRepoData = getRepositoryData(ph_repoFile,ph_LocalFormatVersion,ignoreFormat=bool(argus.ignoreFormat))
    if ph_mainRepoData == "ERR": exit()

# [Get package details]
if argus.package:
    # Get package version since it may be an argument or .<version> in package name
    ph_packver = "Latest"
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
    sourcedata = matchPackage(mainRepoFile=ph_repoFile,repoFolder=ph_repoDir,name=ph_packname,version=ph_packver,repo=ph_packrepo,localFormatVersion=ph_LocalFormatVersion,ignoreFormat=bool(argus.ignoreFormat))
    #TODO handle dependencies
    #TODO install package from source data using a function to handle diffrent types of source types
    pass