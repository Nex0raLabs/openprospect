@echo off
setlocal
cd /d "%~dp0"
if not exist .venv\Scripts\python.exe (
  py -3 -m venv .venv
  if errorlevel 1 goto error
)
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
python -m pip install -e ".[mcp]"
if errorlevel 1 goto error
if not exist .env copy .env.example .env
openprospect dashboard
goto end
:error
echo Installation failed. Check the error above.
pause
:end
endlocal
