import re

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
        retString = f"[INVALID_KEY:{key}]"
        return retString
    # Get RGB of hex
    hexout = hexout.strip("#")
    lv = len(hexout)
    r,g,b = tuple(int(hexout[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
    return f'\033[38;2;{r};{g};{b}m'

# Define a formatter function
def pt_format(palette=dict(),string=str()):
    # placeholder for reset
    string = string.replace("\033[0m","§paletteText.placeholder.reset§")
    string = string.replace("{r}","§paletteText.placeholder.reset§")
    # Match for escape characters
    pattern = r"\033\[(.*?)m"
    matches = re.findall(pattern, string)
    for match in matches:
        string = string.replace(f"\033[{match}m", paletteText_getRGB(palette,match))
    # Match for colorNames
    pattern = r"\{.*\}"
    matches = re.findall(pattern, string)
    for match in matches:
        string = string.replace(match, paletteText_getRGB(palette,match))
    # Remove placeholders
    string = string.replace("§paletteText.placeholder.reset§","\033[0m")
    # Return formatted string
    return string