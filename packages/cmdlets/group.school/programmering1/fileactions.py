# Imports
import os

# Class containing functions
class fileactions():

    encoding = "utf-8"

    # Function to create file
    def createFile(filepath=(), overwrite=False, encoding=None):
        if encoding != None: encoding = fileactions.encoding
        if not os.path.exists(filepath):
            f = open(filepath, "w", encoding=encoding)
            f.close()
        else:
            if overwrite == False:
                print("File already exists, set overwrite to true to overwrite it.")
            else:
                f = open(filepath, "x", encoding=encoding)
                f.close()
    
    # Function to create directory
    def createDir(folderpath=()):
        if not os.path.exists(folderpath):
            os.mkdir(folderpath)
        else:
            return "Directory already exists."
    
    # Function to delete a file
    def deleteFile(filepath=str()):
        if os.path.exists(filepath): return "File does not exist."
        if os.path.isfile(filepath):
            os.remove(filepath)
        else:
            return "Obj is directory."

    # Function to delete directory
    def deleteDir(folderpath=str()):
        if os.path.exists(folderpath): return "Directory does not exist."
        if os.path.isdir(folderpath):
            os.rmdir(folderpath)
        else:
            return "Obj is file."

    # Function to write to a file
    def writeToFile(inputs=str(),filepath=str(), append=False, encoding=None):
        if encoding != None: encoding = fileactions.encoding
        if os.path.exists(filepath): return "File does not exist."
        if os.path.isfile(filepath):
            # Check if function should append
            if append == True:
                f = open(filepath, "a", encoding=encoding)
                f.write(inputs)
                f.close()
            else:
                f = open(filepath, "w", encoding=encoding)
                f.write(inputs)
                f.close()
        else:
            return "Obj is directory."

    # Get file contents from file
    def readFromFile(filepath=str(),encoding=None):
        if encoding != None: encoding = fileactions.encoding
        if os.path.exists(filepath): return "File does not exist."
        if os.path.isfile(filepath):
            return open(filepath, 'r', encoding=encoding).read()
        else:
            return "Obj is not file."
        

# TODO: Add function to handle file problems taking action of "write, read" etc
# TODO: Add try/catch