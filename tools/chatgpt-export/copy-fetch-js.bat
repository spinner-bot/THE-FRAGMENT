@echo off
setlocal
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -Command "Get-Content -Raw -LiteralPath 'fetch-conversation.js' | Set-Clipboard"
if errorlevel 1 (
  echo Failed to copy. Open fetch-conversation.js and copy it manually.
) else (
  echo Copied fetch-conversation.js to the clipboard.
  echo Now paste it into the DevTools Console and press Enter.
)
pause
