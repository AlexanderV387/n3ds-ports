# Enciende todo lo que necesita Catequilla (Windows 11 + WSL Ubuntu).
# Uso: doble clic en encender-catequilla.bat, o ponerlo en Inicio (shell:startup)
# para que se ejecute solo al iniciar sesion.

$ErrorActionPreference = "SilentlyContinue"

function Paso($texto) { Write-Host "-> $texto" }
function Ok($texto)   { Write-Host "   OK: $texto" -ForegroundColor Green }
function Mal($texto)  { Write-Host "   FALLA: $texto" -ForegroundColor Red }

# 1. Ollama (la app de la bandeja usa las variables de C:\Ollama\models y el contexto de 65K).
Paso "Ollama"
$ollamaApp = Join-Path $env:LOCALAPPDATA "Programs\Ollama\ollama app.exe"
if (-not (Get-Process -Name "ollama app", "ollama")) {
    if (Test-Path $ollamaApp) { Start-Process $ollamaApp }
    else { Start-Process "ollama" -ArgumentList "serve" -WindowStyle Hidden }
}
$ollamaOk = $false
for ($i = 0; $i -lt 30; $i++) {
    try { Invoke-RestMethod "http://127.0.0.1:11434/api/tags" -TimeoutSec 2 | Out-Null; $ollamaOk = $true; break }
    catch { Start-Sleep -Seconds 2 }
}
if ($ollamaOk) { Ok "responde en 127.0.0.1:11434" } else { Mal "Ollama no responde: abrelo desde el menu Inicio" }

# 2. Ubuntu (WSL) y el servicio de OpenCode. La ventana oculta mantiene WSL encendido.
Paso "Ubuntu y OpenCode"
Start-Process "wsl.exe" -ArgumentList "--", "bash", "-lc", "opencode service start; sleep infinity" -WindowStyle Hidden
Start-Sleep -Seconds 8
$estado = wsl.exe -- bash -lc "opencode service status 2>&1"
Write-Host "   $estado"

# 3. Docker dentro de Ubuntu (solo hace falta para compilar).
Paso "Docker"
$docker = wsl.exe -- bash -lc "docker info >/dev/null 2>&1 && echo si || echo no"
if ($docker -match "si") { Ok "Docker funciona" }
else { Mal "Docker apagado: en Ubuntu, 'sudo service docker start' (o 'sudo systemctl enable --now docker' una vez)" }

# 4. Tailscale (para entrar desde el movil).
Paso "Tailscale"
$ts = tailscale status 2>&1 | Select-Object -First 1
if ($LASTEXITCODE -eq 0) { Ok "conectado" } else { Mal "Tailscale no conectado: abrelo desde la bandeja" }

Write-Host ""
Write-Host "Listo. Puedes cerrar esta ventana (WSL sigue encendido en segundo plano)."
Start-Sleep -Seconds 15
