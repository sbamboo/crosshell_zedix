command = (' '.join(argv)).strip(" ")
command = command.strip('"')
import os

# get path
localp = path
pathlist = os.path.realpath(localp).split(os.sep)
pathlist.pop(-1)
localp = str(os.sep).join(pathlist)
localp.strip(os.sep)
configpath = f"{localp}{os.sep}dir.cfg"
path = open(configpath,"r").read()
path = path.strip("\n")
shellpath = f"{path}{os.sep}shell.ps1"
valid = False
if os.path.exists(path):
    valid = True
if os.path.exists(shellpath):
    valid = True

# Error if invalid
if valid == False:
    npath = ""
    print("\033[31mInvalid path in configuration!\033[0m")
    while (os.path.exists(npath)) == False and npath == "":
        npath = input("Enter new path: ")
        if os.path.exists(npath):
            f = open(configpath, "w")
            f.write(npath)
            f.close()
    path = open(configpath,"r").read()
    path = path.strip("\n")
    shellpath = f"{path}{os.sep}shell.ps1"

# Load
command = str(shellpath) + " -command " + f'"{command}"'
command = command.replace("\|","|")
os.system(f"pwsh -file {command}")

