from asset import *

def inputAtCords (posX, posY, text=None, color=None):
	# Save cursorPos
	print("\033[s")
	# Get color code
	colorcode = getANSI(color)
	# Print texture
	# Replace tokens in line
	text = deTokenize(text)
	# Set ansi prefix
	ANSIprefix = "\033[" + str(posY) + ";" + str(posX) + "H" + "\033[" + str(colorcode) + "m"
	input(str(ANSIprefix + str(text + "\033[0m")))
	# Load cursorPos
	print("\033[u\033[2A")