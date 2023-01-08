try:
    operation = argv[0]
except:
    operation = ""
try:
    name  = argv[1]
except:
    name = ""
try:
    content  = argv[2]
except:
    content = ""

try:
    # Get name and category
    category = name.split(".")[0]
    name = name.split(".")[1]
    category = category.capitalize()
    name = name.capitalize()
    #Content
    content = content.replace("%s%"," ")
    content = content.replace('"', "")
    content = content.replace("'", "")
except:
    category = ""

# Notice
print(pt_format(cs_palette,f"\033[33mThis cmdlet can be used to change settings, but it is currently recomended to manualy edit the settings file: '{cs_settingsFile}'\033[0m"))

# Set
if operation == "-set":
    currentConfig = cssettings[category][name]
    if str(content) != str(currentConfig):
        cssettings[category][name] = content
        cs_settings("set",cs_settingsFile,cssettings)
        persPrintCmdletDebug = bool(cssettings["General"]["PrintCmdletDebug"])
        print(pt_format(cs_palette,f"\033[32mChanged {category}.{name} to '{content}' from '{currentConfig}'\033[0m"))

# Get
if operation == "-get":
    currentSettings = cs_settings("load",cs_settingsFile,cssettings)
    currentConfig = currentSettings[category][name]
    print(pt_format(cs_palette,f"\033[33m{category}.{name} = '{currentConfig}'\033[0m"))

# Reload
if operation == "-reload":
    currentSettings = cs_settings("load",cs_settingsFile,cssettings)
    cssettings = currentSettings
    persPrintCmdletDebug = bool(cssettings["General"]["PrintCmdletDebug"])
    print(pt_format(cs_palette,"\033[32mReloaded settings.\033[0m"))