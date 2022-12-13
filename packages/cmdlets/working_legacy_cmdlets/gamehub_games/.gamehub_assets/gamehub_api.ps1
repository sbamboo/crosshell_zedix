# API for pantry made by Simon Kalmi Claesson for gamehub_games
# I simon (the author) remain in ownership of this file and it's content. You are not allowed to share or use this file with out my permission.
#

# Function to encrypt and decrypt string
function encdec {
  param([Parameter(ValueFromPipeline=$true)][string]$inputstring,[switch]$enc,[switch]$dec)
  if ($enc) {
    $encstring = pwsh -command "convertto-securestring '$inputstring' -asplaintext -force | convertfrom-securestring"
    #write-host "$encstring"
    return $encstring
  } elseif ($dec) {
    $rawstring = pwsh -command "'$inputstring' | convertto-securestring | convertfrom-securestring -asplaintext"
    #write-host "$rawstring"
    return $rawstring
  }
}

# Settings
$iid = encdec "c96b7120-d350-4ac1-af69-1bee5f3554d3" -enc

# Function to generate string hash
function gamehub_stringhash {
  param([string]$string,[string]$algorithm)
  if ("$string" -ne "") {
    if ("$algorithm" -eq "") {$algorithm = "SHA256"}
    $mystream = [IO.MemoryStream]::new([byte[]][char[]]$string)
    $hash = Get-FileHash -InputStream $mystream -Algorithm "$algorithm"
    return $hash
  }
}

# Function to generate file hash
function gamehub_filehash {
  param([string]$file,[string]$algorithm)
  if ("$file" -ne "") {
    if ("$algorithm" -eq "") {$algorithm = "SHA256"}
    $hash = pwsh -command "Get-FileHash '$file' -Algorithm $algorithm"
    return $hash
  }
}

# Function to test string hash with file
function gamehub_gfile_hash {
  param([string]$string)
  $file = "hash.tmp"
  $cl = get-location
  cd $psscriptroot
  if (test-path $file) {rm $file -force}
  "$string" | out-file -file "$file"
  $hash = pwsh -command "(Get-FileHash '$file' -Algorithm SHA256).hash"
  rm $file -force
  return $hash
}

# Terms Of Use handler
function gamehub_checkTos {
  $tosfile = "$psscriptroot\..\..\..\..\assets\gamehub_api_tos.txt"
  $checkfile = "$psscriptroot\tosaccepted.txt"
  $exi = Test-Path $checkfile
  if (!$exi) {
    $webtos = (Invoke-WebRequest "https://raw.githubusercontent.com/simonkalmiclaesson/CrossShell/main/assets/gamehub_api_tos.txt").Content
    if ($webtos -eq "") {
      if (test-path "$tosfile") {
        get-content "$tosfile"
      } else {
        $webtos | out-file "$tosfile"
        write-host "$webtos"
      }
    } else {
      $webtos | out-file "$tosfile"
      write-host "$webtos"
    }
    Write-Host "Do you accept the agrements above? (A yes means you have read all the agreements) [y/n] " -NoNewline
    $c = Read-Host
    if ($c -eq "y") {
      "True" | out-file $checkfile
      cls
    } else {
      exit
    }
  }
}

# Web request handler for the pantry http api
function pantryapi {
  param([string]$id,[string]$method,[string]$body,[string]$basket)
  if ($basket) {
    if ($body) {
      $ans = Invoke-WebRequest -Uri "https://getpantry.cloud/apiv1/pantry/$id/basket/$basket" -Method "$method" -ContentType 'application/json' -body "$body"
    } else {
      $ans = Invoke-WebRequest -Uri "https://getpantry.cloud/apiv1/pantry/$id/basket/$basket" -Method "$method" -ContentType 'application/json'
    }
  } else {
    if ($body) {
      $ans = Invoke-WebRequest -Uri "https://getpantry.cloud/apiv1/pantry/$id" -Method "$method" -ContentType 'application/json' -body "$body"
    } else {
      $ans = Invoke-WebRequest -Uri "https://getpantry.cloud/apiv1/pantry/$id" -Method "$method" -ContentType 'application/json'
    }
  }
  return $ans
}


