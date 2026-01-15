@echo off
REM ============================================
REM Instalador de Servicio AetherCore2
REM Sistema de procesamiento automático XLSX a TXT
REM ============================================

echo.
echo ============================================
echo Instalador de Servicio AetherCore2
echo ============================================
echo.

REM Verificar privilegios de administrador
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ERROR: Este script requiere privilegios de administrador
    echo.
    echo Por favor:
    echo 1. Cierra esta ventana
    echo 2. Click derecho en install_windows_service.bat
    echo 3. Selecciona "Ejecutar como administrador"
    echo.
    pause
    exit /b 1
)

echo [OK] Ejecutando con privilegios de administrador
echo.

REM Obtener directorio actual (donde esta el .bat)
set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

echo Directorio de trabajo: %CD%
echo.

REM Verificar Python
echo Verificando instalacion de Python...

python --version >nul 2>&1
if %errorLevel% equ 0 (
    set "PYTHON_CMD=python"
    for /f "tokens=*" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
    echo [OK] %PYTHON_VERSION% detectado
    goto python_found
)

py --version >nul 2>&1
if %errorLevel% equ 0 (
    set "PYTHON_CMD=py"
    for /f "tokens=*" %%i in ('py --version 2^>^&1') do set PYTHON_VERSION=%%i
    echo [OK] %PYTHON_VERSION% detectado
    goto python_found
)

echo.
echo ERROR: Python no esta instalado o no esta en el PATH
echo.
echo Instala Python 3.10+ desde: https://www.python.org/downloads/
echo IMPORTANTE: Marca "Add Python to PATH" durante la instalacion
echo.
pause
exit /b 1

:python_found
echo.

REM Verificar main.py
if not exist "main.py" (
    echo ERROR: No se encuentra main.py
    echo Asegurate de estar en la raiz del proyecto AetherCore2
    echo.
    pause
    exit /b 1
)

echo [OK] main.py encontrado
echo.

REM Crear directorios necesarios
echo Creando directorios del sistema...
if not exist "logs" mkdir logs
echo [OK] Carpeta logs creada
echo.

REM Verificar/Crear entorno virtual
if not exist "venv\Scripts\python.exe" (
    echo Creando entorno virtual...
    %PYTHON_CMD% -m venv venv
    if %errorLevel% neq 0 (
        echo ERROR: No se pudo crear el entorno virtual
        pause
        exit /b 1
    )
    echo [OK] Entorno virtual creado
    echo.
    
    echo Instalando dependencias...
    call venv\Scripts\activate
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    if %errorLevel% neq 0 (
        echo ERROR: No se pudieron instalar las dependencias
        pause
        exit /b 1
    )
    call venv\Scripts\deactivate
    echo [OK] Dependencias instaladas
    echo.
) else (
    echo [OK] Entorno virtual ya existe
    echo.
)

REM Verificar .env
echo Verificando configuracion...
if not exist ".env" (
    if exist ".env.example" (
        echo Copiando .env.example a .env...
        copy .env.example .env >nul
        echo.
        echo IMPORTANTE: Debes editar .env con tu configuracion:
        echo   - FACTURACION_BASE_PATH=C:/Facturacion
        echo   - TRANSPORTADORA=NOMBRE_TRANSPORTADORA
        echo   - LOG_LEVEL=INFO
        echo.
        set NEED_CONFIG=1
    ) else (
        echo ADVERTENCIA: No existe .env ni .env.example
        echo Debes crear manualmente el archivo .env
        set NEED_CONFIG=1
    )
) else (
    echo [OK] .env encontrado
)
echo.

if defined NEED_CONFIG (
    echo Presiona cualquier tecla cuando hayas editado .env...
    pause >nul
    echo.
)

REM Verificar NSSM
echo Verificando NSSM (Non-Sucking Service Manager)...
where nssm >nul 2>&1
if %errorLevel% neq 0 (
    echo.
    echo ============================================
    echo ERROR: NSSM no esta instalado
    echo ============================================
    echo.
    echo NSSM es necesario para instalar el servicio de Windows.
    echo.
    echo COMO INSTALAR NSSM:
    echo   1. Descarga desde: https://nssm.cc/download
    echo   2. Extrae nssm.exe
    echo   3. Copia nssm.exe a C:\Windows\System32
    echo   4. O agrega la carpeta de NSSM al PATH del sistema
    echo.
    echo ALTERNATIVA - Usar Programador de Tareas:
    echo   - Abre "Programador de tareas"
    echo   - Crea tarea basica
    echo   - Disparador: "Al iniciar el sistema"
    echo   - Accion: "%CD%\venv\Scripts\python.exe" "%CD%\main.py"
    echo.
    pause
    exit /b 1
)

echo [OK] NSSM instalado
echo.

REM Detener y eliminar servicio existente
echo Verificando servicios existentes...
nssm status AetherCore2Service >nul 2>&1
if %errorLevel% equ 0 (
    echo Servicio existente detectado. Deteniendo...
    nssm stop AetherCore2Service
    timeout /t 2 /nobreak >nul
    echo Eliminando servicio anterior...
    nssm remove AetherCore2Service confirm
    timeout /t 2 /nobreak >nul
    echo [OK] Servicio anterior eliminado
) else (
    echo [OK] No hay servicios previos
)
echo.

