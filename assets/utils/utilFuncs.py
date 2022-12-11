# Additional functions for the Zedix crosshell core
# Author: Simon Kalmi Claesson

from os.path import exists
try:
    from os import scandir
except ImportError:
    from scandir import scandir

# [Files & Folders]

def testPath(path):
    if exists(path):
        return True
    else:
        return False

def getContent(filepath):
    return open(filepath, 'r').read()

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
    
def touchFile(filepath,encoding=None):
    if encoding == None:
        encoding = "utf-8"
    if exists(filepath):
        f = open(filepath, "x", encoding=encoding)
        f.close()
    else:
        f = open(filepath, "w", encoding=encoding)
        f.close()

def scantree(path):
    for entry in scandir(path):
        if entry.is_dir(follow_symlinks=False):
            yield from scantree(entry.path)
        else:
            yield entry


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