# Abstraction layer for better understanding and easier access to the pantry api
function pantryapireq {
  param(
    [string]$key,
    [string]$basket,
    [string]$json,

    [switch]$getall,
    [switch]$get,
    [switch]$append,
    [switch]$create,
    [switch]$replace
  )
  if ($getall) {
    $ans = pantryapi "$key" GET
  }
  if ($get) {
    $ans = pantryapi "$key" GET -basket "$basket"
  }
  if ($append) {
    $ans = pantryapi "$key" PUT -basket "$basket" -body "$json"
  }
  if ($create -or $replace) {
    if ($body) {
      $ans = pantryapi "$key" POST -basket "$basket" -body "$json"
    } else {
      $ans = pantryapi "$key" POST -basket "$basket"
    }
  }
  return $ans
}



# Gamehub function for handling, setting and updating scores on gamehub games. ( Authorised games/users only )
function gamehub_userScore {
  <#
    .DESCRIPTION
    Internal function for GameHub to handle and view scores.
  #>
  param([string]$game,[string]$user,[string]$score,[switch]$create,[switch]$update,[switch]$get,[switch]$getscores)
  #check tos
  gamehub_checkTos
  #create user score
  if ($create) {
    if ($user -eq "") {break}
    if ($score -eq "") {break}
    $json = @"
    {
      "$user": "$score"
    }
"@
    $old_erroractionpreference = $erroractionpreference
    $erroractionpreference = "SilentlyContinue"
    $error.clear()
    $id = encdec "$iid" -dec
    $ans = pantryapireq "$id" -basket "$game" -json "$json" -create
    $id = $null
    $erroractionpreference = $old_erroractionpreference
    [string]$lasterror = $error[0]
    if ($lasterror -ne "") {
      return $lasterror
    } else {
      $content = $ans.content
      return $content
    }
  }
  #update user score
  if ($update) {
    if ($user -eq "") {break}
    if ($score -eq "") {break}
    $json = @"
    {
      "$user": "$score"
    }
"@
    $old_erroractionpreference = $erroractionpreference
    $erroractionpreference = "SilentlyContinue"
    $error.clear()
    $id = encdec "$iid" -dec
    $ans = pantryapireq "$id" -basket "$game" -json "$json" -append
    $id = $null
    $erroractionpreference = $old_erroractionpreference
    [string]$lasterror = $error[0]
    if ($lasterror -ne "") {
      return $lasterror
    } else {
      $content = $ans.content
      return $content
    }
  }
  #get user score
  if ($get) {
    $old_erroractionpreference = $erroractionpreference
    $erroractionpreference = "SilentlyContinue"
    $error.clear()
    $id = encdec "$iid" -dec
    $ans = pantryapireq "$id" -basket "$game" -get
    $id = $null
    $erroractionpreference = $old_erroractionpreference
    [string]$lasterror = $error[0]
    if ($lasterror -ne "") {
      return $lasterror
    } else {
      $json = $ans.content
      $content = ConvertFrom-Json $json
      $userdata = $content."$user"
      return $userdata
    }
  }
  #get all scores
  if ($getscores) {
    $old_erroractionpreference = $erroractionpreference
    $erroractionpreference = "SilentlyContinue"
    $error.clear()
    $id = encdec "$iid" -dec
    $ans = pantryapireq "$id" -get -basket "$game"
    $id = $null
    $erroractionpreference = $old_erroractionpreference
    [string]$lasterror = $error[0]
    if ($lasterror -ne "") {
      return $lasterror
    } else {
      $json = $ans.content
      $data = ConvertFrom-Json "$json"
      return $data
    }
  }
}

