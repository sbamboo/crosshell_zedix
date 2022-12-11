operation = str(argv[-1])
try:
    argv.pop(-1)
    prefix = argv[0:]
    # Handle prefix
    prefix = ' '.join(prefix)
    if prefix[0] == " ":
        prefix.replace(" ", "",1)
except:
    prefix = ""

# Handle decode
if "-decode" in operation:
    operation = operation.replace("-decode","")
    prefix = prefix.replace("{%1%}", "'")
    prefix = prefix.replace("{%2%}", '"')

prefix = prefix.replace("\\'","§")
prefix = prefix.replace("'","")
prefix = prefix.replace('§',"'")

# Set
if operation == "-set" or operation == "-s":
    csshell_prefix = prefix
    cs_persistance("set","cs_prefix",cs_persistanceFile,csshell_prefix)
# Reset
if operation == "-reset" or operation == "-r":
    csshell_prefix = cssettings["Presets"]["Prefix"]
    cs_persistance("set","cs_prefix",cs_persistanceFile,csshell_prefix)
# Dir
if operation == "-dir":
    persprefix_dir = cs_persistance("get","cs_prefix_enabled_dir",cs_persistanceFile)
    if persprefix_dir == "True":
        csprefix_dir = False
    elif persprefix_dir == "False":
        csprefix_dir = True
    cs_persistance("set","cs_prefix_enabled_dir",cs_persistanceFile,csprefix_dir)
# Enable
if operation == "-enable" or operation == "-e":
    csprefix_enabled  = True
    cs_persistance("set","cs_prefix_enabled",cs_persistanceFile,csprefix_enabled)
# Disable
if operation == "-disable" or operation == "-d":
    csprefix_enabled  = False
    cs_persistance("set","cs_prefix_enabled",cs_persistanceFile,csprefix_enabled)
# Get
if operation == "-get" or operation == "-g":
    pref = str(cs_persistance("get","cs_prefix",cs_persistanceFile))
    print("\033[36mCurrent Prefix:            \033[0m'" + pref + "'")
    print("\033[36mRendered prefix:           \033[0m'" + formatPrefix(pref,False,True,csworking_directory,globals()) + "'")
    print("\033[36mRendered prefix: \033[104m(Showdir)\033[0m \033[0m'" + formatPrefix(pref,True,True,csworking_directory,globals()) + "'")