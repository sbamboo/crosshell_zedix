# [Imports]
import os
import yaml
import random
from tabledraw import drawTable

# [Functions]
def readConfig(filename=str()) -> dict:
    with open(filename, "r") as yamli_file:
        dictionary = yaml.safe_load(yamli_file)
    return dictionary

def GetTotIndex(player=dict(),attributeModifiers=dict(),missing_attribute_default=float()) -> float():
    if player["type"] == "hider": modifierType = "hider_modifier"
    if player["type"] == "seeker": modifierType = "seeker_modifier"
    attributes = list(player["attributes"].keys())
    totalIndex = 0
    for attribute in attributes:
        if (player["attributes"]).get(attribute) == None or (player["attributes"]).get(attribute) == "":
            playerAttributeValue = missing_attribute_default
        else:
            playerAttributeValue = float(player["attributes"][attribute])
        totalIndex += playerAttributeValue * float(attributeModifiers[attribute][modifierType])
    return totalIndex
       
def HandlePlayerTypes() -> dict:
    global players
    SeekerTimes = [value["type"] for key,value in players.items()].count("seeker")
    if SeekerTimes == 0:
        players[random.choice(list(players.keys()))]["type"] = "seeker"
    for player in players:
        if players[player]["type"] != "seeker":
            players[player]["type"] = "hider"
    return players

def randomiser(offset_min,offset_max,offset_type) -> float:
    global player
    indexonly = [value["index"] for index,value in players.items()]
    mini = min(indexonly)
    maxi = max(indexonly)
    random_index = random.randint(mini,maxi)
    if offset_type == "+": random_index += random.randint(offset_min, offset_max)
    elif offset_type == "-": random_index -= random.randint(offset_min, offset_max)
    return random_index

# [Setup]
# Crosshell compatibility
try: ScriptRoot = CSScriptRoot                             # Fix if running in crosshell 
except: ScriptRoot = os.path.dirname(__file__)  #
# Variables
configFile = ScriptRoot + os.sep + "config.yml"
config = readConfig(configFile)
players = config["players"]
attributes = config["attribute_modifiers"]
missing_attribute_default = float(config["missing_attribute_default"])
randomiserParameters = config["randomiser_parameters"]
total_seekerFactor = config["seekerfactor_default"]

# [Code]
# Handle types of players
players = HandlePlayerTypes()

# Get playerIndexes
for player in players:
    players[player]["index"] = GetTotIndex(players[player],attributes,missing_attribute_default) # Needs players[player] to get correct iteratpr instance

# Add random numbers to players indexes
for player in players:
    players[player]["index"] += randomiser(randomiserParameters["offset_min"],randomiserParameters["offset_max"],randomiserParameters["offset_type"])

# Calculate total seeker factor
for player in players:
    if players[player]["type"] == "seeker":
        total_seekerFactor += players[player]["index"]
        players[player]["time"] = "Seeker"

# Calculate finding time for players
for player in players:
    if players[player]["type"] == "hider":
        players[player]["time"] = players[player]["index"] * total_seekerFactor

# Sort dictionary based on time
tobesorted = dict()
excluded = dict()
for player in players:
    if str(players[player]["time"]).lower() != "seeker":
        tobesorted[player] = players[player]
    else:
        excluded[player] = players[player]
tobesorted = dict(sorted(tobesorted.items(), key=lambda item: item[1]["time"], reverse=True))
players = tobesorted.copy()
for player in excluded:
    players[player] = excluded[player]

# Print out times
#printString = list()
#longest = 0
#for player in players:
#    string = player + ": " + str(players[player]["time"])
#    printString.append(string)
#    if len(string) > longest: longest = len(string)
#print("╭" + "─"*longest + "╮")
#for line in printString:
#    print("│" + line + " "*(longest-len(line))  + "│")
#print("╰" + "─"*longest + "╯")


# Print out dictionary
table = dict()
table["Players"] = list()
table["Type"] = list()
table["Time"] = list()
table["Index"] = list()
for attribute in attributes:
    table[attribute] = list()
for player in players:
    table["Players"].append(player)
    table["Type"].append(players[player]["type"])
    table["Time"].append(players[player]["time"])
    for attribute in attributes:
        table[attribute].append(str(players[player]["attributes"][attribute]))
    table["Index"].append(players[player]["index"])

drawTable(table)