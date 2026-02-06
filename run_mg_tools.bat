@echo off
REM Lanzador para MG Tools (run.py)
REM Colocar este .bat en la misma carpeta que run.py y doble click para ejecutar.

setlocal
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

REM Preferir pythonw (sin consola) y lanzarlo con start para desacoplar la ventana.
where pythonw >nul 2>&1
if %errorlevel%==0 (
    start "" pythonw "%SCRIPT_DIR%run.py"
    exit /b 0
)

REM Si no hay pythonw, usar PowerShell Start-Process para lanzar python sin bloquear el .bat.
where python >nul 2>&1
if %errorlevel%==0 (
    powershell -NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -Command "Start-Process -FilePath 'python' -ArgumentList '\"%SCRIPT_DIR%run.py\"' -WorkingDirectory '%SCRIPT_DIR%'"
    exit /b 0
)

REM Finalmente intentar con py -3 (launcher)
where py >nul 2>&1
if %errorlevel%==0 (
    powershell -NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -Command "Start-Process -FilePath 'py' -ArgumentList '-3 \"%SCRIPT_DIR%run.py\"' -WorkingDirectory '%SCRIPT_DIR%'"
    exit /b 0
)

echo Python no encontrado. Instale Python y agreguelo al PATH o use el lanzador py.
pause
exit /b 1
