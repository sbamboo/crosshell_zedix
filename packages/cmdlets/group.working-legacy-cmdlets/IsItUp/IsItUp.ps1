<#
  .SYNOPSIS
  Unofficial script for checking if a domain is up using isitup.org.
#>
param($domain)
#v1.0

#return ((iwr isitup.org/$domain).parsedhtml.body.outerText -split "`n")[1]


$text = "The domain " + (((iwr www.frogfind.com/read.php?a=https://isitup.org/$domain).content -split 'rel="nofollow">')[1] -replace '</a>','' -split '</p>')[0]
if ($text -like "*is*" -or $text -like "*seems*") {return $text} else {return "$domain is not a valid domain."}