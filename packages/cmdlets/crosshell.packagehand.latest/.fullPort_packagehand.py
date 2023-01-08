import argparse

cparser = argparse.ArgumentParser(prog="Packagehand")
# Install
cparser.add_argument('--install','--add','--a', dest="install", action='store_true', help="Install switch")
# Uninstall
cparser.add_argument('--uninstall','--remove','--r', dest="uninstall", action='store_true', help="Remove switch")
# List
cparser.add_argument('--list','--l', dest="list", action='store_true', help="Lists out packages in the repo")
# Get
cparser.add_argument('--get','--g', dest="get", action='store_true', help="Gets installed packages")
# VersionTag
cparser.add_argument('-versiontag','-vtag' dest="versiontag", help="Allowes you to specify a versionTag to install. ('Latest'/'LTS')")
# Misc
cparser.add_argument('--force' dest="force", action='store_true', help="Forces installation of a package")
cparser.add_argument('--meta','--shmeta', dest="shmeta", action='store_true', help="Shows meta")
cparser.add_argument('--ar','--reload','--autoreload', dest="autoreload", action='store_true', help="Automaticly reloads crosshell post install")
cparser.add_argument('--showiwrprogress','--showrequestprogress', dest="showiwrprogress", action='store_true', help="Shows the progress of iwr")
cparser.add_argument('--shownonmetas', dest="shownonmetas", action='store_true', help="Show packages without meta")
cparser.add_argument('--grepo','--rr','--rrepo','--reloadrepo', dest="reloadrepo", action="store_true", help="Reload the repository automaticly.")
cparser.add_argument('--o','--overlap', dest="overlap", action='store_true', help="Allowes overlap installations")
cparser.add_argument('-s','-search', dest="search", help="Allowes you to filter stuff by a searchTerm")
cparser.add_argument('--handle_protected_packages', dest="handle_protected_packages", help="Allowes you to handle protected packages")
# Package (Comsume al remaining arguments)
cparser.add_argument('-package','-p', nargs='*', dest="package", help="The package id")
# Create main arguments object
argus = cparser.parse_args(argv)

print(argus)