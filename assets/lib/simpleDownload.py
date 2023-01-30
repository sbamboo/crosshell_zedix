# SimpleDownload: Simple download library
# Made by: Simon Kalmi Claesson

# Imports
import requests

def simpleDownload(url=str(),file=str()):
    r = requests.get(url, allow_redirects=True)
    if file == "":
        return r.content
    open(file, 'wb').write(r.content)