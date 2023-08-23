# Author: Simon Kalmi Claesson
# Version: 2.1
# Changelog: Added alpha support for boxMode

# [Imports]
import os
import re
import argparse
from PIL import Image

# [Config]
baseAsciiPalette = ['Ñ', '@', '#', 'W', '9', '8', '7', '6', '5', '4', '3', '2', '1', '0', '!', 'a', 'b', 'c', ';', ':', '+', '=', '-', ',', '.', '_']
baseBoxCharFg = "\u2588"
baseBoxCharBg = " "
acceptableFgKeywords = ["foreground","fore","fg"]
acceptableBgKeywords = ["background","back","bg"]
monoGradient = ["000000","010101","020202","030303","040404","050505","060606","070707","080808","090909","0a0a0a","0b0b0b","0c0c0c","0d0d0d","0e0e0e","0f0f0f","101010","111111","121212","131313","141414","151515","161616","171717","181818","191919","1a1a1a","1b1b1b","1c1c1c","1d1d1d","1e1e1e","1f1f1f","202020","212121","222222","232323","242424","252525","262626","272727","282828","292929","2a2a2a","2b2b2b","2c2c2c","2d2d2d","2e2e2e","2f2f2f","303030","313131","323232","333333","343434","353535","363636","373737","383838","393939","3a3a3a","3b3b3b","3c3c3c","3d3d3d","3e3e3e","3f3f3f","404040","414141","424242","434343","444444","454545","464646","474747","484848","494949","4a4a4a","4b4b4b","4c4c4c","4d4d4d","4e4e4e","4f4f4f","505050","515151","525252","535353","545454","555555","565656","575757","585858","595959","5a5a5a","5b5b5b","5c5c5c","5d5d5d","5e5e5e","5f5f5f","606060","616161","626262","636363","646464","656565","666666","676767","686868","696969","6a6a6a","6b6b6b","6c6c6c","6d6d6d","6e6e6e","6f6f6f","707070","717171","727272","737373","747474","757575","767676","777777","787878","797979","7a7a7a","7b7b7b","7c7c7c","7d7d7d","7e7e7e","7f7f7f","808080","818181","828282","838383","848484","858585","868686","878787","888888","898989","8a8a8a","8b8b8b","8c8c8c","8d8d8d","8e8e8e","8f8f8f","909090","919191","929292","939393","949494","959595","969696","979797","989898","999999","9a9a9a","9b9b9b","9c9c9c","9d9d9d","9e9e9e","9f9f9f","a0a0a0","a1a1a1","a2a2a2","a3a3a3","a4a4a4","a5a5a5","a6a6a6","a7a7a7","a8a8a8","a9a9a9","aaaaaa","ababab","acacac","adadad","aeaeae","afafaf","b0b0b0","b1b1b1","b2b2b2","b3b3b3","b4b4b4","b5b5b5","b6b6b6","b7b7b7","b8b8b8","b9b9b9","bababa","bbbbbb","bcbcbc","bdbdbd","bebebe","bfbfbf","c0c0c0","c1c1c1","c2c2c2","c3c3c3","c4c4c4","c5c5c5","c6c6c6","c7c7c7","c8c8c8","c9c9c9","cacaca","cbcbcb","cccccc","cdcdcd","cecece","cfcfcf","d0d0d0","d1d1d1","d2d2d2","d3d3d3","d4d4d4","d5d5d5","d6d6d6","d7d7d7","d8d8d8","d9d9d9","dadada","dbdbdb","dcdcdc","dddddd","dedede","dfdfdf","e0e0e0","e1e1e1","e2e2e2","e3e3e3","e4e4e4","e5e5e5","e6e6e6","e7e7e7","e8e8e8","e9e9e9","eaeaea","ebebeb","ececec","ededed","eeeeee","efefef","f0f0f0","f1f1f1","f2f2f2","f3f3f3","f4f4f4","f5f5f5","f6f6f6","f7f7f7","f8f8f8","f9f9f9","fafafa","fbfbfb","fcfcfc","fdfdfd","fefefe","ffffff"]
validResamplingMethods = ["NEAREST", "BOX", "BILINEAR", "HAMMING", "BICUBIC", "LANCZOS", "ANTIALIAS"]

