param([int]$week,[string]$file,[switch]$table,[string]$day,[Alias("dmode")][switch]$daymode)

write-host "Loading... `n" -f darkyellow


if ($week) {} else {$script:mathplan_week = "{0:d1}" -f ($(Get-Culture).Calendar.GetWeekOfYear((Get-Date),[System.Globalization.CalendarWeekRule]::FirstFourDayWeek, [DayOfWeek]::Monday))}
if ($mathplan_week -and ! $week) {$week = $script:mathplan_week}
if ($mathplan_file -and ! $file) {$file = $script:mathplan_file}

function indexof {param([array]$array,[string]$term); $c = 0; foreach ($i in $array) {if ($i -eq "$term") {return $c}; $c++}}

# Get data
$json = get-content "$psscriptroot\migi_preparsed.json"
$data = ConvertFrom-Json "$json"

if ($daymode) {if ($day -eq "") {$day = (get-date).DayOfWeek}}

if ($day -eq "må" -or $day -eq "monday" -or $day -eq "mo") {$day = "Måndag"}
if ($day -eq "ti" -or $day -eq "tuesday" -or $day -eq "tu") {$day = "Tisdag"}
if ($day -eq "on" -or $day -eq "wednesday" -or $day -eq "we") {$day = "Onsdag"}
if ($day -eq "to" -or $day -eq "thursday" -or $day -eq "th") {$day = "Torsdag"}
if ($day -eq "fr" -or $day -eq "friday") {$day = "Fredag"}
if ($day -eq "Sunday" -or $day -eq "Saturday") {
  write-host "Given day: $day has no plan." -f red
  exit
}

cls

$index = indexof $data."TE1 Matematik 1c" $week


[array]$tmp = $null

$tmp += $data[$index + 0]
$tmp += $data[$index + 1]
$tmp += $data[$index + 2]
$tmp += $data[$index + 3]
$tmp += $data[$index + 4]

$script:weekdatavis = $tmp | format-table
$weekdataup = $tmp

$days = $null
$desc = $null
$page = $null
$upst = $null
$upec = $null
$upca = $null
$e__1 = $null
$e__2 = $null
$e__3 = $null

foreach ($object in $weekdataup) {
    if ($object."<Column 2>") {[array]$days += $object."<Column 2>"} else {[array]$days += "§null§"}
    if ($object."<Column 3>") {[array]$desc += $object."<Column 3>"} else {[array]$desc += "§null§"}
    if ($object."<Column 4>") {[array]$page += $object."<Column 4>"} else {[array]$page += "§null§"}
    if ($object."<Column 5>") {[array]$upst += $object."<Column 5>"} else {[array]$upst += "§null§"}
    if ($object."<Column 6>") {[array]$upec += $object."<Column 6>"} else {[array]$upec += "§null§"}
    if ($object."<Column 7>") {[array]$upca += $object."<Column 7>"} else {[array]$upca += "§null§"}
    if ($object."<Column 8>") {[array]$e__1 += $object."<Column 8>"} else {[array]$e__1 += "§null§"}
    if ($object."<Column 9>") {[array]$e__2 += $object."<Column 9>"} else {[array]$e__2 += "§null§"}
    if ($object."<Column 10>") {[array]$e__3 += $object."<Column 10>"} else {[array]$e__3 += "§null§"}
}

[PSCustomObject]$script:weekdata = @{
    "week" = $week
    "days" = $days
    "lession_desc" = $desc
    "book_page" = $page
    "upg_st" = $upst
    "upg_ec" = $upec
    "upg_ca" = $upca
    "ex_1" = $e__1
    "ex_2" = $e__2
    "ex_3" = $e__3
}

ConvertTo-Json $script:weekdata | out-file "$psscriptroot\preparsed.json"

[int]$c = "lession_desc:".length

# foreach ($property in $weekdata.GetEnumerator()) {
#     $l = ":"
#     $len = ($property.name).length
#     $cl = $c - $len
#     if ($len -lt $c) {$l += " "*$cl}
#     write-host -NoNewline $property.name -f darkBlue
#     write-host -NoNewline "$l  " -f darkBlue
#     write-host $property.value -f darkgreen
# }

$upg_stArray = $null
foreach ($upgst in $weekdata.upg_st) {
  $upg_stArray += $upgst
}

function GetLongest {
  param([array]$array)
  [int]$longest = 0
  foreach ($c in $array) {
    if ([int]$longest -lt $c.length) {[int]$longest = $c.length}
  }
  return [int]$longest
}
[int]$longestUPG = GetLongest($upg_stArray)

