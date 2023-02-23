# Virtuell Hide & Seek

# [imports]
import random

# [Definitions]
attributes = {
    "ingenuity": {"hider":3, "seeker":2},
    "patience":     {"hider":1, "seeker":2},
    "giggling":  {"hider":-2, "seeker":-1}
}
hiders = {}
seekers = {}
indexes = {}

#[Functions]
# Function to calculate total index of a player
def GetTotIndex(player=str(),playerType=str()):
    if playerType == "hider":
        totIndex =  player["ingenuity"] * attributes["ingenuity"]["hider"]
        totIndex += player["patience"] * attributes["patience"]["hider"]
        totIndex += player["giggling"] * attributes["giggling"]["hider"]
        return totIndex
    elif playerType == "seeker":
        totIndex =  player["ingenuity"] * attributes["ingenuity"]["seeker"]
        totIndex += player["patience"] * attributes["patience"]["seeker"]
        totIndex += player["giggling"] * attributes["giggling"]["seeker"]
        return totIndex
# Function to add a player
def addPlayer(name=str(),type=str(),ingenuity=0,patience=0,giggling=0) -> None:
    global hiders,seekers
    if type == "hider":     hiders = hiders   | {name: {"ingenuity":ingenuity, "patience":patience,  "giggling":giggling}}
    elif type == "seeker":  seekers = seekers | {name: {"ingenuity":ingenuity, "patience":patience,  "giggling":giggling}}

# [Code]
# Add Players
addPlayer("stina","hider",5,5,5)
addPlayer("orvar","hider",3,10,9)
addPlayer("per","hider",1,1,9)
addPlayer("olle","hider",9,1,1)
addPlayer("pernilla","seeker",2,5,9)

# Get dictionary containing every players total index values
for hider in hiders: indexes  = indexes | {hider: GetTotIndex(hiders[hider],"hider")}
for seeker in seekers: indexes  = indexes | {seeker: GetTotIndex(seekers[seeker],"seeker")}

# Get a list of indexes only
indexOnly = [value for index,value in indexes.items()]

# Add random numbers to players indexes
for player in indexes: 
    indexes[player] += random.randint(min(indexOnly), max(indexOnly))

# Add seeker number to hiders
for hider in hiders:
    seekerFactor = 1
    for seeker in seekers:
        seekerFactor = indexes[seeker]
    indexes[hider] *= seekerFactor

print(indexes)