# [Functions]
def stringPrepper(char=str,hexcode=str,background=bool,mode="pythonAnsi"):
    if mode.lower() == "pythonansi":
        # Python ansicode output
        string = f"{hexToAnsi(hexcode,background)}{char}"
    elif mode.lower() == "pansies":
        # Powershell PANSIES color output
        string = '${fg:#' + hexcode + '}' + char + '${fg:clear}'
    else:
        raise Exception("Invalid colorMode!")
    return string

def pixelAverage(pixel):
    return sum(pixel[:3]) // 3

def pixelToHexColor(pixel):
    return "{:02X}{:02X}{:02X}".format(*pixel[:3])

def hexToAnsi(hexColor, background=False):
    prefix = "\033[48;2;" if background else "\033[38;2;"
    r, g, b = int(hexColor[0:2], 16), int(hexColor[2:4], 16), int(hexColor[4:6], 16)
    return f"{prefix}{r};{g};{b}m"

def hexToMonochromeHex(hex_color):
    # Calculate the average of R, G, and B components
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    avg = (r + g + b) // 3
    # Convert the average to a hexadecimal value
    monochrome_hex = "{:02X}{:02X}{:02X}".format(avg, avg, avg)
    return monochrome_hex

def unicodeToHtmlDecimal(inputString):
    def replaceUnicode(match):
        hexDigits = match.group(2)
        decimalEntity = f'&#{int(hexDigits, 16)};'
        return decimalEntity
    unicodeEscapePattern = r'(\\\\u|\\u)([0-9A-Fa-f]{4})'
    convertedString = re.sub(unicodeEscapePattern, replaceUnicode, inputString)
    return convertedString

def unicodeToPwshUnicode(inputString):
    def replaceUnicode(match):
        hexDigits = match.group(2)
        decimalEntity = '`u{' + f"{int(hexDigits, 16)}" + "}"
        return decimalEntity
    unicodeEscapePattern = r'(\\\\u|\\u)([0-9A-Fa-f]{4})'
    convertedString = re.sub(unicodeEscapePattern, replaceUnicode, inputString)
    return convertedString

def darkenColor(hexcolor, alpha):
    # Convert hexcolor to RGB values
    r = int(hexcolor[0:2], 16)
    g = int(hexcolor[2:4], 16)
    b = int(hexcolor[4:6], 16)
    # Calculate AlphaDiff
    alpha_diff = 255 - alpha
    # Darken each color component by the AlphaDiff
    r = max(0, r - alpha_diff)
    g = max(0, g - alpha_diff)
    b = max(0, b - alpha_diff)
    # Convert the darkened RGB values back to hex
    darkened_hex = "{:02X}{:02X}{:02X}".format(r, g, b)
    return darkened_hex

def darkenColorWrap(hexcolor,alpha=None,apply=True):
    if apply == True:
        return darkenColor(hexcolor,alpha)
    else:
        return hexcolor


