$giturl = "https://github.com/skyline75489/exa/tree/chesterliu/dev/win-support.git"
$giturlQ = read-host "url"
if ($giturlQ -ne "") {$giturl = $giturlQ} else {echo "No giturl provided! Using default '$giturl'"}
git clone $giturl
wsl ./wsl.sh