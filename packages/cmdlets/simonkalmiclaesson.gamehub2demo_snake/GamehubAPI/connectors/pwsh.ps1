# Setup
$_internal_pyPath = "python3.exe"
$_internal_gamehubAPI = "$PSScriptRoot\..\gamehubAPI.py"
$_internal_quickuseAPI = "$PSScriptRoot\..\quickuseAPI.py"

# Internal Function
function _internal_RunPython($pyPath,$file,$argu) {
    $processInfo = New-Object System.Diagnostics.ProcessStartInfo
    $processInfo.FileName = $py
    $processInfo.Arguments = "$file $argu"
    $processInfo.RedirectStandardOutput = $true
    $processInfo.UseShellExecute = $false
    $process = [System.Diagnostics.Process]::Start($processInfo)
    $output = $process.StandardOutput.ReadToEnd()
    return $output
}



# Functions to commincate with the CLI access of the API
# ====================[ GamehubAPI ]====================
function requireAPI($py=$_internal_pyPath, $apiVid, $verFileOverwrite) {
    $args = ""
    if ($apiVid) { $args += "-rq_apiVid $apiVid" }
    if ($verFileOverwrite) { $args += "-rq_verFileOverwrite $verFileOverwrite" }
    return _internal_RunPython($pyPath,$_internal_gamehubAPI,$args)
}
function registerManager($py=$_internal_pyPath, $managerFile, $name, $path, $needKey=$False) {
    $args = ""
    if ($managerFile) { $args += "-mg_managerFile $managerFile" }
    if ($name) { $args += "-mg_name $name" }
    if ($path) { $args += "-mg_path $path" }
    if ($path -eq $True) { $args += "--mg_needKey" }
    return _internal_RunPython($pyPath,$_internal_gamehubAPI,$args)
}
function unregisterManager($py=$_internal_pyPath, $managerFile, $name) {
    $args = ""
    if ($managerFile) { $args += "-mg_managerFile $managerFile" }
    if ($name) { $args += "-mg_name $name" }
    return _internal_RunPython($pyPath,$_internal_gamehubAPI,$args)
}
function createTempDir($py=$_internal_pyPath) {
    $args = "--createTempDir"
    return _internal_RunPython($pyPath,$_internal_gamehubAPI,$args)
}
function deleteTempDir($py=$_internal_pyPath, $tempFolder) {
    $args = "--deleteTempDir -tf_tempFolder $tempFolder"
    return _internal_RunPython($pyPath,$_internal_gamehubAPI,$args)
}
function cleanFolder($py=$_internal_pyPath, $tempFolder) {
    $args = "--cleanFolder -tf_tempFolder $tempFolder"
    return _internal_RunPython($pyPath,$_internal_gamehubAPI,$args)
}
function saveDict($py=$_internal_pyPath, $securityLevel, $encType, $encKey, $hashType, $tempFolder, $fileName, $jsonStr) {
    $args = "--saveDict "
    if ($securityLevel) { $args += "-tf_securityLevel $securityLevel" }
    if ($encType) { $args += "-tf_encType $encType" }
    if ($encKey) { $args += "-tf_encKey $encKey" }
    if ($hashType) { $args += "-tf_hashType $hashType" }
    if ($tempFolder) { $args += "-tf_tempFolder $tempFolder" }
    if ($fileName) { $args += "-tf_fileName $fileName" }
    if ($jsonStr) { $args += "-tf_jsonStr $jsonStr" }
    return _internal_RunPython($pyPath,$_internal_gamehubAPI,$args)
}
function loadDict($py=$_internal_pyPath, $securityLevel, $encType, $encKey, $hashType, $tempFolder, $fileName, $fileHash) {
    $args = "--loadDict "
    if ($securityLevel) { $args += "-tf_securityLevel $securityLevel" }
    if ($encType) { $args += "-tf_encType $encType" }
    if ($encKey) { $args += "-tf_encKey $encKey" }
    if ($hashType) { $args += "-tf_hashType $hashType" }
    if ($tempFolder) { $args += "-tf_tempFolder $tempFolder" }
    if ($fileName) { $args += "-tf_fileName $fileName" }
    if ($fileHash) { $args += "-tf_fileHash $fileHash" }
    return _internal_RunPython($pyPath,$_internal_gamehubAPI,$args)
}
function getTOS($py=$_internal_pyPath) {
    $args = "--getTOS"
    return _internal_RunPython($pyPath,$_internal_gamehubAPI,$args)
}
function asFunction($py=$_internal_pyPath, $encType, $manager, $apiKey, $encKey, $managerFile, $ignoreManFormat, $scoreboard, $jsonData, $create=$False, $remove=$False, $get=$False, $append=$False, $doesExist=$False) {
    $args = "--asFunction "
    if ($encType) { $args += "-m_encType $encType" }
    if ($manager) { $args += "-m_manager $manager" }
    if ($apiKey) { $args += "-m_apiKey $apiKey" }
    if ($encKey) { $args += "-m_encKey $encKey" }
    if ($managerFile) { $args += "-m_managerFile $managerFile" }
    if ($ignoreManFormat) { $args += "--m_ignoreManFormat" }
    if ($scoreboard) { $args += "-m_scoreboard $scoreboard" }
    if ($jsonData) { $args += "-m_jsonData $jsonData" }
    if ($create -eq $True) { $args += "--m_create" }
    if ($remove -eq $True) { $args += "--m_remove" }
    if ($get -eq $True) { $args += "--m_get" }
    if ($append -eq $True) { $args += "--m_append" }
    if ($doesExist -eq $True) { $args += "--m_doesExist" }
    return _internal_RunPython($pyPath,$_internal_gamehubAPI,$args)
}