# [Main Function]
def ImageRenderer(image=str,type="ascii",mode=None,char=None,pc=False,method=None,invert=False,monochrome=False,width=None,height=None,resampling="lanczos",asTexture=False,colorMode="pythonAnsi",textureCodec=None):
    types = {
        "image":str,
        "type":str,
        "mode":str,
        "char":str,
        "pc":bool,
        "method":str,
        "invert":bool,
        "monochrome":bool,
        "width":int,
        "height":int,
        "resampling":str,
        "asTexture":bool,
        "colorMode":str,
        "textureCodec":str
    }
    for _var,_type in types.items():
        if locals()[_var] != None:
            if isinstance(locals()[_var],_type) != True:
                raise ValueError(f"{_var} must be of type {str(_type)}")

    # [Check Image]
    if image != None:
        if os.path.exists(image) != True:
            raise FileNotFoundError(f"Image file not found: '{image}'")

        # [Lowering some arguments]
        if isinstance(type,str) == True: type = type.lower()
        if isinstance(mode,str) == True: mode = mode.lower()
        if isinstance(method,str) == True: method = method.lower()
        if isinstance(colorMode,str) == True: colorMode = colorMode.lower()
        if isinstance(textureCodec,str) == True: textureCodec = textureCodec.lower()

        # [Set Default Values]
        # Set default rendering mode based on type
        if mode is None:
            if type == "ascii":
                mode = "standard"
            else:
                mode = "foreground"

        # Set default mapping method
        if method is None:
            method = "lum"

        # Set default characters for rendering based on type and mode
        if char is None:
            if type == "ascii":
                char = baseAsciiPalette
            elif type == "box":
                if mode in acceptableFgKeywords:
                    char = baseBoxCharFg
                elif mode in acceptableBgKeywords:
                    char = baseBoxCharBg
        else:
            if type == "ascii":
                # Parse charSet commas
                if ",,," in char.strip(" ") or ",," in char.strip(" "):
                    char = char.strip(" ")
                    char = char.replace(",,,",",\u0000,")
                    if char.endswith(",,"):
                        char = char[:len(char)-2] + ",\u0000"
                    if char.startswith(",,"):
                        char = "\u0000," + char[2:]
                # Split
                char = char.split(",")
                # Remove temp chars
                while "\u0000" in char:
                    i = char.index("\u0000")
                    char[i] = ","

        # [Load image and resize if needed]
        # Validate resampling method
        if resampling.upper() not in validResamplingMethods:
            raise ValueError(f"InvalidResampler: '{resampling}' is not a valid resampling method. Supported methods: {', '.join(validResamplingMethods)}")

        # Open the image
        image = Image.open(image)

        # Scale the image if width and/or height arguments are provided
        if width or height:
            if width and not height:
                aspectRatio = float(image.height) / float(image.width)
                newWidth = width
                newHeight = int(width * aspectRatio)
            elif height and not width:
                aspectRatio = float(image.width) / float(image.height)
                newWidth = int(height * aspectRatio)
                newHeight = height
            else:
                newWidth = width
                newHeight = height
            resampling_method = getattr(Image, resampling.upper(), Image.LANCZOS)
            image = image.resize((newWidth, newHeight), resampling_method)

        # [Handle character mapping]
        # Invert character mapping if requested
        if invert:
            char = char[::-1]

        # Reverse character array if using alpha method in ASCII mode
        if method == "alpha" and type == "ascii":
            char = char[::-1]

        # [Render / Assemble Texture]
        # Loop through image pixels and render
        outTexture = []
        charset = char
        for y in range(image.height):
            line = ""
            for x in range(image.width):
                pixel = image.getpixel((x, y))
                # ASCII
                if type == "ascii":
                    # STANDARD
                    if mode == "standard":
                        # NOPC
                        if not pc:
                            #LUM
                            if method == "lum":
                                charIndex = int(pixelAverage(pixel) / len(charset))
                            # ALPHA
                            elif method == "alpha":
                                charIndex = int(pixel[3] / len(charset))
                            char = charset[charIndex]
                        #PC (PerChar mapping)
                        else:
                            #LUM
                            if method == "lum":
                                charIndex = int(pixelAverage(pixel) / (255 / len(charset)))
                            # ALPHA
                            elif method == "alpha":
                                charIndex = int(pixel[3] / (255 / len(charset)))
                            char = charset[charIndex]
                    # COLOR
                    elif mode == "color":
                        # NOPC
                        if not pc:
                            #LUM
                            if method == "lum":
                                charIndex = int(pixelAverage(pixel) / len(charset))
                            # ALPHA
                            elif method == "alpha":
                                charIndex = int(pixel[3] / len(charset))
                        #PC (PerChar mapping)
                        else:
                            #LUM
                            if method == "lum":
                                charIndex = int(pixelAverage(pixel) / (255 / len(charset)))
                            # ALPHA
                            elif method == "alpha":
                                charIndex = int(pixel[3] / (255 / len(charset)))
                        # Get char
                        if monochrome:
                            _hex = hexToMonochromeHex(pixelToHexColor(pixel))
                            char = stringPrepper(charset[charIndex],_hex,False,colorMode)
                        else:
                            char = stringPrepper(charset[charIndex],pixelToHexColor(pixel),False,colorMode)
                    line += char
                # BOX
                elif type == "box":
                    # FOREGROUND
                    if mode == "foreground":
                        # MONO
                        if monochrome:
                            charIndex = int(pixelAverage(pixel) / (255 / len(monoGradient)))
                            #char = f"{hexToAnsi(monoGradient[charIndex])}{char}\033[0m"
                            char = stringPrepper(charset,darkenColorWrap(monoGradient[charIndex],pixel[3],method == "alpha"),False,colorMode)
                        # FullColor
                        else:
                            #char = f"{hexToAnsi(pixelToHexColor(pixel))}{char}\033[0m"
                            char = stringPrepper(charset,darkenColorWrap(pixelToHexColor(pixel),pixel[3],method == "alpha"),False,colorMode)
                    # BACKGROUND
                    elif mode == "background":
                        # MONO
                        if monochrome:
                            charIndex = int(pixelAverage(pixel) / (255 / len(monoGradient)))
                            #char = f"{hexToAnsi(monoGradient[charIndex], background=True)}{char}\033[0m"
                            char = stringPrepper(charset,darkenColorWrap(monoGradient[charIndex],pixel[3],method == "alpha"),True,colorMode)
                        # FullColor
                        else:
                            #char = f"{hexToAnsi(pixelToHexColor(pixel), background=True)}{char}\033[0m"
                            char = stringPrepper(charset,darkenColorWrap(pixelToHexColor(pixel),pixel[3],method == "alpha"),True,colorMode)
                    line += char
            # Print or append to texture
            outTexture.append(line+"\033[0m")

        # Handle codec
        newTexture = []
        if textureCodec != None:
            # Carry out action
            for line in outTexture:
                backslashers = ["uni","html","unipwsh"]
                backslash = False
                spec = textureCodec.split(":")
                if ":" in textureCodec and spec[0] in backslashers:
                    textureCodec = textureCodec.replace(f"{spec[0]}:","")
                    # unicode
                    newTexture.append( line.encode(textureCodec, 'backslashreplace').decode(textureCodec) )
                    # html
                    if spec[0] == "html":
                        newTexture.append( unicodeToHtmlDecimal(line) )
                    # unipwsh (powershell formatted unicode)
                    elif spec[0] == "unipwsh":
                        newTexture.append( unicodeToPwshUnicode(line) )
                else:
                    newTexture.append( line.encode(textureCodec, 'replace').decode(textureCodec) )
        else:
            newTexture = outTexture.copy()
        # Return texture if requested
        if asTexture:
            return newTexture
        else:
            print("\n".join(newTexture))

