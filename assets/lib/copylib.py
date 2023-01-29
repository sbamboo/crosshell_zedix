import shutil
from assets.utils.utilFuncs import *

def CopyFile(sourcefile=str(),destination=str()):
    shutil.copy2(sourcefile, destination)

def CopyFolder(sourceDirectory=str(),destinationDirectory=str()):
    shutil.copytree(sourceDirectory, destinationDirectory)

def CopyFolder2(sourceDirectory=str(),destinationDirectory=str(),debug=False):
    # Get files and folders in source that should be copied.
    entries = scantree(sourceDirectory)
    # Make sure that the destination directory only contains os.sep characters.
    destinationDirectory = destinationDirectory.replace("\\",os.sep)
    destinationDirectory = destinationDirectory.replace("/",os.sep)
    # Save the old working directory
    olddir = os.getcwd()
    # DEBUG
    if debug: print(f"Copying from '{sourceDirectory}' to '{destinationDirectory}' and was working in '{olddir}'\n\n")
    # Loop through al the files/folders that should be copied
    for entrie in entries:
        # Create the path to the file/folder in the source.
        newpath = (entrie.path).replace(sourceDirectory,f"{destinationDirectory}{os.sep}")
        newpath = newpath.replace(f"{os.sep}{os.sep}",os.sep)
        folderpath = newpath
        # If the source is a file then remove it from the path to make sure that al folders can be created before copying the file.
        if os.path.isfile(entrie.path):
            folderpath = os.path.dirname(folderpath)
        # Make sure al the folders in the path exists
        splitdir = folderpath.split(os.sep)
        # goto root and remove root from splitdir
        if IsWindows():
            if splitdir[0][-1] != "\\": splitdir[0] = splitdir[0] + '\\'
            os.chdir(splitdir[0])
            splitdir.pop(0)
        else: os.chdir("/")
        # DEBUG
        if debug: print(f"Working on '{entrie.path}' with new directory of '{folderpath}' and type-data 'IsFile:{os.path.isfile(entrie.path)}' and splitdir '{splitdir}'\n")
        # Iterate over the files
        for part in splitdir:
            partPath = os.path.realpath(str(f"{os.getcwd()}{os.sep}{part}"))
            try:
                os.chdir(partPath)
                # DEBUG
                if debug: print(f"{entrie.name}: 'Working on path partial '{part}'")
            except:
                os.mkdir(partPath)
                os.chdir(partPath)
                # DEBUG
                if debug: print(f"{entrie.name}: 'Needed to create path partial '{part}'")
        # If the source was a file copy it
        if os.path.isfile(entrie.path):
            shutil.copy2(entrie.path,newpath)
            # DEBUG
            if debug: print(f"Copied file '{entrie.path}'")
        # DEBUG
        if debug: print("\n\n")
    os.chdir(olddir)

