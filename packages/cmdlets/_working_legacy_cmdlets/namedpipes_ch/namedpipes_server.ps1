<#
  .SYNOPSIS
  Simple namedpipes server.
#>
$npipeServer = new-object System.IO.Pipes.NamedPipeServerStream('IPC test', [System.IO.Pipes.PipeDirection]::InOut)
$npipeServer.WaitForConnection()

$pipeReader = new-object System.IO.StreamReader($npipeServer)
$script:pipeWriter = new-object System.IO.StreamWriter($npipeServer)
$pipeWriter.AutoFlush = $true
while ($text -ne "exit") {
  $text = $pipeReader.ReadLine()
  write-host "$text"
}

$npipeServer.Dispose()