# ====================[ QuickuseAPI ]====================
function userData($py=$_internal_pyPath, $encType, $manager, $apiKey, $encKey, $managerFile, $ignoreManFormat=$False, $scoreboard, $user, $dictData, $saveUser=$False, $getUser=$False, $updateUser=$False, $getAllUsers=$False, $doesExist=$False) {
    $args = "--userData "
    if ($encType) { $args += "-qu_encType $encType" }
    if ($manager) { $args += "-qu_manager $manager" }
    if ($apiKey) { $args += "-qu_apiKey $apiKey" }
    if ($encKey) { $args += "-qu_encKey $encKey" }
    if ($managerFile) { $args += "-qu_managerFile $managerFile" }
    if ($ignoreManFormat -eq $True) { $args += "--qu_ignoreManFormat" }
    if ($scoreboard) { $args += "-qu_scoreboard $scoreboard" }
    if ($user) { $args += "-qu_user $user" }
    if ($dictData) { $args += "-qu_dictData $dictData" }
    if ($saveUser -eq $True) { $args += "--qu_saveUser" }
    if ($getUser -eq $True) { $args += "--qu_getUser" }
    if ($updateUser -eq $True) { $args += "--qu_updateUser" }
    if ($getAllUsers -eq $True) { $args += "--qu_getAllUsers" }
    if ($doesExist -eq $True) { $args += "--qu_doesExist" }
    return _internal_RunPython($pyPath,$_internal_quickuseAPI,$args)
}
function singleSavePrep($py=$_internal_pyPath, $tempFolder, $fileName, $encrypt, $scoreboard, $user, $data) {
    $args = "--singleSavePrep "
    if ($tempFolder) { $args += "-qu_tempFolder $tempFolder" }
    if ($fileName) { $args += "-qu_fileName $fileName" }
    if ($encrypt -eq $True) { $args += "--qu_encrypt" }
    if ($scoreboard) { $args += "-qu_scoreboard $scoreboard" }
    if ($user) { $args += "-qu_user $user" }
    if ($data) { $args += "-qu_dictData $data" }
    return _internal_RunPython($pyPath,$_internal_quickuseAPI,$args)
}
function singleSave($py=$_internal_pyPath, $encType, $manager, $apiKey, $encKey, $managerFile, $ignoreManFormat=$False, $tempFolder, $fileName, $encrypt) {
    $args = "--singleSave "
    if ($encType) { $args += "-qu_encType $encType" }
    if ($manager) { $args += "-qu_manager $manager" }
    if ($apiKey) { $args += "-qu_apiKey $apiKey" }
    if ($encKey) { $args += "-qu_encKey $encKey" }
    if ($managerFile) { $args += "-qu_managerFile $managerFile" }
    if ($ignoreManFormat -eq $True) { $args += "--qu_ignoreManFormat" }
    if ($tempFolder) { $args += "-qu_tempFolder $tempFolder" }
    if ($fileName) { $args += "-qu_fileName $fileName" }
    if ($encrypt -eq $True) { $args += "--qu_encrypt" }
    return _internal_RunPython($pyPath,$_internal_quickuseAPI,$args)
}
function singleSave_score($py=$_internal_pyPath, $encType, $manager, $apiKey, $encKey, $managerFile, $ignoreManFormat=$False, $tempFolder, $fileName, $encrypt) {
    $args = "--singleSave_score "
    if ($encType) { $args += "-qu_encType $encType" }
    if ($manager) { $args += "-qu_manager $manager" }
    if ($apiKey) { $args += "-qu_apiKey $apiKey" }
    if ($encKey) { $args += "-qu_encKey $encKey" }
    if ($managerFile) { $args += "-qu_managerFile $managerFile" }
    if ($ignoreManFormat -eq $True) { $args += "--qu_ignoreManFormat" }
    if ($tempFolder) { $args += "-qu_tempFolder $tempFolder" }
    if ($fileName) { $args += "-qu_fileName $fileName" }
    if ($encrypt -eq $True) { $args += "--qu_encrypt" }
    return _internal_RunPython($pyPath,$_internal_quickuseAPI,$args)
}
function apiConfScoreboardFunc($py=$_internal_pyPath, $apiConfPath, $scoreboard, $jsonData, $create=$False, $remove=$False, $get=$False, $append=$False, $doesExist=$False) {
    $args = "--apiConfScoreboardFunc "
    if ($apiConfPath) { $args += "-qu_apiConfPath $apiConfPath" }
    if ($scoreboard) { $args += "-qu_scoreboard $scoreboard" }
    if ($jsonData) { $args += "-qu_dictData $jsonData" }
    if ($create -eq $True) { $args += "--qu_create" }
    if ($remove -eq $True) { $args += "--qu_remove" }
    if ($get -eq $True) { $args += "--qu_get" }
    if ($append -eq $True) { $args += "--qu_append" }
    if ($doesExist -eq $True) { $args += "--qu_doesExist" }
    return _internal_RunPython($pyPath,$_internal_gamehubAPI,$args)
}
function saveServiceFunction($py=$_internal_pyPath, $apiConfPath, $linkedFile, $exitFile, $doEncrypt=$False, $verbose=$False, $simpleScore=$False) {
    $args = "--saveServiceFunction "
    if ($apiConfPath) { $args += "-ss_apiConfPath $apiConfPath" }
    if ($linkedFile) { $args += "-ss_linkedFile $linkedFile" }
    if ($exitFile) { $args += "-ss_exitFile $exitFile" }
    if ($doEncrypt -eq $True) { $args += "--ss_doEncrypt" }
    if ($verbose -eq $True) { $args += "--ss_verbose" }
    if ($simpleScore -eq $True) { $args += "--ss_simpleScore" }
    return _internal_RunPython($pyPath,$_internal_quickuseAPI,$args)
}
function saveServicePrep($py=$_internal_pyPath, $linkedFile, $doEncrypt=$False, $scoreboard, $user, $data) {
    $args = "--saveServicePrep "
    if ($linkedFile) { $args += "-ss_linkedFile $linkedFile" }
    if ($doEncrypt -eq $True) { $args += "--ss_doEncrypt" }
    if ($scoreboard) { $args += "-ss_scoreboard $scoreboard" }
    if ($user) { $args += "-ss_user $user" }
    if ($data) { $args += "-ss_data $data" }
    return _internal_RunPython($pyPath,$_internal_quickuseAPI,$args)
}
function saveService_on($py=$_internal_pyPath, $apiConfPath, $linkedFile, $exitFile, $doEncrypt=$False, $verbose=$False, $simpleScore=$False) {
    $args = "--saveService_on "
    if ($apiConfPath) { $args += "-ss_apiConfPath $apiConfPath" }
    if ($linkedFile) { $args += "-ss_linkedFile $linkedFile" }
    if ($exitFile) { $args += "-ss_exitFile $exitFile" }
    if ($doEncrypt -eq $True) { $args += "--ss_doEncrypt" }
    if ($verbose -eq $True) { $args += "--ss_verbose" }
    if ($simpleScore -eq $True) { $args += "--ss_simpleScore" }
    return _internal_RunPython($pyPath,$_internal_quickuseAPI,$args)
}
function saveService_off($py=$_internal_pyPath, $exitFile) {
    $args = "--saveService_off "
    if ($exitFile) { $args += "-ss_exitFile $exitFile" }
    return _internal_RunPython($pyPath,$_internal_quickuseAPI,$args)
}
function _ep($py=$_internal_pyPath, $inp) {
    $args = "--internal_ep "
    if ($inp) { $args += "-it_inp $inp" }
    return _internal_RunPython($pyPath,$_internal_quickuseAPI,$args)
}
function _linkFileExist($py=$_internal_pyPath, $linkedFile) {
    $args = "--internal_linkFileExist "
    if ($linkedFile) { $args += "-it_linkedFile $linkedFile" }
    return _internal_RunPython($pyPath,$_internal_quickuseAPI,$args)
}
function _getAPIConfig($py=$_internal_pyPath, $apiConfPath) {
    $args = "--internal_getAPIConfig "
    if ($linkedFile) { $args += "-it_apiConfPath $apiConfPath" }
    return _internal_RunPython($pyPath,$_internal_quickuseAPI,$args)
}