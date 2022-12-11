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

# Handle content
content = content.replace("%s%"," ")
content = content.replace('"', "")
content = content.replace("'", "")

# Set
if operation == "-set":
    currentConfig = cs_persistance("get",name,cs_persistanceFile)
    cs_persistance("set",name,cs_persistanceFile,content)
    print(f"\033[32mChanged {name} to '{content}' from '{currentConfig}'\033[0m")

# Get
if operation == "-get":
    currentConfig = cs_persistance("get",name,cs_persistanceFile)
    print(f"\033[33m{name} = '{currentConfig}'\033[0m")