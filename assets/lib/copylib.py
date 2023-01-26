import shutil
from assets.utils.utilFuncs import *

def CopyFile(sourcefile=str(),destination=str()):
    shutil.copy2(sourcefile, destination)

def CopyFolder(sourceDirectory=str(),destinationDirectory=str()):
    shutil.copytree(sourceDirectory, destinationDirectory)

def CopyFolder2(sourceDirectory=str(),destinationDirectory=str()):
    entries = scantree(sourceDirectory)
    destinationDirectory = destinationDirectory.replace("\\",os.sep)
    destinationDirectory = destinationDirectory.replace("/",os.sep)
    olddir = os.getcwd()
    splitdir = destinationDirectory.split(os.sep)
    # goto root and remove root from splitdir
    if IsWindows():
        os.chdir(splitdir[0])
        splitdir.pop(0)
    else: os.chdir("/")
    for part in splitdir:
        partPath = os.path.realpath(str(f"{os.getcwd()}{os.sep}{part}"))
        print(partPath)
        try:
            os.chdir(partPath)
        except:
            os.mkdir(partPath)
            os.chdir(partPath)
    os.chdir(olddir)
    #for entrie in entries:
    #    newpath = (entrie.path).replace(sourceDirectory,f"{destinationDirectory}{os.sep}")
    #    newpath = newpath.replace(f"{os.sep}{os.sep}",os.sep)
    #    # Files
    #    if os.path.isfile(entrie.path):
    #        shutil.copy2(entrie.path,newpath)
    #    # Folders
    #    else:
    #        if not os.path.exists(entrie.path): os.mkdir(newpath)