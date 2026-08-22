$OUT = "C:\Users\Lee\AppData\Local\Temp\claude\C--Users-Lee-Desktop-crownhelm\e8dc9658-0eda-4ae2-9092-6b6527c00099\scratchpad\shots"
if (-not (Test-Path $OUT)) { New-Item -ItemType Directory -Force $OUT | Out-Null }

$listener = New-Object System.Net.HttpListener
$listener.Prefixes.Add("http://localhost:8139/")
$listener.Start()
Write-Host "shotsink listening on http://localhost:8139/ -> $OUT"

while ($listener.IsListening) {
  $ctx = $listener.GetContext()
  $req = $ctx.Request
  $res = $ctx.Response
  $res.Headers.Add("Access-Control-Allow-Origin", "*")
  $res.Headers.Add("Access-Control-Allow-Headers", "*")
  $res.Headers.Add("Access-Control-Allow-Methods", "POST, OPTIONS")
  try {
    if ($req.HttpMethod -eq "OPTIONS") {
      $res.StatusCode = 200
    } elseif ($req.HttpMethod -eq "POST") {
      $reader = New-Object System.IO.StreamReader($req.InputStream, [System.Text.Encoding]::UTF8)
      $body = $reader.ReadToEnd()
      $reader.Close()
      $name = $req.Url.AbsolutePath.Trim("/")
      if (-not $name) { $name = "shot" }
      $name = ($name -replace '[^A-Za-z0-9_\-]', '_') + ".jpg"
      if ($body.StartsWith("data:")) { $b64 = $body.Substring($body.IndexOf(",") + 1) } else { $b64 = $body }
      $bytes = [System.Convert]::FromBase64String($b64)
      $path = Join-Path $OUT $name
      [System.IO.File]::WriteAllBytes($path, $bytes)
      $msg = [System.Text.Encoding]::UTF8.GetBytes("$path $($bytes.Length) bytes")
      $res.ContentType = "text/plain"
      $res.OutputStream.Write($msg, 0, $msg.Length)
    } else {
      $res.StatusCode = 405
    }
  } catch {
    $res.StatusCode = 500
    $err = [System.Text.Encoding]::UTF8.GetBytes($_.Exception.Message)
    try { $res.OutputStream.Write($err, 0, $err.Length) } catch {}
  } finally {
    $res.Close()
  }
}
