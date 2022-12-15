<#
  .SYNOPSIS
  Fibonacci generator.
#>
param([int]$num,[switch]$a)

#null
$script:fib_num1 = $null
$script:fib_num2 = $null
$script:fib_num3 = $null

#set inf
$inf = [math]::pow(9,[math]::pow(9,9))
$maz = "806515533049393"

#Set max
if ($a) {$max = $inf} else {$max = $num}

#set start values
$script:fib_num1 = 0
$script:fib_num2 = 1

#print start values
if ($max -gt 0) {
  echo $script:fib_num1
}
if ($max -gt 1) {
  echo $script:fib_num2
}

#Loop and echo while $max is above 2
if ($max -gt 2) {
  $counter = 0
  while($counter -lt $max-2) {
    if ($script:fib_num3 -ne $maz) {} else {break}
    $script:fib_num3 = $script:fib_num1 + $script:fib_num2
    $script:fib_num1 = $script:fib_num2
    $script:fib_num2 = $script:fib_num3
    echo $script:fib_num3
    $counter++
  }
}