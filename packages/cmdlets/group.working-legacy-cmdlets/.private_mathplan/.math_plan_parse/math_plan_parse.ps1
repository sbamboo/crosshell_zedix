params($file)
write-host "Parsing... `n" -f darkyellow

if (get-module PSExcel) {} else {Install-module PSExcel}
import-module psexcel -force

if ($file) {} else {echo "`e[31mNo filename given to the file param`e[0m"}
$script:mathplan_file = "$psscriptroot\Matematik M2_2023.xlsx"

$data = import-xlsx $script:mathplan_file

#print
$json = ConvertTo-Json $data
$json = $json -replace "null",'"§null§"'
$json | out-file "migi_preparsed.json"