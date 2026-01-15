@echo off
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ERROR: Ejecuta como ADMINISTRADOR.
    pause & exit /b 1
)

set "SERVICE_NAME=AetherCore2Service"
set "NSSM=%~dp0nssm.exe"

echo Deteniendo y eliminando servicio %SERVICE_NAME%...
"%NSSM%" stop %SERVICE_NAME%
"%NSSM%" remove %SERVICE_NAME% confirm

echo Proceso terminado.
pause