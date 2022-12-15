<#
  .SYNOPSIS
  Unofficial script for searching useblackbox.io/search from powershell.
#>
param($keyword)
$body = @{
  userId= ''
  textInput= $keyword
  source= "webapp"
} | ConvertTo-Json

$header = @{
  "Content-Type"="application/json"
  "Accept"="application/json"
} 
$response = Invoke-RestMethod -Uri "https://www.useblackbox.io/autocomplete" -Method 'Post' -Body $body -Headers $header
$answear = $response.response
return "`e[34m$answear`e[0m"