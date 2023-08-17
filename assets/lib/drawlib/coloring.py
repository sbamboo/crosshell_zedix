# Standard color-ansi palette
standardPalette = {
    "f_Black": "\033[90m",
    "b_Black": "\033[100m",
    "f_Red": "\033[91m",
    "b_Red": "\033[101m",
    "f_Green": "\033[92m",
    "b_Green": "\033[102m",
    "f_Yellow": "\033[93m",
    "b_Yellow": "\033[103m",
    "f_Blue": "\033[94m",
    "b_Blue": "\033[104m",
    "f_Magenta": "\033[95m",
    "b_Magenta": "\033[105m",
    "f_Cyan": "\033[96m",
    "b_Cyan": "\033[106m",
    "f_White": "\033[97m",
    "b_White": "\033[107m",
    "f_DarkBlack": "\033[30m",
    "b_DarkBlack": "\033[40m",
    "f_DarkRed": "\033[31m",
    "b_DarkRed": "\033[41m",
    "f_DarkGreen": "\033[32m",
    "b_DarkGreen": "\033[42m",
    "f_DarkYellow": "\033[33m",
    "b_DarkYellow": "\033[43m",
    "f_DarkBlue": "\033[34m",
    "b_DarkBlue": "\033[44m",
    "f_DarkMagenta": "\033[35m",
    "b_DarkMagenta": "\033[45m",
    "f_DarkCyan": "\033[36m",
    "b_DarkCyan": "\033[46m",
    "f_DarkWhite": "\033[37m",
    "b_DarkWhite": "\033[47m"
}

# Simple function to get the stdpalette (if '''import drawlib.coloring as coloring; stdpalette = coloring.stdpalette''' is not avaliable)
def getStdPalette() -> dict:
    return standardPalette

# Get the value from the palette using a palette
def getAnsiFromColor(color,palette):
    # Handle non-capitalized color names
    hasDark = "dark" in color.lower()
    if hasDark == True:
        color = color.lower()
        color = color.replace("dark", "")
    mode = color.split("_")[0]
    mode = mode + "_"
    color = color.split("_")[1]
    color = color.capitalize()
    if hasDark == True:
        color = mode + "Dark" + color
    else:
        color = mode + color
    # get the palette and error if non existing
    ansi = palette.get(color)
    if ansi == None:
        raise Exception(f"Color 'color' not found in selected palette!")
    else:
        return ansi

# Function to also autoNone if invalid input is given
def autoNoneColor(color,palette):
    if color == None or palette == None or type(palette) != dict:
        return None
    else:
        return getAnsiFromColor(color,palette)