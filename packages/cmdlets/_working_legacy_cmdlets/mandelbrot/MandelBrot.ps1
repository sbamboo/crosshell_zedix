<#
  .SYNOPSIS
  Mandelbrot script from: https://til.secretgeek.net/powershell/dumb_or_fun_ideas.html
#>
param([switch]$color)
if ($color) {
  $i=[float]-16;
  $j=[float]-16;
  $r=[float]-16;
  $x=[float]-16;
  $y=[float]-16;
  #Color Array
  $colors="Black","DarkBlue","DarkGreen","DarkCyan","DarkRed","DarkMagenta","DarkYellow","Gray","DarkGray","Blue","Green","Cyan","Red","Magenta","Yellow","White"
  while(($y++) -lt 15)
  {
      for($x=0; ($x++) -lt 70; Write-Host " " -BackgroundColor ($colors[$k -band 15]) -NoNewline)
          {
              #Zero
              $i=[float]0;
              $k=[float]0;
              $r=[float]0;
              do
              {
                  #Explain to PowerShell what a complex number looks like because computers are basally stupid.
                  $j=$r*$r-$i*$i-2+$x/25; $i=2*$r*$i+$y/10; $r=$j
              }
              #Make sure the fractal doesn't draw to infinity
              while (($j*$j+$i*$i) -lt 4 -band ($k++) -lt 111)
          }
      Write-Host " "
  }
} else {
   $i=$j=$r=$x=$y=[float]-16; while(($y++) -lt 15) {for($x=0; ($x++) -lt 84; write-host (" .:-;!/>')|&IH%*#"[$k -band 15]) -nonewline){$i=$k=$r=[float]0;do{$j=$r*$r-$i*$i-2+$x/25;$i=2*$r*$i+$y/10;$r=$j} while (($j*$j+$i*$i) -lt 11 -band ($k++) -lt 111)}" "}
}