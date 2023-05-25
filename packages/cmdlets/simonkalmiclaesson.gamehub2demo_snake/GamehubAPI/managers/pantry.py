managerFormat = [1, "https://sbamboo.github.io/websa/Gamehub/API/v2/docs/managers/format1.html"]


import importlib.util
def fromPath(path):
    spec = importlib.util.spec_from_file_location("module", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

class Manager():
    def __init__(self):
        import json,os
        self.json = json
        parentDir = os.path.dirname(__file__)
        pantryapi = fromPath(f"{parentDir}\\..\\libs\\libpantryapi.py")
        self.api = pantryapi.pantryapi
    # Function to sendback answers as dictionary
    def safeCast(self,*args):
        _object = args[0]
        try: return self.json.loads(_object.content.decode())
        except: return _object
    # Function to check if a basket exists
    def doesExist(self,key,scoreboard=str()) -> bool:
        ans = self.api(key, "GET")
        pantryData = self.json.loads(ans.content.decode())
        baskets = pantryData["baskets"]
        basketNames = list()
        for basket in baskets:
            basketNames.append(basket["name"])
        return scoreboard in basketNames
    # Creates a basket if it dosen't exists
    def create(self,key,scoreboard=str(),json=None):
        doesExist = self.doesExist(key,scoreboard=scoreboard)
        if doesExist != True:
            if json != None:
                ans = self.api(key, "POST", basket=scoreboard, body=json)
            else:
                ans = self.api(key, "POST", basket=scoreboard)
            return self.safeCast(ans)
    # Removes a basket if it exists
    def remove(self,key,scoreboard=str()):
        doesExist = self.doesExist(key,scoreboard=scoreboard)
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