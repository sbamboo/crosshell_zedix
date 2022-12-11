#LibaryLoader by Simon Kalmi Claesson
#Ver: 2.0
#(Edited to work with this calculator)
#

function script:ReadLibary {
  param($libfile)
  #FormatHeads
  $format0head = "§Format:0" #JustCode
  $format1head = "§Format:1" #Polygott CodeLast
  $format2head = "§Format:2" #Polygott CodeLast
  $format3head = "§Format:3" #JustArchive
  $format4head = "§Format:4" #ExtendedLibraryFormat (ELF) !Reserved for the future
  #Handle
  $libfilecontent = Get-Content "$libfile"
  #Format0
  if ($libfilecontent -like "*$format0head*") {
    $tmp = $libfilecontent
    $tmp1 = ""
    foreach ($l in $tmp) {
      if ($l -notlike "*$format0head*") {
        $tmp1 += "$l`n"
      }
    }
    Invoke-Expression "$tmp1"
  }
  #Format1
  if ($libfilecontent -like "*$format1head*") {
    $tmp = $libfilecontent
    $tmp1 = ""
    $sof_found = "0"
    foreach ($l in $tmp) {
     if ($l -like "*$format1head*") {$sof_found = "1"}
     if ($sof_found -eq "1") {
       if ($l -notlike "*$format1head*") {
         $tmp1 += "$l`n"
       }
     }
    }
    if ($sof_found -ne "0") {$sof_found = "0"}
    Invoke-Expression "$tmp1"
  }
  #Format2
  if ($libfilecontent -like "*$format2head*") {
  }
  #Format3
  if ($libfilecontent -like "*$format3head*") {
  }
}