# Function to generate working dir
function gamehub_generateworkdir {
  function returnRandomString($len) {
    [string]$randoms = "abcdefghijklmnopqrstuvwxyz0123456789_".ToCharArray() | get-random -count $len
    return $randoms.Replace(" ","")
  }
  $foldername = returnRandomString 40
  $cl = Get-Location
  set-location $env:temp
  if (test-path $foldername) {
    while (test-path $foldername) {
      $foldername = returnRandomString 40
    }
  }
  mkdir $foldername
  set-location $foldername
  $workdirpath = Get-Location
  set-location $cl
  return "$workdirpath"
}

# Function to set hardcoded workdir
function add_abs_workdir {
  $fol = $env:temp
  $randoms = "egh9a20w3lvq87us4txjozn5y1r_d6icfbkpm"
  if (test-path "$fol\$randoms") {} else { cd $fol; mkdir $randoms }
  return "$fol\$randoms"
}

# Functions remove hardcoded workdir
function rem_abs_workdir {
  $workdir = add_abs_workdir
  remove-item $workdir -confirm:$false -force -Recurse
}

# Function to encrypt and decrypt file
function gamehub_filehand {
  param([string]$file,[string]$string,[string]$datalocation,[switch]$abs,[switch]$enc,[switch]$dec)
  if ($abs) {
    $dataLocation = add_abs_workdir
  }
  $cl = Get-Location
  if (test-path $dataLocation) {
    Set-Location $datalocation
    $exi = test-path "$file"
    if (!$exi) {"" | out-file "$file"}
    if (test-path $file) {
      # Encrypt
      if ($enc) {
        $encryptedString = encdec "$string" -enc
        #write-host "$encryptedString $file $pwd"
        $encryptedString | out-file "$file"
      }
      # Decrypt
      if ($dec) {
        $rawcontent = get-content "$file"
        $unencryptedstring = encdec "$rawcontent" -dec
        return $unencryptedstring
      }
    }
  }
  set-location $cl
}



# Function to start the gamehub save service
function gamehub_saveService_on {
  param([string]$dataLocation,[string]$dataFile,[switch]$abs,[switch]$dodebug)
  if ($abs) {
    $dataLocation = add_abs_workdir
  }
  if ("$dodebug" -eq "$true") {
    [string]$command = "start pwsh {-command " + "$psscriptroot" + "\gamehub_api_saveService.ps1 -loc " + '"' + "$dataLocation" + '"' + " -datafile " + '"' + "$dataFile" + '"}'
  } else {
    [string]$command = "start pwsh {-command " + "$psscriptroot" + "\gamehub_api_saveService.ps1 -loc " + '"' + "$dataLocation" + '"' + " -datafile " + '"' + "$dataFile" + '"} -WindowStyle Minimized'
  }
  #[string]$command = "start pwsh {-command echo '$dataLocation $dataFile'; pause}"
  iex ($command)
}

# Function to close the gamehub save service
function gamehub_saveService_off {
  "" | out-file "$psscriptroot\exit.state"
}

# Function to save score once
function gamehub_singlesave {
  param([string]$file,[string]$location,[switch]$abs)
  if ($abs) {
    $dataLocation = add_abs_workdir
  }
  $cl = Get-Location
  Set-Location $location
  if (test-path $dataLocation) {
    Set-Location $dataLocation
    if (test-path "$file") {
      $scoreData = gamehub_filehand -file "$file" -abs -dec
      #write-host "$scoreData";pause
      [array]$scoreDataA = $scoreData -split ' : '
      $user = $scoreDataA[0]
      [int]$newScore = $scoreDataA[-1]
      [int]$lastScore = gamehub_userScore -game "snake" -user "$user" -get
      if ($newScore -gt $lastScore) {
        $ans = gamehub_userScore -game "snake" -user "$user" -score "$newScore" -update
        $lastScore = $newScore
        write-host "[Debug] Wrote new score '$newScore' for user '$user'" -f yellow
      }
      if (test-path "$file") {
        rm "$file" -Force
      }
    } else {
      write-host "No score found, did something break, or was the game quit early?" -f darkgray
    }
  } else {
    write-host "Internal datalocation for score saving not found." -f red
  }
  Set-Location $cl
}

# Function to simple save
function gamehub_simpleSaveHandle([int]$score) {
  # start childprocess whom saves the score
  
}