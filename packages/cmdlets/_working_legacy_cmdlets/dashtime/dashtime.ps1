<#
  .SYNOPSIS
  Shows time and date.
#>
param([Alias("d")][switch]$date,[Alias("t")][switch]$timeout,[Alias("p")][switch]$pause,[Alias("day")][switch]$weekday,[Alias("w")][switch]$week)
$dashtimeDate = Get-Date
if ($date) {
  return "$dashtimeDate"
} elseif ($weekday) {
  return (get-date).DayOfWeek
} elseif ($week) {
  return "{0:d1}" -f ($(Get-Culture).Calendar.GetWeekOfYear((Get-Date),[System.Globalization.CalendarWeekRule]::FirstFourDayWeek, [DayOfWeek]::Monday))
} else {
  $dashtimeDate = $dashtimeDate.ToShortTimeString()
  return $dashtimeDate
}
if ($timeout) {Start-Sleep -s 2}
if ($pause) {pause}