# [Imports]
import os
import argparse
import shutil
import yaml
import json

# [Setup]
app_project_formatVersion = 1.0
projects_directory = CSScriptRoot + os.sep + "projects"
templateYAML_file = CSScriptRoot + os.sep + "template.yaml"
if not os.path.exists: os.mkdir(projects_directory)
templateYAML = getContent(templateYAML_file)

# region [Arguments]
# Main
cparser = argparse.ArgumentParser(prog="Resgen",exit_on_error=False,add_help=False)
cparser.add_argument('--exhelp', action='store_true', default=False, help='Shows help then exits.')
cparser.add_argument('-h', '--help', action='store_true', default=False, help='Shows help menu.')
# General
cparser.add_argument('--openprojects','--openproj','--oj', dest="openprojects", action='store_true', help="Opens the resgen projects directory.")
# Project Management
cparser.add_argument('-init', dest="initproject", help="Inits a project, supply name.")
cparser.add_argument('-remove', dest="removeproject", help="Removes a project, supply name. Irreversible!!!")
cparser.add_argument('-archive', dest="archiveproject", help="Creates a zipfile of the project in the projects folder.")
# Compile
cparser.add_argument('-compile', dest="compileproject", help="Compiles a project, supply name. (This will remove any old compilations)")
# Create main arguments object
try: argus = cparser.parse_args(argv)
except: argus = cparser.parse_args()
if argus.help: cparser.print_help()
if argus.exhelp: cparser.print_help(); exit()
# endregion

# region [GeneralActions]
if argus.openprojects:
    if IsWindows(): os.system(f"explorer {projects_directory}")
    elif IsMacOS(): os.system(f"open {projects_directory}")
    elif IsLinux():
        #Rassberry pi
        if distro.id() == "raspbian": os.system(f"pcmanfm {projects_directory}")
# endregion

# region [Project Management]
# Init
if argus.initproject:
    projdir = f"{projects_directory}{os.sep}{argus.initproject}"
    projfile = f"{projdir}{os.sep}{argus.initproject}.yaml"
    if not os.path.exists(projdir):
        os.mkdir(projdir)
        outFile(templateYAML,projfile)
        print(pt_format(cs_palette,f"\033[32mCreated yaml template at '{projfile}', use 'resgen --openproject' to open the project directory.\033[0m"))
    else:
        print(pt_format(cs_palette,f"\033[31mA project directory already exists with the name '{argus.initproject}', remove it or change the name."))
# Remove
if argus.removeproject:
    projdir = f"{projects_directory}{os.sep}{argus.removeproject}"
    if os.path.exists(projdir):
        if input(pt_format(cs_palette,f"\033[33mAre you want to delete the project '{argus.removeproject}'? This action is irreversible! [y/n] \033[0m")).lower() == "y":
            shutil.rmtree(projdir)
    else:
        print(pt_format(cs_palette,f"\033[31mNo project with the name '{argus.initproject}' found."))
# Archive
if argus.archiveproject:
    projdir = f"{projects_directory}{os.sep}{argus.archiveproject}"
    if os.path.exists(projdir):
        shutil.make_archive(projdir, "zip", projdir)
    else:
        print(pt_format(cs_palette,f"\033[31mNo project with the name '{argus.initproject}' found."))
# endregion

