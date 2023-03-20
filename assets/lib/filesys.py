# FileSys: Library to work with filesystems.
# Made by: Simon Kalmi Claesson

# Imports
import os
import shutil
import platform
try:
    from os import scandir
except ImportError:
    from scandir import scandir

# Simple alternative to conUtils
class altConUtils():
    def IsWindows():
        # Get platform and return boolean value depending of platform
        platformv = platform.system()
        if platformv == "Linux":
            return False
        elif platformv == "Darwin":
            return False
        elif platformv == "Windows":
            return True
        else:
            return False
    def IsLinux():
        # Get platform and return boolean value depending of platform
        platformv = platform.system()
        if platformv == "Linux":
            return True
        elif platformv == "Darwin":
            return False
        elif platformv == "Windows":
            return False
        else:
            return False
    def IsMacOS():
        # Get platform and return boolean value depending of platform
        platformv = platform.system()
        if platformv == "Linux":
            return False
        elif platformv == "Darwin":
            return True
        elif platformv == "Windows":
            return False
        else:
            return False

# Class containing functions
class filesys():

    defaultencoding = "utf-8"

    sep = os.sep

    # Help function
    def help(ret=False):
        helpText = '''
        This class contains functions to perform filessytem actions like creating and removing files/directories.
        Functions included are:
          - help: Shows this help message.
          - errorhandler: Internal function to handle errors. (Taking "action=<str_action>", "path=<str_path>" and "noexist=<bool>"
          - renameFile: Renames a file. (Taking "filepath=<str>", "newFilepath=<str>")
          - renameDir: Renames a directory. (Taking "folderpath=<str>", "newFolderpath=<str>")
          - doesExist: Checks if a file/directory exists. (Taking "path=<str>")
          - notExist: Checks if a file/directory does not exist. (Taking "path=<str>")
          - isFile: Checks if a object is a file. (Taking "path=<str>")
          - isDir: Checks if a object is a directory. (Taking "path=<str>")
          - getFileName: Returns the filename of the given file, excluding file extension. (Taking "path=<str>")
          - createFile: Creates a file. (Taking "filepath=<str>", "overwrite=<bool>" and "encoding=<encoding>")
          - createDir: Creates a directory. (Taking "folderpath=<str>")
          - deleteFile: Deletes a file. (Taking "filepath=<str>")
          - deleteDir: Deletes an empty directory. (Taking "folderpath=<str>")
          - deleteDirNE: Deletes a non empty directory, wrapping shutil.rmtree. (Taking "folderpath=<str>")
          - writeToFile: Writes to a file. (Taking "inputs=<str>", "filepath=<str>", "append=<bool>" and "encoding=<encoding>")
          - readFromFile: Gets the content of a file. (Taking "filepath=<str>" and "encoding=<encoding>")
          - getWorkingDir: Gets the current working directory.
          - setWorkingDir: Sets or changes the working directory. (Taking "dir=<str>")
          - copyFile: Wrapper around shutil.copy2. (Taking "sourcefile=<str>" and "destination=<str>")
          - copyFolder: Wrapper around shutil.copytree. (Taking "sourceDirectory=<str>" and "destinationDirectory=<str>")
          - copyFolder2: Custom recursive folder copy, destination may exists. (Taking "sourceDirectory=<str>", "destinationDirectory=<str>" and "debug=<bool>")
          - archive: Creates an archive of a folder. (Taking "sourceDirectory=<str>","<destination=<str>" and "format=<archive.format>") Note! Paths on on windows must be double slashed.
          - unArchive: Unpacks a archive into a folder. (Taking "archiveFile=<str>","<destination=<str>") Note! Paths on on windows must be double slashed.
          - scantree: Returns a generator, wrapps scantree. (Taking "path=<str>")
          - isExecutable: Checks if a file is an executable. (Taking "filepath=<str>" and optionally "fileEndings=<list>")
          - getMagicMime: Gets the magic-mime info of a file. (Taking "filepath=<str>")
          - openFolder: Opens a folder in the host's filemanager. (Taking "path=<str>") Might not work on al systems!
        For al functions taking encoding, the argument is an overwrite for the default encoding "filesys.defaultencoding" that is set to {filesys.defaultencoding}.
        '''
        if ret != True: print(helpText)
        else: return helpText

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

    # Function to get the filename of file (Excluding file extension)
    def getFileName(path=str()):
        return ('.'.join(os.path.basename(path).split(".")[:-1])).strip(".")

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

    # Function to rename a file
    def renameFile(filepath=str(),newFilepath=str()):
        # Validate
        valid1 = filesys.errorHandler("file",filepath)
        valid2 = filesys.errorHandler("file",newFilepath,noexist=True)
        if valid1 != True:
            print("[filepath]"+valid1)
        elif valid2 != True:
            print("[newFilepath]"+valid2)
        else:
            try:
                os.rename(filepath,newFilepath)
            except: print("\033[31mAn error occurred!\033[0m")

    # Function to rename a folder
    def renameDir(folderpath=str(),newFolderpath=str()):
        # Validate
        valid1 = filesys.errorHandler("dir",folderpath)
        valid2 = filesys.errorHandler("dir",newFolderpath,noexist=True)
        if valid1 != True:
            print("[folderpath]"+valid1)
        elif valid2 != True:
            print("[newFolderpath]"+valid2)
        else:
            try:
                shutil.move(folderpath,newFolderpath)
            except: print("\033[31mAn error occurred!\033[0m")

    # Function to create file
    def createFile(filepath=str(), overwrite=False, encoding=None):
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
    def createDir(folderpath=str()):
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

    # Function to delete directory NON EMPTY
    def deleteDirNE(folderpath=str()):
        # Validate
        valid = filesys.errorHandler("dir",folderpath)
        # Delete directory
        if valid == True:
            try: shutil.rmtree(folderpath)
            except: print("\033[31mAn error occurred!\033[0m")
        else:
            print(valid); exit()

    # Function to write to a file
    def writeToFile(inputs=str(),filepath=str(), append=False, encoding=None, autocreate=False):
        if encoding != None: encoding = filesys.defaultencoding
        # AutoCreate
        if autocreate == True:
            if not os.path.exists(filepath): filesys.createFile(filepath=filepath,encoding=encoding)
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

    # Function to copy a file
    def copyFile(sourcefile=str(),destination=str()):
        valid = filesys.errorHandler("file",sourcefile)
        if valid == True:
            try:
                shutil.copy2(sourcefile, destination)
            except: print("\033[31mAn error occurred!\033[0m")
        else:
            print(valid); exit()

    # Function to copy a folder
    def copyFolder(sourceDirectory=str(),destinationDirectory=str()):
        valid = filesys.errorHandler("dir",sourceDirectory)
        if valid == True:
            try:
                shutil.copytree(sourceDirectory, destinationDirectory)
            except: print("\033[31mAn error occurred!\033[0m")
        else:
            print(valid); exit()

    # Another function to copy a folder, custom made to allow the destination to exists
    def copyFolder2(sourceDirectory=str(),destinationDirectory=str(),debug=False):
        # Validate
        valid = filesys.errorHandler("dir", sourceDirectory)
        if valid == True:
            # Get files and folders in source that should be copied.
            entries = filesys.scantree(sourceDirectory)
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
                if altConUtils.IsWindows():
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
        else:
            print(valid); exit()

    # Function to zip a file
    def archive(sourceDirectory=str(),destination=str(),format=str()):
        valid = filesys.errorHandler("dir", destination)
        if valid == True:
            try:
                shutil.make_archive(('.'.join(destination.split(".")[:-1]).strip("'")), format=format, root_dir=sourceDirectory)
            except:  print("\033[31mAn error occurred!\033[0m")
        else:
            print(valid); exit()

    # Function to unzip a file
    def unArchive(archiveFile=str(),destination=str()):
        valid = filesys.errorHandler("file", archiveFile)
        if valid == True:
            try:
                shutil.unpack_archive(archiveFile, destination)
            except: print("\033[31mAn error occurred!\033[0m")
        else:
            print(valid); exit()
        
    # Function to scantree using scantree()
    def scantree(path=str()):
        valid = filesys.errorHandler("dir", path)
        if valid == True:
            try:
                # Code
                for entry in scandir(path):
                    if entry.is_dir(follow_symlinks=False):
                        yield from filesys.scantree(entry.path)
                    else:
                        yield entry
            except: print("\033[31mAn error occurred!\033[0m")
        else:
            print(valid); exit()

    # Function to check if a file is an executable
    def isExecutable(filepath=str(),fileEndings=None):
        exeFileEnds = [".exe",".cmd",".com",".py"]
        if fileEndings != None: exeFileEnds = fileEndings
        valid = filesys.errorHandler("file", filepath)
        if valid == True:
            try:
                # [Code]
                # Non Windows
                if altConUtils.IsLinux() or altConUtils.IsMacOS():
                    try: import magic
                    except:
                        os.system("pip3 install file-magic")
                    detected = magic.detect_from_filename(filepath)
                    return "application" in str(detected.mime_type)
                # Windows
                if altConUtils.IsWindows():
                    fending = str("." +''.join(filepath.split('.')[-1]))
                    if fending in exeFileEnds:
                        return True
                    else:
                        return False
            except: print("\033[31mAn error occurred!\033[0m")
        else:
            print(valid); exit()

    # Function to get magic-mime info:
    def getMagicMime(filepath=str()):
        import magic # Internal import since module should only be loaded if function is called.
        detected = magic.detect_from_filename(filepath)
        return detected.mime_type

    # Function to open a folder in the host's filemanager
    def openFolder(path=str()):
        # Local imports:
        try: import distro
        except:
            os.system("python3 -m pip install distro")
            import distro
        # Launch manager
        if altConUtils.IsWindows(): os.system(f"explorer {path}")
        elif altConUtils.IsMacOS(): os.system(f"open {path}")
        elif altConUtils.IsLinux():
            #Rassberry pi
            if distro.id() == "raspbian": os.system(f"pcmanfm {path}")


# Class with "powershell-styled" functions
class pwshStyled():

    # Alias to doesExist
    def testPath(path=str()):
        return filesys.doesExist(path)

    # Alias to readFromFile
    def getContent(filepath=str(),encoding=None):
        return filesys.readFromFile(filepath=filepath,encoding="utf-8")
    
    # Alias to writeToFile
    def outFile(inputs=str(),filepath=str(),append=False,encoding=None):
        filesys.writeToFile(inputs=str(),filepath=str(),append=False,encoding=None)

    # Alias to createFile
    def touchFile(filepath=str(),encoding=None):
        filesys.createFile(filepath=filepath, overwrite=False, encoding=encoding)
