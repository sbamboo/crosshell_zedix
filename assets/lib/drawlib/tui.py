from .assets import getANSI,deTokenize

# Function to place an input() statement at a x,y position
def inputAtCords (posX, posY, text=None, color=None, offsetX=None, offsetY=None):
	if offsetX != None: posX = posX + offsetX
	if offsetY != None: posY = posY + offsetY
	# Save cursorPos
	print("\033[s")
	# Get color code
	if "ansi:" in color:
		color = color.replace("ansi:","")
		colorcode = color
	else:
		colorcode = getANSI(color)
	# Print texture
	# Replace tokens in line
	text = deTokenize(text)
	# Set ansi prefix
	ANSIprefix = "\033[" + str(posY) + ";" + str(posX) + "H" + "\033[" + str(colorcode) + "m"
	input(str(ANSIprefix + str(text + "\033[0m")))
	# Load cursorPos
	print("\033[u\033[2A")