# CLI
if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Image to text renderer")
    parser.add_argument("-image", help="Path to the image to render")
    parser.add_argument("-type", default="ascii", help="Type of rendering (ascii or box)")
    parser.add_argument("-mode", help="Rendering mode (foreground, background, standard, color)")
    parser.add_argument("-char", help="Characters for rendering")
    parser.add_argument("-pc", action="store_true", help="Use PerChar mapping")
    parser.add_argument("-method", help="Mapping method (lum or alpha)")
    parser.add_argument("-invert", action="store_true", help="Invert character mapping")
    parser.add_argument("-monochrome", action="store_true", help="Use monochrome gradient")
    parser.add_argument("-width", type=int, help="Width for image scaling")
    parser.add_argument("-height", type=int, help="Height for image scaling")
    parser.add_argument("-resampling", default="lanczos", help="Resampling method for image scaling (lanczos, nearest, etc.)")
    parser.add_argument("-asTexture", action="store_true", help="Output the ASCII as a drawlib Texture")
    parser.add_argument("-colorMode", default="pythonAnsi", help="Colormode to use (pythonAnsi,pansies)")
    parser.add_argument("-textureCodec", help="Codec to use in the text (utf, cp1252, etc.)")
    args = parser.parse_args()
    # Execute
    returnValue = None
    mapping = {
        "image":args.image,
        "type":args.type,
        "mode":args.mode,
        "char":args.char,
        "pc":args.pc,
        "method":args.method,
        "invert":args.invert,
        "monochrome":args.monochrome,
        "width":args.width,
        "height":args.height,
        "resampling":args.resampling,
        "asTexture":args.asTexture,
        "colorMode":args.colorMode,
        "textureCodec":args.textureCodec
    }
    newMapping = dict()
    for key,value in mapping.items():
        if value != None:
            newMapping[key] = value
    returnValue = ImageRenderer(**mapping)
    if returnValue != None:
        print(returnValue)