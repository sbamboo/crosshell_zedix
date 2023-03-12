import json
import urllib.request

# Fetch the JSON data from the URL
url = "https://piston-meta.mojang.com/mc/game/version_manifest_v2.json"
response = urllib.request.urlopen(url)
data = response.read().decode()

# Parse the JSON data
versions = json.loads(data)["versions"]

# Imports
from assets.lib.tabledraw import *
from assets.lib.conUtils import pause
# Prep tablew
table = dict()
table["Version"] = list()
table["Type"] = list()
table["Release Time"] = list()
# Add values
for version in versions:
    table["Version"].append(version["id"])
    table["Type"].append(version["type"])
    table["Release Time"].append(version["releaseTime"])
# Print
columns, rows = os.get_terminal_size()
drawTable(table)
print("\033[42m" + "#"*columns + "\033[0m")
print("Press any key to continue...")
pause()
