from assets.lib.tqdm_ui import *
try:
    import zipfile
except:
    os.system("python3 -m pip install zipfile")
    import zipfile


# Get argv as string
stringInput = (' '.join(argv)).strip(" ")

stringInput = stringInput.strip('"')

# Handle Online packages group
onlinePackagesGroup = f"{path_cmdletsfolder}{os.sep}group.onlinePackages"
if not os.path.exists(onlinePackagesGroup):
    os.mkdir(onlinePackagesGroup)

# Setup file path
filename = stringInput.split('/')[-1]
ZipFilePath = f"{onlinePackagesGroup}{os.sep}{filename}"
ZipFilePath_folder = f"{onlinePackagesGroup}{os.sep}{filename.rstrip('.zip')}"

# Goto group
OldPath = os.getcwd()
os.chdir(onlinePackagesGroup)

# Download archive
formatting = "{desc}: {percentage:3.0f}% |{color}{bar}{reset}| {n_fmt}/{total_fmt}  {rate_fmt}{postfix}  [Elap: {elapsed} | ETA: {remaining}]"
chars = " " + chr(9592) + chr(9473)
downloadBar(stringInput,formatting,chars)

# Handle package file
if filename.split(".")[-1] == "package":
    ZipFilePath_new = filename.replace(".package", ".zip")
    os.rename(ZipFilePath, ZipFilePath_new)

# Expand archive
with zipfile.ZipFile(ZipFilePath,"r") as zip_ref:
    zip_ref.extractall(ZipFilePath_folder)

# Check if directory exists
if os.path.exists(ZipFilePath_folder):

    # Load cmdlets inside directory
    packagePathables = cs_loadCmdlets(ZipFilePath_folder,allowedFileTypes)
    for pathable in packagePathables:
        cspathables.append(pathable)
    
    # Remove zip file
    os.remove(ZipFilePath)

else:
    print(pt_format(cs_palette,"\033[31mError! Failed import download, file not found post download.\033[0m"))