# region [Compile]
if argus.compileproject:
    projdir = f"{projects_directory}{os.sep}{argus.compileproject}"
    projfile = f"{projdir}{os.sep}{argus.compileproject}.yaml"
    resourcepackFolder = f"{projdir}{os.sep}resourcepack"
    resourcepackMcMeta = f"{resourcepackFolder}{os.sep}pack.mcmeta"
    if not os.path.exists(projdir):
        print(pt_format(cs_palette,f"\033[31mNo project with the name '{argus.compileproject}' found."))
    # Compile
    else:
        print(pt_format(cs_palette,f"\033[32mCompiling resource pack of project '{argus.compileproject}'"))
        print("This will create a folder in the project directory named 'resourcepack' containing the compiled pack.")
        # Get region data
        with open(projfile, "r") as yamli_file:
            raw_projectData = yaml.safe_load(yamli_file)
        projectData = raw_projectData["ResGenProject"]
        # Check ProjectFormat
        project_formatVer = projectData["Metadata"]["Format"]
        if project_formatVer != app_project_formatVersion:
            print(pt_format(cs_palette,f"\033[31mThe projects format version '{project_formatVer}' is not compatible with this version of resgen (FormatVersion:{app_project_formatVersion})"))
            exit()
        # Create resource pack folder
        if os.path.exists(resourcepackFolder): shutil.rmtree(resourcepackFolder)
        else: os.mkdir(resourcepackFolder)
        # Retrive resourcepack data from project
        name = (projectData["ResourcepackData"]["Name"]).strip('"')
        if name == "" or name == None: name == argus.compileproject
        description = (projectData["ResourcepackData"]["Description"]).strip('"')
        packformat = projectData["ResourcepackData"]["PackFormat"]
        # Create resource pack meta data
        mcmeta_dict = {
            "pack": {
                "pack_format": packformat,
                "description": description
            }
        }
        mcmeta_json = json.dumps(mcmeta_dict, indent=4)
        touchFile(resourcepackMcMeta)
        outFile(mcmeta_json,resourcepackMcMeta)
        # Create base folder structure
        os.mkdir(f"{resourcepackFolder}{os.sep}assets")
        os.mkdir(f"{resourcepackFolder}{os.sep}assets{os.sep}minecraft")
        os.mkdir(f"{resourcepackFolder}{os.sep}assets{os.sep}minecraft{os.sep}optifine")
        citDataFolder = f"{resourcepackFolder}{os.sep}assets{os.sep}minecraft{os.sep}optifine{os.sep}cit"
        os.mkdir(citDataFolder)
        # Create cit files
        for cit in projectData["Cit"]:
            cit_folder = f"{citDataFolder}{os.sep}{cit}"
            # Get data
            cit_Data = projectData["Cit"][cit]
            cit_item = (cit_Data["Item"]).strip('"')
            cit_type = cit_Data["Type"]
            cit_texture = (cit_Data["Texture"]).strip('"')
            cit_NbtName = (cit_Data["Nbt.Name"]).strip('"')
            if cit_type == "Armor": cit_layer = cit_Data["Layer"]
            else: cit_layer = None
            # Add project directory to the paths
            cit_texture = projdir + os.sep + cit_texture
            if cit_layer != None:
                cit_layer_id = (cit_layer["Id"]).strip('"')
                cit_layer_texture = (cit_layer["Texture"]).strip('"')
                cit_layer_texture = projdir + os.sep + cit_layer_texture
            # Create folder for this cit
            os.mkdir(cit_folder)
            # Copy texture files
            shutil.copy(cit_texture,f"{cit_folder}{os.sep}texture.png")
            if cit_layer != None:
                shutil.copy(cit_layer_texture,f"{cit_folder}{os.sep}layer.png")
            # Create partialPaths
            cit_texture_path = f"optifine/cit/{cit}/texture.png"
            if cit_layer != None:
                cit_layer_path = f"optifine/cit/{cit}/layer.png"
            # Create properties file
            cit_propertieFile = cit_folder + os.sep + cit + ".properties"
            cit_propertieFile_armor = cit_folder + os.sep + cit + "_armor.properties"
            if cit_type == "Item":
                rawCitProperties = f"type=item\nmatchItems={cit_item}\ntexture={cit_texture_path}\nnbt.display.Name={cit_NbtName}"
                touchFile(cit_propertieFile)
                outFile(rawCitProperties,cit_propertieFile)
            elif cit_type == "Armor":
                rawCitProperties = f"type=item\nmatchItems={cit_item}\ntexture={cit_texture_path}\nnbt.display.Name={cit_NbtName}"
                rawCitProperties_armor = f"type=armor\nmatchItems={cit_item}\nnbt.display.Name={cit_NbtName}\ntexture.{cit_layer_id}={cit_layer_path}"
                touchFile(cit_propertieFile)
                outFile(rawCitProperties,cit_propertieFile)
                touchFile(cit_propertieFile_armor)
                outFile(rawCitProperties_armor,cit_propertieFile_armor)
        print(pt_format(cs_palette,"\033[32mCompilation of resourcepack complete, open the project folder by running 'resgen --openproject'\033[0m"))
# endregion