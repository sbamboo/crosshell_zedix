from assets.lib.drawlib import *
try:
	if argv[0] == '"' and argv[1] == '"': char = " "
	else:
		char = ''.join(argv)
	char = char.strip('"')
	if char == "" or char == None: char = " "
except: char = " "
fill_terminal(char)