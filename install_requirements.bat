@echo off
REM install_requirements.bat
REM Instala dependencias desde requirements.txt usando el Python disponible.
REM Este script asume que el usuario instalará Python por separado si no está presente.

setlocal
set SCRIPT_DIR=%~dp0
set REQ=%SCRIPT_DIR%requirements.txt

if not exist "%REQ%" (
    echo ERROR: no se encontró "requirements.txt" en %SCRIPT_DIR%
    echo Copia este archivo al mismo directorio que este .bat y vuelve a intentarlo.
    pause
    exit /b 1
)

echo Instalando dependencias desde "%REQ%" ...

REM Intentar usar el lanzador 'py' (recomendado en Windows)
where py >nul 2>&1
if %errorlevel%==0 (
    echo Usando el lanzador 'py'...
    py -3 -m pip install --user -r "%REQ%"
    if %errorlevel%==0 goto done
)

REM Intentar usar 'python'
where python >nul 2>&1
if %errorlevel%==0 (
    echo Usando 'python'...
    python -m pip install --user -r "%REQ%"
    if %errorlevel%==0 goto done
)

REM Intentar usar 'pip' directamente
where pip >nul 2>&1
if %errorlevel%==0 (
    echo Usando 'pip'...
    pip install --user -r "%REQ%"
    if %errorlevel%==0 goto done
)

echo.
echo No se encontró un Python utilizable ni pip en el PATH.
echo Por favor instala Python desde: https://www.python.org/downloads/ y asegúrate de marcar "Add Python to PATH" o usa el lanzador 'py'.
echo Luego vuelve a ejecutar este archivo.
pause
exit /b 1

:done
echo.
echo Dependencias instaladas correctamente (instalacion por usuario: --user).
echo Para ejecutar la aplicacion use: run_mg_tools.bat
pause
exit /b 0
