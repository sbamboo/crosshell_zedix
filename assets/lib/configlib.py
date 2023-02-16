# ConfigLib: Library for using config files
# Made by: Simon Kalmi Claesson
# 2023-02-04

# [Imports]
import os
import yaml
import json

# [Function]

# Function to read a config file
def readConfig(filepath):
    if os.path.exists(filepath):
        content = open(filepath, 'r').read().split("\n")
        dataDict = dict()
        for line in content:
            if line.strip()[0] != "#":
                name = line.split("=")[0].strip(" ")
                data = ''.join(line.split("=")[1:(len(line.split("=")))]).strip()
                dataDict[name] = data
        return dataDict
    
# Function to get/set a json file
def useJson(mode=str(),jsonFile=str(),dictionary=dict()):
    # Load
    if mode == "load":
        with open(jsonFile) as json_file:
            dictionary = json.load(json_file)
            if dictionary == "" or dictionary == {} or dictionary == None:
                dictionary = {}
        return dictionary
    # Set
    if mode == "set":
        with open(jsonFile, "w") as outfile:
            json.dump(dictionary, outfile)

# Function to get/set a yaml file
def useYaml(mode=str(),yamlFile=str(),dictionary=dict()):
    if mode == "get":
        with open(yamlFile, "r") as yamli_file:
            dictionary = yaml.safe_load(yamli_file)
            if dictionary == "" or dictionary == {} or dictionary == None:
                dictionary = {}
        return dictionary
    if mode == "set":
        with open(yamlFile, "w") as outfile:
            yaml.dump(dictionary, outfile)