try:
	req = requests.get('https://google.com')
	req.raise_for_status()
	print( req.ok )
except:
	print("No connection established")