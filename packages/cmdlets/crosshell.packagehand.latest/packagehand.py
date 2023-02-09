# [Imports]
from assets.lib.tqdm_ui import *
from assets.lib.netwa import simpleDownload
from assets.lib.filesys import filesys as fs
import assets.lib.importa as im
import argparse
import requests
import json
import os

# [Importa imports]
hf = im.fromPath(f"{CSScriptRoot}\.helperfuncs.py")

cparser = argparse.ArgumentParser(prog="Packagehand",exit_on_error=False,add_help=False)
cparser.add_argument('-h', '--help', action='store_true', default=False, help='Shows help menu.')
cparser.add_argument('--exhelp', action='store_true', default=False, help='Shows help then exits.')
# Options
cparser.add_argument('-repofile', dest="customrepofile", help="Your own repository file to load instead of the installed ones.")
cparser.add_argument('-version', dest="packge_version", help="The version of the package to install, non-numerical. Ex: LTS or Latest")
# Actions
cparser.add_argument('--install','--add','--a', dest="install", action='store_true', help="Install switch")
# Package (Comsume al remaining arguments)
cparser.add_argument('package', nargs='*', help="The package id (author.package)")
# Create main arguments object
try: argus = cparser.parse_args(argv)
except: argus = cparser.parse_args()
if argus.help: cparser.print_help()
if argus.exhelp: cparser.print_help(); exit()

# ===============================[Handle repository version]===============================


# [Setup/Declarations]
ph_LocalFormatVersion = 1 # The format version this version of packagehand expects
ph_repoURL = "https://github.com/simonkalmiclaesson/packagehand_repository/raw/main/crosshell_zedix/repo.jsonc"
ph_idefURL = "https://github.com/simonkalmiclaesson/packagehand_repository/raw/main/crosshell_zedix/repo.idef"
ph_repoFile = f"{CSScriptRoot}{os.sep}localrepo.jsonc"
ph_idefFile = f"{CSScriptRoot}{os.sep}localrepo.idef"
ph_repoDir = f"{CSScriptRoot}{os.sep}repos"

# [Handle official repository]
# Check if local repo should be downloaded
if not os.path.exists(ph_repoFile):
    print("Local repo not found, downloading...")
    simpleDownload(ph_repoURL,ph_repoFile)
    if os.path.exists(ph_idefFile): os.remove(ph_idefFile)
    simpleDownload(ph_idefURL,ph_idefFile)
    print("Done!")
# Check if local repo should be updated
else:
    ret = updateRepositoryFile(repoFile=ph_repoFile,idefFile=ph_idefFile,repoURL=ph_repoURL,idefURL=ph_idefURL)
    if ret == "": exit()

# ====================================[Handle actions]====================================

# [Get data for official repo]
if argus.customrepofile:
    ph_mainRepoData = getRepositoryData(str(argus.customrepofile),ph_LocalFormatVersion)
    if ph_mainRepoData == "": exit()
else:
    ph_mainRepoData = getRepositoryData(ph_repoFile,ph_LocalFormatVersion)
    if ph_mainRepoData == "": exit()


# [Get package details]
if argus.package:
    ph_repodata = 