if ($table) {
  foreach ($day in $weekdata.days) {
    [int]$i = [array]::IndexOf($weekdata.days,$day)
    $line = $day + "~" + $weekdata.lession_desc[$i] + "~" + $weekdata.book_page[$i] + "~" + $weekdata.upg_st[$i] + "~" + $weekdata.upg_ec[$i] + "~" + $weekdata.upg_ca[$i] + "~" + $weekdata.ex_1[$i] + "~" + $weekdata.ex_2[$i] + "~" + $weekdata.ex_3[$i]
    $line
  }
} else {
  if ($day -ne "") {
    [int]$i = [array]::IndexOf($weekdata.days,$day)
    write-host -nonewline "Week_" -f darkblue
    write-host -nonewline $weekdata.week -f darkblue
    write-host -nonewline ": " -f darkblue
    write-host "$day" -f darkyellow
    write-host "==================================================" -f green
    write-host -nonewline "lession_desc: " -f darkblue
    $lessdesc = "$($weekdata.lession_desc[$i])".replace('§null§',"")
    write-host $lessdesc -f darkgreen
    $bookpage = "$($weekdata.book_page[$i])".replace('§null§',"")
    write-host -nonewline "book_page:    " -f darkblue
    write-host $bookpage -f darkgreen
    $upgst = "$($weekdata.upg_st[$i])".replace('§null§',"")
    write-host -nonewline "upg_start:    " -f darkblue
    write-host $upgst -f darkgreen
    $upgec = "$($weekdata.upg_ec[$i])".replace('§null§',"")
    write-host -nonewline "upg_E-C:      " -f darkblue
    write-host $upgec -f darkgreen
    $upgca = "$($weekdata.upg_ca[$i])".replace('§null§',"")
    write-host -nonewline "upg_C-A:      " -f darkblue
    write-host $upgca -f darkgreen
    $ex1 = "$($weekdata.ex_1[$i])".replace('§null§',"")
    write-host -nonewline "extrainfo_1:  " -f darkblue
    write-host $ex1 -f darkgreen
    $ex2 = "$($weekdata.ex_2[$i])".replace('§null§',"")
    write-host -nonewline "extrainfo_2:  " -f darkblue
    write-host $ex2 -f darkgreen
    $ex3 = "$($weekdata.ex_3[$i])".replace('§null§',"")
    write-host -nonewline "extrainfo_3:  " -f darkblue
    write-host $ex3 -f darkgreen
    write-host ""
    write-host ""
  } else {
    foreach ($day in $weekdata.days) {
      [int]$i = [array]::IndexOf($weekdata.days,$day)
      write-host -nonewline "Week_" -f darkblue
      write-host -nonewline $weekdata.week -f darkblue
      write-host -nonewline ": " -f darkblue
      write-host "$day" -f darkyellow
      write-host "==================================================" -f green
      write-host -nonewline "lession_desc: " -f darkblue
      $lessdesc = "$($weekdata.lession_desc[$i])".replace('§null§',"")
      write-host $lessdesc -f darkgreen
      $bookpage = "$($weekdata.book_page[$i])".replace('§null§',"")
      write-host -nonewline "book_page:    " -f darkblue
      write-host $bookpage -f darkgreen
      $upgst = "$($weekdata.upg_st[$i])".replace('§null§',"")
      write-host -nonewline "upg_start:    " -f darkblue
      write-host $upgst -f darkgreen
      $upgec = "$($weekdata.upg_ec[$i])".replace('§null§',"")
      write-host -nonewline "upg_E-C:      " -f darkblue
      write-host $upgec -f darkgreen
      $upgca = "$($weekdata.upg_ca[$i])".replace('§null§',"")
      write-host -nonewline "upg_C-A:      " -f darkblue
      write-host $upgca -f darkgreen
      $ex1 = "$($weekdata.ex_1[$i])".replace('§null§',"")
      write-host -nonewline "extrainfo_1:  " -f darkblue
      write-host $ex1 -f darkgreen
      $ex2 = "$($weekdata.ex_2[$i])".replace('§null§',"")
      write-host -nonewline "extrainfo_2:  " -f darkblue
      write-host $ex2 -f darkgreen
      $ex3 = "$($weekdata.ex_3[$i])".replace('§null§',"")
      write-host -nonewline "extrainfo_3:  " -f darkblue
      write-host $ex3 -f darkgreen
      write-host ""
      write-host ""
    }
  }
}
