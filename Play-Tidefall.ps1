# Play-Tidefall.ps1 — tiny static server for the game, then opens it in the browser.
# No python/node needed. Stop with Ctrl+C or just close this window.
$root = $PSScriptRoot
$port = 8137
$listener = New-Object System.Net.HttpListener
$listener.Prefixes.Add("http://localhost:$port/")
try {
    $listener.Start()
} catch {
    Write-Host "Port $port is already in use - the game server is probably already running." -ForegroundColor Yellow
    Start-Process "http://localhost:$port/Crownhelm3D.html"
    exit
}
Write-Host "Crownhelm serving $root at http://localhost:$port/ (Ctrl+C or close window to stop)" -ForegroundColor Green
Start-Process "http://localhost:$port/Crownhelm3D.html"

$mime = @{
    ".html"="text/html"; ".js"="text/javascript"; ".css"="text/css"; ".json"="application/json"
    ".png"="image/png"; ".jpg"="image/jpeg"; ".jpeg"="image/jpeg"; ".gif"="image/gif"; ".svg"="image/svg+xml"
    ".ico"="image/x-icon"; ".glb"="model/gltf-binary"; ".gltf"="model/gltf+json"
    ".mp3"="audio/mpeg"; ".ogg"="audio/ogg"; ".wav"="audio/wav"; ".woff"="font/woff"; ".woff2"="font/woff2"
}

while ($listener.IsListening) {
    $ctx = $listener.GetContext()
    $rel = [System.Uri]::UnescapeDataString($ctx.Request.Url.AbsolutePath).TrimStart('/')
    if ($rel -eq "") { $rel = "Crownhelm3D.html" }
    $path = Join-Path $root $rel
    # keep requests inside the game folder
    $full = [System.IO.Path]::GetFullPath($path)
    if ($full.StartsWith($root, [System.StringComparison]::OrdinalIgnoreCase) -and (Test-Path $full -PathType Leaf)) {
        try {
            $bytes = [System.IO.File]::ReadAllBytes($full)
            $ext = [System.IO.Path]::GetExtension($full).ToLower()
            if ($mime.ContainsKey($ext)) { $ctx.Response.ContentType = $mime[$ext] }
            $ctx.Response.ContentLength64 = $bytes.Length
            $ctx.Response.OutputStream.Write($bytes, 0, $bytes.Length)
        } catch {
            $ctx.Response.StatusCode = 500
        }
    } else {
        $ctx.Response.StatusCode = 404
    }
    $ctx.Response.Close()
}