REM Instalar servicio
echo ============================================
echo INSTALANDO SERVICIO
echo ============================================
echo.
echo Configuracion:
echo - Nombre: AetherCore2Service
echo - Python: %CD%\venv\Scripts\python.exe
echo - Script: %CD%\main.py
echo - Directorio: %CD%
echo.

nssm install AetherCore2Service "%CD%\venv\Scripts\python.exe" "%CD%\main.py"

if %errorLevel% neq 0 (
    echo ERROR: No se pudo instalar el servicio
    pause
    exit /b 1
)
echo [OK] Servicio instalado
echo.

REM Configurar servicio
echo Configurando parametros del servicio...

nssm set AetherCore2Service AppDirectory "%CD%"
nssm set AetherCore2Service DisplayName "AetherCore2 - Procesador de Archivos Bancarios"
nssm set AetherCore2Service Description "Sistema automatico de procesamiento de archivos XLSX a TXT para liquidaciones bancarias"
nssm set AetherCore2Service Start SERVICE_AUTO_START

REM Configurar logs
nssm set AetherCore2Service AppStdout "%CD%\logs\service_stdout.log"
nssm set AetherCore2Service AppStderr "%CD%\logs\service_stderr.log"
nssm set AetherCore2Service AppStdoutCreationDisposition 4
nssm set AetherCore2Service AppStderrCreationDisposition 4
nssm set AetherCore2Service AppEnvironmentExtra "PYTHONUNBUFFERED=1"

REM Configurar rotacion de logs (10MB maximo)
nssm set AetherCore2Service AppRotateFiles 1
nssm set AetherCore2Service AppRotateOnline 1
nssm set AetherCore2Service AppRotateSeconds 86400
nssm set AetherCore2Service AppRotateBytes 10485760

REM Configurar reinicio automatico
nssm set AetherCore2Service AppExit Default Restart
nssm set AetherCore2Service AppRestartDelay 5000
nssm set AetherCore2Service AppThrottle 10000

echo [OK] Servicio configurado
echo.

REM Verificar instalacion
echo Verificando instalacion...
nssm status AetherCore2Service >nul 2>&1
if %errorLevel% neq 0 (
    echo ERROR: El servicio no se instalo correctamente
    pause
    exit /b 1
)

echo [OK] Servicio verificado
echo.

REM Resumen
echo ============================================
echo INSTALACION COMPLETADA
echo ============================================
echo.
echo El servicio "AetherCore2Service" ha sido instalado correctamente.
echo.
echo COMANDOS UTILES:
echo.
echo   Iniciar servicio:
echo     nssm start AetherCore2Service
echo     o desde Servicios de Windows (services.msc)
echo.
echo   Detener servicio:
echo     nssm stop AetherCore2Service
echo.
echo   Reiniciar servicio:
echo     nssm restart AetherCore2Service
echo.
echo   Ver estado:
echo     nssm status AetherCore2Service
echo.
echo   Editar configuracion:
echo     nssm edit AetherCore2Service
echo.
echo   Ver logs:
echo     type logs\app.log
echo     type logs\service_stdout.log
echo     type logs\service_stderr.log
echo.
echo   Eliminar servicio:
echo     nssm stop AetherCore2Service
echo     nssm remove AetherCore2Service confirm
echo.
echo ARCHIVOS IMPORTANTES:
echo   - .env                         : Configuracion (rutas, transportadora)
echo   - logs\app.log                 : Log principal del sistema
echo   - logs\service_stdout.log      : Salida estandar del servicio
echo   - logs\service_stderr.log      : Errores del servicio
echo   - logs\historial_procesamiento.csv : Historial de archivos procesados
echo.
echo ESTRUCTURA DE CARPETAS DINAMICA:
echo   %FACTURACION_BASE_PATH%\{AÑO}\{MES}\Entrada\
echo   %FACTURACION_BASE_PATH%\{AÑO}\{MES}\Salida\Procesamiento\
echo   %FACTURACION_BASE_PATH%\{AÑO}\{MES}\Salida\Transporte\
echo.
echo   Ejemplo: C:\Facturacion\2025\Enero\Entrada\
echo            C:\Facturacion\2025\Enero\Salida\Procesamiento\
echo.
echo NOTAS IMPORTANTES:
echo   - El servicio se ejecuta automaticamente al iniciar Windows
echo   - Monitorea continuamente la carpeta de entrada
echo   - Las carpetas se crean automaticamente cada mes
echo   - Revisa logs regularmente para detectar errores
echo   - Los archivos procesados generan archivos TXT con formato especifico
echo.
echo ============================================
echo.

set /p START_NOW="¿Deseas iniciar el servicio ahora? (S/N): "
if /i "%START_NOW%"=="S" (
    echo.
    echo Iniciando servicio...
    nssm start AetherCore2Service
    timeout /t 3 /nobreak >nul
    echo.
    nssm status AetherCore2Service
    echo.
    echo El servicio esta ejecutandose.
    echo Revisa los logs en: %CD%\logs\
    echo.
) else (
    echo.
    echo El servicio esta instalado pero NO iniciado.
    echo Para iniciarlo manualmente:
    echo   nssm start AetherCore2Service
    echo   o desde Servicios de Windows (services.msc)
    echo.
)

echo Presiona cualquier tecla para salir...
pause >nul