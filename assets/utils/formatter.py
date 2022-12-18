# Formatter by Simon Kalmi Claesson
#

# [Imports]
import os
import socket
import re
import getpass

# Function to format prefix
def formatPrefix(s=str(),prefix_dir=bool(),prefix_enabled=bool(),current_directory=str(),varDict=dict()):
    # Fix {dir} reserved
    cs1 = "{" + "dir" + "}"
    cs2 = "{" + "dir:"
    s = s.replace(str(cs1),"{wdir}")
    s = s.replace(str(cs2),"{wdir:")
    # replace newlines
    s = s.replace("{\\n}","\n")
    # Directory parse
    if "{wdir:" in s:
        # Fix check
        pat = '{wdir:"{wdir}"}'
        pat2 = '{wdir:"{wdir}␀"}'
        if pat in s:
            s = s.replace(pat,pat2)
        # match for dir element
        pattern = r'{wdir:([^]]+)"}'
        matchr = re.search(pattern,s)
        match = matchr.group()
        matchraw = match
        matchContent = match.lstrip("{")
        matchContent = matchContent.lstrip('wdir:"')
        matchContent = matchContent.rstrip('"}')
        # remove placeholder char
        s = s.replace("␀", "")
        matchraw = matchraw.replace("␀", "")
        matchContent = matchContent.replace("␀", "")
        # handle dir element
        if prefix_dir == True and prefix_enabled == True:
            s = s.replace(str(matchraw),str(matchContent))
            s = s.replace("{wdir}", current_directory)
        else:
            s = s.replace(str(matchraw), "")
    elif "{wdir}" in s:
        if prefix_dir == True and prefix_enabled == True:
            s = s.replace("{wdir}", current_directory)
        else:
            s = s.replace("{wdir}", "")
    # Variable parse
    pattern = r'\[([^]]+)\]'
    matches = re.finditer(pattern,s)
    for m in matches:
        o = m.group()
        n = str(o).lstrip("[")
        n = n.rstrip("]")
        # control match
        try:
            isVar = varDict[n]
        except:
            isVar = ""
        if isVar != "":
            s = s.replace(str(o),isVar)
    # Special key parse
    #s = s.replace("{user}",os.getlogin())
    s = s.replace("{user}",getpass.getuser())
    s = s.replace("{hostname}",socket.gethostname())
    # ansi key parse
    pattern = r'\{\!([^}]+)\}'
    matches = re.finditer(pattern,s)
    for m in matches:
        o = m.group()
        n = str(o).lstrip("{!")
        n = n.rstrip("}")
        s = s.replace(str(o),f"\033[{n}")
    # general key parse
    s = s.replace("{reset}","\033[0m")
    s = s.replace("{blinkoff}","\033[25m")
    s = s.replace("{blink}","\033[22m")
    s = s.replace("{boldoff}","\033[22m")
    s = s.replace("{bold}","\033[1m")
    s = s.replace("{hiddenoff}","\033[28m")
    s = s.replace("{hidden}","\033[8m")
    s = s.replace("{reverseoff}","\033[27m")
    s = s.replace("{reverse}","\033[7m")
    s = s.replace("{italicoff}","\033[23m")
    s = s.replace("{italic}","\033[3m")
    s = s.replace("{underlineoff}","\033[24m")
    s = s.replace("{underline}","\033[4m")
    s = s.replace("{strikethroughoff}","\033[29m")
    s = s.replace("{strikethrough}","\033[9m")
    # powershell compatability presets (HardCoded on python)
    s = s.replace("{formataccent}","\033[32;1m")
    s = s.replace("{tableheader}","\033[32;1m")
    s = s.replace("{erroraccent}","\033[36;1m")
    s = s.replace("{error}","\033[31;1m")
    s = s.replace("{warning}","\033[33;1m")
    s = s.replace("{verbose}","\033[33;1m")
    s = s.replace("{debug}","\033[33;1m")
    s = s.replace("{p.style}","\033[33;1m")
    s = s.replace("{fi.directory}","\033[44;1m")
    s = s.replace("{fi.symboliclink}","\033[36;1m")
    s = s.replace("{fi.executable}","\033[32;1m")
    # unicode key parse
    pattern = r'\{u.([^}]+)\}'
    matches = re.finditer(pattern,s)
    for m in matches:
        o = m.group()
        n = str(o).lstrip("{u.")
        n = n.rstrip("}")
        r = eval(f"chr(0x{n})")
        s = s.replace(str(o),str(r))
    # Colors
    s = s.replace("{f.black}","\033[30m")
    s = s.replace("{f.darkgray}","\033[90m")
    s = s.replace("{f.gray}","\033[37m")
    s = s.replace("{f.white}","\033[97m")
    s = s.replace("{f.darkred}","\033[31m")
    s = s.replace("{f.red}","\033[91m")
    s = s.replace("{f.darkmagenta}","\033[35m")
    s = s.replace("{f.magenta}","\033[95m")
    s = s.replace("{f.darkblue}","\033[34m")
    s = s.replace("{f.blue}","\033[94m")
    s = s.replace("{f.darkcyan}","\033[36m")
    s = s.replace("{f.cyan}","\033[96m")
    s = s.replace("{f.darkgreen}","\033[32m")
    s = s.replace("{f.green}","\033[92m")
    s = s.replace("{f.darkyellow}","\033[33m")
    s = s.replace("{f.yellow}","\033[93m")

    s = s.replace("{b.black}","\033[40m")
    s = s.replace("{b.darkgray}","\033[100m")
    s = s.replace("{b.gray}","\033[47m")
    s = s.replace("{b.white}","\033[107m")
    s = s.replace("{b.darkred}","\033[41m")
    s = s.replace("{b.red}","\033[101m")
    s = s.replace("{b.darkmagenta}","\033[45m")
    s = s.replace("{b.magenta}","\033[105m")
    s = s.replace("{b.darkblue}","\033[44m")
    s = s.replace("{b.blue}","\033[104m")
    s = s.replace("{b.darkcyan}","\033[46m")
    s = s.replace("{b.cyan}","\033[106m")
    s = s.replace("{b.darkgreen}","\033[42m")
    s = s.replace("{b.green}","\033[102m")
    s = s.replace("{b.darkyellow}","\033[43m")
    s = s.replace("{b.yellow}","\033[103m")
    s = s.replace("{r}","\033[0m")
    # hex key parse
    pattern = r'\{\#([^}]+)\}'
    matches = re.finditer(pattern,s)
    for m in matches:
        o = m.group()
        n = str(o).lstrip("{#")
        if n[0] == "!":
            n = n.lstrip("!")
            background = True
        else:
            background = False
        n = n.rstrip("}")
        lv = len(n)
        r,g,b = tuple(int(n[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
        ansi = '\033[{};2;{};{};{}m'.format(48 if background else 38, r, g, b)
        s = s.replace(str(o),ansi)
    # RGB key parse
    pattern = r'\{rgb.([^}]+)\}'
    matches = re.finditer(pattern,s)
    for m in matches:
        o = m.group()
        n = str(o).lstrip("{rgb.")
        n = n.rstrip("}")
        r,g,b = n.split(";")
        ansi = '\033[{};2;{};{};{}m'.format(48 if background else 38, r, g, b)
        s = s.replace(str(o),ansi)
    # Return string
    return s