<#
  .SYNOPSIS
  Simple namedpipes client.
#>
$ComputerName = '.'
$npipeClient = new-object System.IO.Pipes.NamedPipeClientStream($ComputerName, 'IPC test', [System.IO.Pipes.PipeDirection]::InOut, [System.IO.Pipes.PipeOptions]::None, [System.Security.Principal.TokenImpersonationLevel]::Impersonation)
$pipeReader = $null
$pipeWriter = $null
$npipeClient.Connect()

$pipeReader = new-object System.IO.StreamReader($npipeClient)
$pipeWriter = new-object System.IO.StreamWriter($npipeClient)
$pipeWriter.AutoFlush = $true

while (1) {
  cls
  [string]$text = read-host "ts"
  $pipeWriter.WriteLine($text)
  if ($text -eq "exit") {
    $npipeClient.Dispose()
    break
  }
}