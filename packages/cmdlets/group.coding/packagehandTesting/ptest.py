url = "https://github.com/simonkalmiclaesson/packagehand_repository/raw/main/packages/cmdlet/crosshell.packagehandTesting/latest.package"

import requests

session = requests.session()
response = session.get(url,allow_redirects=True,timeout=5)
session.close()

print(response.headers["Content-Length"])