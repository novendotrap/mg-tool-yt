@echo off
REM Lanzador para MG Tools (run.py)
REM Colocar este .bat en la misma carpeta que run.py y doble click para ejecutar.

setlocal
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

echo Iniciando MG Tools...
echo Si la ventana se cierra inmediatamente o el programa no abre,
echo toma una foto de esta consola.
echo.

where python >nul 2>&1
if %errorlevel%==0 (
    python "%SCRIPT_DIR%run.py"
    if %errorlevel% neq 0 (
        echo.
        echo [ERROR] El programa se cerro inesperadamente.
        echo Por favor, saca una captura de pantalla de estos errores y enviasela al desarrollador.
        pause
    )
    exit /b %errorlevel%
)

where py >nul 2>&1
if %errorlevel%==0 (
    py -3 "%SCRIPT_DIR%run.py"
    if %errorlevel% neq 0 (
        echo.
        echo [ERROR] El programa se cerro inesperadamente.
        echo Por favor, saca una captura de pantalla de estos errores y enviasela al desarrollador.
        pause
    )
    exit /b %errorlevel%
)

echo [ERROR CRITICO] Python no encontrado.
echo Debes instalar Python y agregarlo al PATH durante la instalacion o usar el lanzador py.
pause
exit /b 1
