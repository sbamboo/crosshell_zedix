# NetwaLib, 2023-01-02 Simon Kalmi Claesson

# [Imports]
import urllib
import traceback

# [Classes]
class netwa:
	# Function to check for an internet connection
	def has_connection(override_url=None):
		# If no url is given, default to google's dns ip (8.8.8.8)
		if override_url != None and override_url != "":
			override_url = "8.8.8.8"
		# Check/Validate the connection using urllib, catch exeptions and return boolean
		try:
			urllib.request.urlopen(url=override_url,timeout=3)
			return True
		except:
			return False

	# Text response return alternative to has_connection
	def t_has_connection(override_url=None):
		# If no url is given, default to google's dns ip (8.8.8.8)
		if override_url != None and override_url != "":
			override_url = "8.8.8.8"
		# Check/Validate the connection using urllib, catch exeptions and return boolean
		try:
			urllib.request.urlopen(url=override_url,timeout=3)
			return "\033[32m[cs.lib.Netwa]: Connection is valid.\033[0m"
		except Exception:
			return f"\033[31m[cs.lib.Netwa]: { traceback.format_exc() }\033[0m"