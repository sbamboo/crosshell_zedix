#Image to text renderer
#Made by Simon kalmi claesson
#

# Docs:
# THIS SCRIPT REQUIRES THE "Pansies" MODULE FOR COLORS! INSTALL WITH: "Install-Module Pansies -AllowClobber"
#
# Some parameters are always required:
# 'image':  The image to render 
# 'invert': This reverses the character set so inverts mappings.
#
# This script has two executionTypes that work with paramaters diffrently:
# "ascii" and "box", which one is used is defined by the 'type' parameter, the default is 'ascii'
# 
# When using ascii parameters work like this:
# 'mode':   Sets how the rendering works, can be "standard" for monochrome output and "color" for colored output, the default is "standard"
# 'char':   This sets a list of characters to be mapped. With low amounts of characters use PerChar mapping or there might be blank spots.
# 'pc':     Short for PerChar, switch, makes sure mappings are per char and not per level (this ensure that no blank spots exists where charcters could not be mapped)
# 'method': The mapping method either "lum" for luminocity, or "alpha" for opacity (lum: low-lumen=smal-char, alpha: low-opac=smal-char)
# 
# When using box paramaters work like this:
# 'mode':   Sets how the rendering works, can be "foreground" or "background", depending on which layer to color.
# 'char':   This can be only a string and will be used as char, so if multiple chars it will map each pixel to al chars.
# 'monochrome': Works like ascii mode standard.

#Param Handling
param (
  #Image
  [string]$image,
  #Type
  [string]$type,
  #mode
  [string]$mode,
  #char
  [string]$char,
  #PerChar (PC)
  [switch]$pc,
  #method
  [string]$method,
  #invert
  [switch]$invert,
  #monochrome
  [switch]$monochrome,
  #Operation (Non Used)
  [string]$op,


  #HelpMenu
  [switch]$help,

  #ExternalBitmapCreator
  [string]$ExtBitmap
)

#NoImage
if ("$image" -eq "") {
  $help = $true
}

#Built in variables
$version = "Beta 1.2"
[array]$def_densChars = 'Ñ','@','#','W','9','8','7','6','5','4','3','2','1','0','!','a','b','c',';',':','+','=','-',",",".",'_'
[array]$monoGradient = "000000","010101","020202","030303","040404","050505","060606","070707","080808","090909","0a0a0a","0b0b0b","0c0c0c","0d0d0d","0e0e0e","0f0f0f","101010","111111","121212","131313","141414","151515","161616","171717","181818","191919","1a1a1a","1b1b1b","1c1c1c","1d1d1d","1e1e1e","1f1f1f","202020","212121","222222","232323","242424","252525","262626","272727","282828","292929","2a2a2a","2b2b2b","2c2c2c","2d2d2d","2e2e2e","2f2f2f","303030","313131","323232","333333","343434","353535","363636","373737","383838","393939","3a3a3a","3b3b3b","3c3c3c","3d3d3d","3e3e3e","3f3f3f","404040","414141","424242","434343","444444","454545","464646","474747","484848","494949","4a4a4a","4b4b4b","4c4c4c","4d4d4d","4e4e4e","4f4f4f","505050","515151","525252","535353","545454","555555","565656","575757","585858","595959","5a5a5a","5b5b5b","5c5c5c","5d5d5d","5e5e5e","5f5f5f","606060","616161","626262","636363","646464","656565","666666","676767","686868","696969","6a6a6a","6b6b6b","6c6c6c","6d6d6d","6e6e6e","6f6f6f","707070","717171","727272","737373","747474","757575","767676","777777","787878","797979","7a7a7a","7b7b7b","7c7c7c","7d7d7d","7e7e7e","7f7f7f","808080","818181","828282","838383","848484","858585","868686","878787","888888","898989","8a8a8a","8b8b8b","8c8c8c","8d8d8d","8e8e8e","8f8f8f","909090","919191","929292","939393","949494","959595","969696","979797","989898","999999","9a9a9a","9b9b9b","9c9c9c","9d9d9d","9e9e9e","9f9f9f","a0a0a0","a1a1a1","a2a2a2","a3a3a3","a4a4a4","a5a5a5","a6a6a6","a7a7a7","a8a8a8","a9a9a9","aaaaaa","ababab","acacac","adadad","aeaeae","afafaf","b0b0b0","b1b1b1","b2b2b2","b3b3b3","b4b4b4","b5b5b5","b6b6b6","b7b7b7","b8b8b8","b9b9b9","bababa","bbbbbb","bcbcbc","bdbdbd","bebebe","bfbfbf","c0c0c0","c1c1c1","c2c2c2","c3c3c3","c4c4c4","c5c5c5","c6c6c6","c7c7c7","c8c8c8","c9c9c9","cacaca","cbcbcb","cccccc","cdcdcd","cecece","cfcfcf","d0d0d0","d1d1d1","d2d2d2","d3d3d3","d4d4d4","d5d5d5","d6d6d6","d7d7d7","d8d8d8","d9d9d9","dadada","dbdbdb","dcdcdc","dddddd","dedede","dfdfdf","e0e0e0","e1e1e1","e2e2e2","e3e3e3","e4e4e4","e5e5e5","e6e6e6","e7e7e7","e8e8e8","e9e9e9","eaeaea","ebebeb","ececec","ededed","eeeeee","efefef","f0f0f0","f1f1f1","f2f2f2","f3f3f3","f4f4f4","f5f5f5","f6f6f6","f7f7f7","f8f8f8","f9f9f9","fafafa","fbfbfb","fcfcfc","fdfdfd","fefefe","ffffff"

