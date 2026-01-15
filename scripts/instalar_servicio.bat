@echo off
setlocal enabledelayedexpansion

:: Verificar privilegios de administrador
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ERROR: Por favor, ejecuta este script como ADMINISTRADOR.
    pause & exit /b 1
)

:: Obtener ruta y ELIMINAR la barra invertida final para evitar el error de comillas
set "APP_DIR=%~dp0"
if "%APP_DIR:~-1%"=="\" set "APP_DIR=%APP_DIR:~0,-1%"

set "EXE_NAME=AetherCore2.exe"
set "SERVICE_NAME=AetherCore2Service"
set "NSSM=%APP_DIR%\nssm.exe"

cd /d "%APP_DIR%"

echo ============================================
echo Instalando AetherCore2 como Servicio
echo ============================================

:: 1. Verificar archivos esenciales
if not exist "%EXE_NAME%" (echo ERROR: No se encuentra %EXE_NAME% & pause & exit /b 1)
if not exist "nssm.exe" (echo ERROR: No se encuentra nssm.exe & pause & exit /b 1)
if not exist ".env" (echo ADVERTENCIA: No se encuentra el archivo .env & pause)

:: 2. Instalar el servicio
:: Usamos barras explicitas para evitar el error de escape \"
"%NSSM%" stop %SERVICE_NAME%
"%NSSM%" remove %SERVICE_NAME% confirm
"%NSSM%" install %SERVICE_NAME% "%APP_DIR%\%EXE_NAME%"
"%NSSM%" set %SERVICE_NAME% AppDirectory "%APP_DIR%"
"%NSSM%" set %SERVICE_NAME% DisplayName "AetherCore2 - Procesador de Archivos"
"%NSSM%" set %SERVICE_NAME% Description "Monitoreo y procesamiento automatico de archivos XLSX a TXT"
"%NSSM%" set %SERVICE_NAME% Start SERVICE_AUTO_START

:: 3. Configurar Logs del servicio
if not exist "logs" mkdir logs
"%NSSM%" set %SERVICE_NAME% AppStdout "%APP_DIR%\logs\service_stdout.log"
"%NSSM%" set %SERVICE_NAME% AppStderr "%APP_DIR%\logs\service_stderr.log"
"%NSSM%" set %SERVICE_NAME% AppRotateFiles 1
"%NSSM%" set %SERVICE_NAME% AppRotateBytes 10485760

:: 4. Iniciar servicio
echo Iniciando el servicio...
"%NSSM%" start %SERVICE_NAME%

echo.
echo ============================================
echo INSTALACION COMPLETADA
echo ============================================
"%NSSM%" status %SERVICE_NAME%
pause