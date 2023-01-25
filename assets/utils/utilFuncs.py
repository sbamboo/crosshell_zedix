# Additional functions for the Zedix crosshell core
# Author: Simon Kalmi Claesson

# [Imports]

from os.path import exists
from os.path import isfile
try:
    from os import scandir
except ImportError:
    from scandir import scandir
from os import access
from os import X_OK

# [Files & Folders]

# Function to test path using os.exists
def testPath(path):
    if exists(path):
        return True
    else:
        return False

# Function to get file content using open().read()
def getContent(filepath):
    return open(filepath, 'r').read()

# Function to write a string to a file using open().write()
def outFile(inputs=str(),filepath=str(),append=False,encoding=None):
    if encoding == None:
        encoding = "utf-8"
    if append == True:
        f = open(filepath, "a", encoding=encoding)
        f.write(inputs)
        f.close()
    else:
        f = open(filepath, "w", encoding=encoding)
        f.write(inputs)
        f.close()
    
# Function to create an empty file using open("x")
def touchFile(filepath,encoding=None):
    if encoding == None:
        encoding = "utf-8"
    if exists(filepath):
        f = open(filepath, "x", encoding=encoding)
        f.close()
    else:
        f = open(filepath, "w", encoding=encoding)
        f.close()

# Function to scantree using scantree()
def scantree(path):
    for entry in scandir(path):
        if entry.is_dir(follow_symlinks=False):
            yield from scantree(entry.path)
        else:
            yield entry

# Function to check if file is executable
def IsExecutable(filepath):
    return isfile(filepath) and access(filepath, X_OK)


# [Readers]
def readConfig(filepath):
    if exists(filepath):
        content = open(filepath, 'r').read().split("\n")
        dataDict = dict()
        for line in content:
            if line.strip()[0] != "#":
                name = line.split("=")[0].strip(" ")
                data = ''.join(line.split("=")[1:(len(line.split("=")))]).strip()
                dataDict[name] = data
        return dataDict
    