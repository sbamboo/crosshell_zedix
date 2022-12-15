<#
  .SYNOPSIS
  Cmdlet for converting from and to base32.
#>
param(
  [Parameter(ValueFromPipeline=$true)]
  [string]$in,
  [switch]$encode,
  [switch]$decode
)

if ($encode) {
  [byte[]]$bytes = [system.Text.Encoding]::Default.GetBytes($in)
  $byteArrayAsBinaryString = -join $bytes.ForEach{
    [Convert]::ToString($_, 2).PadLeft(8, '0')
  }
  $Base32Secret = [regex]::Replace($byteArrayAsBinaryString, '.{5}', {
    param($Match)
    'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567'[[Convert]::ToInt32($Match.Value, 2)]
  })
  return $Base32Secret
} elseif ($decode) {
  $secret = $in
  $bigInteger = [Numerics.BigInteger]::Zero
  foreach ($char in ($secret.ToUpper() -replace '[^A-Z2-7]').GetEnumerator()) {
    $bigInteger = ($bigInteger -shl 5) -bor ('ABCDEFGHIJKLMNOPQRSTUVWXYZ234567'.IndexOf($char))
  }
  [byte[]]$secretAsBytes = $bigInteger.ToByteArray()
  # BigInteger sometimes adds a 0 byte to the end,
  # if the positive number could be mistaken as a two's complement negative number.
  # If it happens, we need to remove it.
  if ($secretAsBytes[-1] -eq 0) {
    $secretAsBytes = $secretAsBytes[0..($secretAsBytes.Count - 2)]
  }
  # BigInteger stores bytes in Little-Endian order, 
  # but we need them in Big-Endian order.
  $bytes = $secretAsBytes[$secretAsBytes.length..0]
  $chars = $null
  foreach ($byte in $bytes) {$chars += [char]$byte}
  return $chars
}