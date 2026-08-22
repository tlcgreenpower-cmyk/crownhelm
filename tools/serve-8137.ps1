$root = "C:\Users\Lee\Desktop\crownhelm"
$listener = New-Object System.Net.HttpListener
$listener.Prefixes.Add("http://localhost:8137/")
$listener.Start()
Write-Host "Serving $root on http://localhost:8137/"

$mime = @{
  ".html"="text/html"; ".js"="application/javascript"; ".css"="text/css"
  ".glb"="model/gltf-binary"; ".gltf"="model/gltf+json"; ".png"="image/png"
  ".jpg"="image/jpeg"; ".jpeg"="image/jpeg"; ".bin"="application/octet-stream"
  ".json"="application/json"; ".ico"="image/x-icon"; ".mp3"="audio/mpeg"; ".wav"="audio/wav"
  ".svg"="image/svg+xml"; ".webp"="image/webp"; ".ogg"="audio/ogg"
}

while ($listener.IsListening) {
  $ctx = $listener.GetContext()
  $req = $ctx.Request
  $res = $ctx.Response
  try {
    $res.Headers.Add("Cache-Control", "no-store, no-cache, must-revalidate")
    $path = [System.Uri]::UnescapeDataString($req.Url.AbsolutePath)
    if ($path -eq "/") { $path = "/Crownhelm3D.html" }
    $full = Join-Path $root ($path.TrimStart("/"))
    $full = [System.IO.Path]::GetFullPath($full)
    if (-not $full.StartsWith([System.IO.Path]::GetFullPath($root))) {
      $res.StatusCode = 403; $res.Close(); continue
    }
    if (Test-Path $full -PathType Leaf) {
      $ext = [System.IO.Path]::GetExtension($full).ToLower()
      $ct = $mime[$ext]; if (-not $ct) { $ct = "application/octet-stream" }
      $res.ContentType = $ct
      $bytes = [System.IO.File]::ReadAllBytes($full)
      $res.ContentLength64 = $bytes.Length
      $res.OutputStream.Write($bytes, 0, $bytes.Length)
    } else {
      $res.StatusCode = 404
    }
  } catch {
    $res.StatusCode = 500
  } finally {
    try { $res.Close() } catch {}
  }
}