if ($isLinux -eq "$true") {
  $isUnix = "$true"
} elseif ($isMacOS -eq "true") {
  $isUnix = "$true"
} elseif ($isWindows -ne "true") {
  $isUnix = "$true"
} else {
  $isUnix = "$false"
}

#Param fix
  #char
  [array]$char = $char -split " "
  #DollarSignError Fix
  foreach ($c in $char) {
    if ("$c" -notlike "*$*") {
      [array]$charO += $c
    }
  }
  [array]$char = $charO
  #ExternalBitmapCreator
  if ("$isUnix" -eq "$true") {
    if ("$ExtBitmap" -eq "") {
      write-host "On unix systems the -ExtBitmap parameter must be given with a bitmap extractor class for unixsupport." -f $host.privatedata.errorforegroundcolor -b $host.privatedata.errorbackgroundcolor
      break
    }
  }

#Param Defaulting
  #type
  if ("$type" -eq "") {[string]$type = "ascii"}
  #mode
  if ("$mode" -eq "") {
    if ("$type" -eq "ascii") {[string]$mode = "standard"}
    if ("$type" -eq "box") {[string]$mode = "foreground"}
  }
  #char
  if ("$char" -eq "") {
    if ("$type" -eq "ascii") {[array]$char = [array]$def_densChars}
    if ("$type" -eq "box") {
        if ("$mode" -eq "foreground") {[string]$char = "█"}
        if ("$mode" -eq "background") {[string]$char = " "}
    }
  }
  #pc
  if ("$pc" -eq "") {[string]$pc = $false}
  #method
  if ("$method" -eq "") {[string]$method = "lum"}
  #invert
  if ("$invert" -eq "") {[string]$invert = $false}
  #monochrome
  if ("$monochrome" -eq "") {[string]$monochrome = $false}

#ImageTester
#$imageValid = Test-Path $image
if ($imageValid -eq "$false") {
  write-host "Image: $image was not valid, or dosen't exist" -f $host.privatedata.errorforegroundcolor -b $host.privatedata.errorbackgroundcolor
  break
}


#  ImageRender   -image <path>   -type <rendertype>   -mode <rendertype.box.mode/ascii.mode>   -char <rendertype.box.mode.foreground.char>   -pc <rendertype.ascii.pc>   -method <rendertype.ascii.mode.color.method>   -op <operation>   -ExtBitmap <BitMapClass>
#   -image (mandatory)
#   -type (def: ascii)
#   -mode ({type.ascii}def: ascii.standard;  {type.box}def: box.foreground)
#   -char ({type.ascii}def: $array.densChars;  {type.box}def: "█")
#   -op   (def: "")
#   [type.ascii]
#   -pc (def: false, switch)
#   -method (def: lum) [parent: type.ascii.mode.color]

#HelpMenu
if ($help) {
    write-host "Image renderer $version Help:" -f darkYellow
    write-host "------------------------------" -f darkYellow
    break
}

