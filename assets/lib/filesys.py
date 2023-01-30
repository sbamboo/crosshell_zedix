# FileSys: Library to work with filesystems.
# Made by: Simon Kalmi Claesson

# Imports
import os

# Class containing functions
class filesys():

    defaultencoding = "utf-8"

    sep = os.sep

    # Help function
    def help():
        print(f'''
        This class contains functions to perform filessytem actions like creating and removing files/directories.
        Functions included are:
          - help: Shows this help message.
          - errorhandler: Internal function to handle errors. (Taking "action=<str_action>", "path=<str_path>" and "noexist=<bool>"
          - doesExist: Checks if a file/directory exists. (Taking "path=<str>")
          - notExist: Checks if a file/directory does not exist. (Taking "path=<str>")
          - isFile: Checks if a object is a file. (Taking "path=<str>")
          - isDir: Checks if a object is a directory. (Taking "path=<str>")
          - createFile: Creates a file. (Taking "filepath=<str>", "overwrite=<bool>" and "encoding=<encoding>")
          - createDir: Creates a directory. (Taking "folderpath=<str>")
          - deleteFile: Deletes a file. (Taking "filepath=<str>")
          - deleteDir: Deletes a directory. (Taking "folderpath=<str>")
          - writeToFile: Writes to a file. (Taking "inputs=<str>", "filepath=<str>", "append=<bool>" and "encoding=<encoding>")
          - readFromFile: Gets the content of a file. (Taking "filepath=<str>" and "encoding=<encoding>")
          - getWorkingDir: Gets the current working directory.
          - setWorkingDir: Sets or changes the working directory. (Taking "dir=<str>")

        For al functions taking encoding, the argument is an overwrite for the default encoding "filesys.defaultencoding" that is set to {filesys.defaultencoding}.
        ''')

    # Function to check if a file/directory exists
    def doesExist(path=str()):
        return bool(os.path.exists(path))
        
    # Function to check if a file/directory does not exist
    def notExist(path=str()):
        if os.path.exists(path): return False
        else: return True

    # Function to check if object is file
    def isFile(path=str()):
        return bool(os.path.isfile(path))

    # Function to check if object is directory
    def isDir(path=str()):
        return bool(os.path.isdir(path))

    # Error handler function where noexists flips functionality, checks for filetype and existance
    def errorHandler(action,path,noexist=False):
        output = True
        # Noexists checks
        if noexist:
            if filesys.doesExist(path):
                if action == "dir": output = f"\033[31mError: Directory already exists! ({path})\033[0m"
                if action == "file": output = f"\033[31mError: File already exists! ({path})\033[0m"
        else:
            if filesys.doesExist(path):
                # Directory
                if action == "dir":
                    if not filesys.isDir(path):
                        output = f"\033[31mError: Object is not directory. ({path})\033[0m"
                # Files
                elif action == "file":
                    if not filesys.isFile(path):
                        output = f"\033[31mError: Object is not file. ({path})\033[0m"
            # Not found
            else:
                if action == "folder": output = f"\033[31mError: Folder not found! ({path})\033[0m"
                if action == "file": output = f"\033[31mError: File not found! ({path})\033[0m"
        return output


    # Function to create file
    def createFile(filepath=(), overwrite=False, encoding=None):
        # Validate
        valid = filesys.errorHandler("file",filepath,noexist=True)
        # Overwrite to file
        if "already exists" in str(valid):
            if overwrite == False:
                print("File already exists, set overwrite to true to overwrite it.")
            else:
                try:
                    f = open(filepath, "x", encoding=encoding)
                    f.close()
                except: print("\033[31mAn error occurred!\033[0m")
        # Create new file
        else:
            try:
                f = open(filepath, "w", encoding=encoding)
                f.close()
            except: print("\033[31mAn error occurred!\033[0m")
    
    # Function to create directory
    def createDir(folderpath=()):
        # Validate
        valid = filesys.errorHandler("dir",folderpath,noexist=True)
        # Make directory
        if valid == True:
            try: os.mkdir(folderpath)
            except: print("\033[31mAn error occurred!\033[0m")
        else:
            print(valid); exit()
    
    # Function to delete a file
    def deleteFile(filepath=str()):
        # Validate
        valid = filesys.errorHandler("file",filepath)
        # Delete file
        if valid == True:
            try: os.remove(filepath)
            except: print("\033[31mAn error occurred!\033[0m")
        else:
            print(valid); exit()

    # Function to delete directory
    def deleteDir(folderpath=str()):
        # Validate
        valid = filesys.errorHandler("dir",folderpath)
        # Delete directory
        if valid == True:
            try: os.rmdir(folderpath)
            except: print("\033[31mAn error occurred!\033[0m")
        else:
            print(valid); exit()

    # Function to write to a file
    def writeToFile(inputs=str(),filepath=str(), append=False, encoding=None):
        if encoding != None: encoding = filesys.defaultencoding
        # Validate
        valid = filesys.errorHandler("file",filepath)
        if valid == True:
            # Check if function should append
            if append == True:
                try:
                    f = open(filepath, "a", encoding=encoding)
                    f.write(inputs)
                    f.close()
                except: print("\033[31mAn error occurred!\033[0m")
            # Overwrite existing file
            else:
                try:
                    f = open(filepath, "w", encoding=encoding)
                    f.write(inputs)
                    f.close()
                except: print("\033[31mAn error occurred!\033[0m")
        else:
            print(valid); exit()

    # Function to get file contents from file
    def readFromFile(filepath=str(),encoding=None):
        if encoding != None: encoding = filesys.defaultencoding
        # Validate
        valid = filesys.errorHandler("file",filepath)
        # Read from file
        if valid == True:
            try: 
                f = open(filepath, 'r', encoding=encoding)
                content = f.read()
                f.close()
                return content
            except: print("\033[31mAn error occurred!\033[0m")
        else:
            print(valid); exit()

    # Function to get current working directory
    def getWorkingDir():
        return os.getcwd()
    
    # Function to change working directory
    def setWorkingDir(dir=str()):
        os.chdir(dir)