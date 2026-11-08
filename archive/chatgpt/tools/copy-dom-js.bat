@echo off
setlocal
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -Command "Get-Content -Raw -LiteralPath 'scrape-dom.js' | Set-Clipboard"
if errorlevel 1 (
  echo Failed to copy. Open scrape-dom.js and copy it manually.
) else (
  echo Copied scrape-dom.js to the clipboard.
  echo Now paste it into the DevTools Console and press Enter.
)
pause
