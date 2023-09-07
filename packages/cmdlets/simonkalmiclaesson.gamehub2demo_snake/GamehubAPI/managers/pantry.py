managerFormat = [3, "https://sbamboo.github.io/websa/docview/?markdown=https://raw.githubusercontent.com/sbamboo/Gamehub/main/API/v2/docs/managers/format3.md&css=https://raw.githubusercontent.com/sbamboo/Gamehub/main/API/v2/docs/managers/docs.css&json=https://raw.githubusercontent.com/sbamboo/Gamehub/main/API/v2/docs/docview_files.json",[2]]


import importlib.util
import os
def fromPath(path):
    path = path.replace("\\",os.sep)
    spec = importlib.util.spec_from_file_location("module", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

class Manager():
    def __init__(self,doCheck=None):
        import json,os
        self.json = json
        parentDir = os.path.dirname(__file__)
        pantryapi = fromPath(f"{parentDir}\\..\\libs\\libpantryapi.py")
        self.api = pantryapi.pantryapi
        if doCheck == None: self.doCheck_umb = True
        else: self.doCheck_umb = doCheck
    # Function to sendback answers as dictionary
    def safeCast(self,*args):
        _object = args[0]
        try: return self.json.loads(_object.content.decode())
        except: return _object
    # Function to check if a basket exists
    def doesExist(self,key,scoreboard=str(),doCheck=None) -> bool:
        if doCheck == None: doCheck = True
        if doCheck == True:
            ans = self.api(key, "GET")
            pantryData = self.json.loads(ans.content.decode())
            baskets = pantryData["baskets"]
            basketNames = list()
            for basket in baskets:
                basketNames.append(basket["name"])
            return scoreboard in basketNames
        else: return True
    # Creates a basket if it dosen't exists
    def create(self,key,scoreboard=str(),jsonDict=None,doCheck=None):
        if doCheck == None: doCheck = self.doCheck_umb
        doesExist = self.doesExist(key,scoreboard=scoreboard,doCheck=doCheck)
        if doesExist != True:
            if jsonDict != None:
                ans = self.api(key, "POST", basket=scoreboard, body=jsonDict)
            else:
                ans = self.api(key, "POST", basket=scoreboard)
            return self.safeCast(ans)
    # Replaces a basket if it exists
    def replace(self,key,scoreboard=str(),jsonDict=None,doCheck=None):
        if doCheck == None: doCheck = self.doCheck_umb
        doesExist = self.doesExist(key,scoreboard=scoreboard,doCheck=doCheck)
        if doesExist == True:
            if jsonDict != None:
                ans = self.api(key, "POST", basket=scoreboard, body=jsonDict)
            else:
                ans = self.api(key, "POST", basket=scoreboard)
            return self.safeCast(ans)
    # Removes a basket if it exists
    def remove(self,key,scoreboard=str(),doCheck=None):
        if doCheck == None: doCheck = self.doCheck_umb
        doesExist = self.doesExist(key,scoreboard=scoreboard,doCheck=doCheck)
        if doesExist == True:
            ans = self.api(key, "DELETE", basket=scoreboard)
            return self.safeCast(ans)
    # Gets a basket value
    def get(self,key,scoreboard=str()) -> dict:
        ans = self.api(key, "GET", basket=scoreboard)
        return self.safeCast(ans)
    # Appends a baskets values
    def append(self,key,scoreboard=str(),jsonDict=dict()):
        ans = self.api(_id=key, method="PUT", basket=scoreboard, body=jsonDict)
        return self.safeCast(ans)