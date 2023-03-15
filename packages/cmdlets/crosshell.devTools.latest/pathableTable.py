gottenData = []
for pathable in cspathables:
    gottenData.append(cs_getPathableProperties(pathable))

# Exclude stuff
keys = list(gottenData[0].keys())
excludes = ["paramhelp"]
newkeys = list()
for key in keys:
    if key in excludes: pass
    else:
        newkeys.append(key)
keys = newkeys

# Define table
table = dict()
for key in keys:
    table[key] = list()

# PopulateTable
for pathable in cspathables:
    data = cs_getPathableProperties(pathable)
    for key in keys:
        if key == "path":
            data[key] = data[key].replace(CSPackDir,"%CSPackDir%")
        if key == "description":
            if len(str(data[key])) > 100:
                data[key] = str(data[key])[0:100] + "..."
        table[key].append(data[key])

# Draw table
from assets.lib.tabledraw import drawTable
drawTable(table)