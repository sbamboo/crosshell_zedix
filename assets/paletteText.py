import re

paletteText_standardPalette = {
    # Text colors (normal intensity)
    "30": "f#000000",  # Black
    "31": "f#FF0000",  # Red
    "32": "f#00FF00",  # Green
    "33": "f#FFFF00",  # Yellow
    "34": "f#0000FF",  # Blue
    "35": "f#FF00FF",  # Magenta
    "36": "f#00FFFF",  # Cyan
    "37": "f#FFFFFF",  # White
    # Text colors (bright intensity)
    "90": "f#555555",  # Black
    "91": "f#FF5555",  # Red
    "92": "f#55FF55",  # Green
    "93": "f#FFFF55",  # Yellow
    "94": "f#5555FF",  # Blue
    "95": "f#FF55FF",  # Magenta
    "96": "f#55FFFF",  # Cyan
    "97": "f#FFFFFF",  # White
    # Background colors (normal intensity)
    "40": "b#000000",  # Black
    "41": "b#FF0000",  # Red
    "42": "b#00FF00",  # Green
    "43": "b#FFFF00",  # Yellow
    "44": "b#0000FF",  # Blue
    "45": "b#FF00FF",  # Magenta
    "46": "b#00FFFF",  # Cyan
    "47": "b#FFFFFF",  # White
    # Background colors (bright intensity)
    "100": "f#555555",  # Black
    "101": "f#FF5555",  # Red
    "102": "f#55FF55",  # Green
    "103": "f#FFFF55",  # Yellow
    "104": "f#5555FF",  # Blue
    "105": "f#FF55FF",  # Magenta
    "106": "f#55FFFF",  # Cyan
    "107": "f#FFFFFF",  # White
}


# Function that takes palette data and a name or ansi code and returns an RGB ansi code
def paletteText_getRGB(palette=dict(),key=str()):
    key = key.lstrip("{")
    key = key.rstrip("}")
    hexout = ""
    for color in palette:
        if str(color) == key:
            hexout = palette[color]
            break
    else:
        for color in paletteText_standardPalette:
            if str(color) == key:
                hexout = paletteText_standardPalette[color]
                break
        else:
            return "[INVALID_PALETTE]"
    if hexout[0] == "f":
        background = False
        hexout = hexout.strip("f")
    elif hexout[0] == "b":
        background = True
        hexout = hexout.strip("b")
    else:
        background = False
    hexout = hexout.strip("#")
    lv = len(hexout)
    r,g,b = tuple(int(hexout[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
    return '\033[{};2;{};{};{}m'.format(48 if background else 38, r, g, b)

# Define a formatter function
def pt_format(palette=dict(),string=str()):
    # placeholder for reset
    string = string.replace("\033[0m","§paletteText.placeholder.reset§")
    string = string.replace("{r}","§paletteText.placeholder.reset§")
    # Match for escape characters
    pattern = r"\033\[(.*?)m"
    matches = re.findall(pattern, string)
    for match in matches:
        replaced = paletteText_getRGB(palette,match)
        if replaced != "[INVALID_PALETTE]":
            string = string.replace(f"\033[{match}m", replaced)
    # Remove placeholders
    string = string.replace("§paletteText.placeholder.reset§","\033[0m")
    # Return formatted string
    return string