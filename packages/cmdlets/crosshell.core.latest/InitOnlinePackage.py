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
onlinePackagesGroup = f"{csCmdletPath}{os.sep}{group.onlinePackages}"
if not os.path.exists(onlinePackagesGroup):
    os.mkdir(onlinePackagesGroup)

# Setup file path
ZipFilePath = f"{onlinePackagesGroup}{os.sep}{stringInput.split('/')[0]}"
ZipFilePath_folder = ('.'.join(ZipFilePath.split(".")[1:])).strip(".")

# Goto group
OldPath = os.getcwd()
os.chdir(onlinePackagesGroup)

# Download archive
formatting = "{desc}: {percentage:3.0f}% |{color}{bar}{reset}| {n_fmt}/{total_fmt}  {rate_fmt}{postfix}  [Elap: {elapsed} | ETA: {remaining}]"
chars = " " + chr(9592) + chr(9473)
downloadBar(stringInput,formatting,chars)

# Expand archive
with zipfile.ZipFile(ZipFilePath,"r") as zip_ref:
    zip_ref.extractall(ZipFilePath_folder)

# Check if directory exists
if os.path.exists(ZipFilePath_folder):

    # Load cmdlets inside directory
    packagePathables = cs_loadCmdlets(ZipFilePath_folder,allowedFileTypes)
    for pathable in packagePathables:
        cspathables.append(pathable)
    
else:
    print(pt_format(cs_palette,"\033[31mError! Failed import download, file not found post download.\033[0m"))