operation = str(argv[-1])
try:
    argv.pop(-1)
    title = argv[0:]
    # Handle title
    title = ' '.join(title)
    if title[0] == " ":
        title.replace(" ", "",1)
    title = title.replace('\\"',"§")
    title = title.replace('"',"")
    title = title.replace('§','"')
except:
    title = ""


# Set
if operation == "-set" or operation == "-s":
    saveTitle(title,cs_persistanceFile)
# Reset
if operation == "-reset" or operation == "-r":
    saveTitle(cssettings["Presets"]["Title"],cs_persistanceFile)