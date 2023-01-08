# Simple downloading lib by Simon Kalmi Claesson
import requests

def simpleDownload(url=str(),file=str()):
    r = requests.get(url, allow_redirects=True)
    if file == "":
        return r.content
    open(file, 'wb').write(r.content)