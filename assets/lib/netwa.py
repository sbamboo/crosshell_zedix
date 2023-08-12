# NetwaLib: Simple network library.
# Made by: Simon Kalmi Claesson
# 2023-02-09

# [Imports]
import traceback
import requests

# [Classes]
class netwa:
	# Function to check for an internet connection
	def has_connection(override_url=None):
		# If no url is given, default to google.
		if override_url == None or override_url == "":
			override_url = "https://google.com"
		# Check/Validate the connection, catch exeptions and return boolean
		try:
			req = requests.get(override_url)
			req.raise_for_status()
		except:
			return False

	# Text response return alternative to has_connection
	def t_has_connection(override_url=None):
		# If no url is given, default to google.
		if override_url == None or override_url == "":
			override_url = "https://google.com"
		# Check/Validate the connection, catch exeptions and return boolean
		try:
			req = requests.get(override_url)
			req.raise_for_status()
			print( f"\033[32m[cs.lib.Netwa]: Connected: {req.ok}" )
		except Exception:
			return f"\033[31m[cs.lib.Netwa]: { traceback.format_exc() }\033[0m"


# [Functions]
def simpleDownload(url=str(),file=str()):
    try:
        r = requests.get(url, allow_redirects=True)
    except:
        print("\033[31mConnection could not be initated, please check your internet connection!\033[0m")
        exit()
    if file == "":
        return r.content
    open(file, 'wb').write(r.content)