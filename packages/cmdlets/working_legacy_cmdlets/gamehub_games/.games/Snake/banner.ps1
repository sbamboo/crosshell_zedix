param([string]$color)
$head = @"
`e[32m .d8888b.                    888
`e[32m 88P  Y88b                   888
`e[32m 88b.                        888
`e[32m "Y888b.   88888b.   8888b.  888  888 `e[31m .d88b. 
`e[32m    "Y88b. 888 "88b     "88b 888 .88P `e[31md8P  Y8b
`e[32m      "888 888  888 .d888888 888888K  `e[31m88888888
`e[32m 88b  d88P 888  888 888  888 888 "88b `e[31mY8b.    
`e[32m "Y8888P"  888  888 "Y888888 888  888 `e[31m "Y8888 `e[0m
"@
write-output $head
write-output "`e[$color"
write-host ""
write-host " Original game made by: nikonthethird. (This version is made by: Simon Kalmi Claesson)" -f darkgreen
write-host " Logo by Simon Kalmi Claesson" -f darkgray
write-host ""
write-host ""