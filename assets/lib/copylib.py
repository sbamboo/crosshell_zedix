import shutil

def CopyFile(sourcefile=str(),destination=str()):
    shutil.copy2(sourcefile, destination)

def CopyFolder(sourceDirectory=str(),destinationDirectory=str()):
    shutil.copytree(sourceDirectory, destinationDirectory)