#Rendering Code
  #Create Bitmap (Windows only) other modules with switch "-ExtBitmap"
  if ($extBitmap -ne "") {
      #Use your own
      $stringBuild = $extBitmap + '((Get-Item ' + $image + ').fullname)'
      $BitMap = iex($stringBuild)
  } else {
      #Windows
      $BitMap = [System.Drawing.Bitmap]::FromFile((Get-Item $image).fullname)
  }
  #densChar
  if ("$type" -eq "ascii") {
    if ($invert) { [array]$char = $char[$char.length..0] }
  }

  #DrawLoop

  # If method is alpha charArray should be reversed to work properly (lowOpacity = smalCharacter)
  if ("$method" -eq "alpha" -and "$type" -eq "ascii") {
    [array]$char = $char[$char.length..0]
  }

  $interP = ""
  $dChar = ""
  #CreateLine
  foreach ($y in (1..($BitMap.Height-1))) {
    $line = ""
    foreach ($x in (1..($BitMap.Width-1))) {
      #GetPixelData
        #RGB Color
        $rgb = $BitMap.GetPixel($X,$Y) | select R,G,B
        #Lumnance/Alpha
        $alpha = $BitMap.GetPixel($X,$Y).A
        $lum = [math]::Round(($rgb.r +$rgb.g + $rgb.b) / 3)
        #PCValues
        if ($pc) {
          $PCvalue = [math]::round(255/$char.length)
        }
        #HexColor
        if ($monochrome) {
          $hexColor = $monoGradient[$lum]
        } else {
          if ($BitMap.GetPixel($X,$Y).name -eq "0") {
            $noChar = $true
            $hexColor = "000000"
          } else {
            $noChar = $false
            $hexColor = $BitMap.GetPixel($X,$Y).name.Substring(2)
          }
        }
      #characterHandling
        #BoxMode
        if ("$type" -eq "box") {
          #SetColor
          if ("$mode" -eq "foreground") {
            #foreground
            $interP = '"${fg:#' + $hexColor + '}' + $char + '${fg:clear}"'
          } elseif ("$mode" -eq "background") {
            #background
            $interP = '"${bg:#' + $hexColor + '}' + $char + '${bg:clear}"'
          }
          #Create Line
          $line += iex($interP)
        }
        #AsciiMode
        if ("$type" -eq "ascii") {
          #ColorModes
          if ("$mode" -eq "standard") {
            #StandardMode
            if ("$pc" -ne "$true") {
              #No PC
              if ("$method" -eq "lum") {
                #Lum
                $dChar = $char[[math]::floor($lum/$char.length)]
              } elseif ("$method" -eq "alpha") {
                #Alpha
                $dChar = $ichar[[math]::floor($alpha/$char.length)]
              }
            } elseif ("$pc" -eq "$true") {
              #PC
              if ("$method" -eq "lum") {
                #Lum
                $dChar = $char[[math]::floor($lum/$PCvalue)]
              } elseif ("$method" -eq "alpha") {
                #Alpha
                $dChar = $char[[math]::floor($alpha/$PCvalue)]
              }
            }
            #CreateLine
            $line += $dChar
          } elseif ("$mode" -eq "color") {
            #ColorMode
            if ("$pc" -ne "$true") {
              #No PC
              if ("$method" -eq "lum") {
                #Lum
                $dChar = $char[[math]::floor($lum/$char.length)]
                $interP = '"${fg:#' + $hexColor + '}' + $dChar + '${fg:clear}"'
              } elseif ("$method" -eq "alpha") {
                #Alpha
                $dChar = $char[[math]::floor($alpha/$char.length)]
                $interP = '"${fg:#' + $hexColor + '}' + $dChar + '${fg:clear}"'
              }
            } elseif ("$pc" -eq "$true") {
              #PC
              if ("$method" -eq "lum") {
                #Lum
                $dChar = $char[[math]::floor($lum/$PCvalue)]
                $interP = '"${fg:#' + $hexColor + '}' + $dChar + '${fg:clear}"'
              } elseif ("$method" -eq "alpha") {
                #Alpha
                $dChar = $char[[math]::floor($alpha/$PCvalue)]
                $interP = '"${fg:#' + $hexColor + '}' + $dChar + '${fg:clear}"'
              }
            }
            #CreateLine
            $line += iex($interP)
          }
        }
    }
    write-host "$line"
  }