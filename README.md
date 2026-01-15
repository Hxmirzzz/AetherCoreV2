# AetherCore2 – Procesamiento de Archivos Bancarios

## Descripción

**AetherCore 2** es una herramienta profesional para el monitoreo y procesamiento automático de archivos bancarios. Diseñada para funcionar de forma autónoma como un servicio de Windows, transforma archivos .xlsx en formatos .txt estandarizados sin intervención humana.

---

## Funcionalidades Principales

- **Monitoreo Inteligente**: Detecta archivos nuevos (on_created) y actualizaciones de archivos existentes (on_modified).
- **Portabilidad Total**: Ejecutable autónomo que no requiere instalación de Python ni librerías en el computador de destino.
- **Servicio de Windows**: Integración con NSSM para ejecución ininterrumpida en segundo plano.
- **Limpieza Avanzada**: Normalización de texto (sin tildes ni caracteres especiales) y validación estricta de tipos de datos.

---

## Arquitectura y Estructura

El proyecto utiliza una arquitectura de rutas dinámicas que detecta si la aplicación corre como script o como ejecutable empaquetado, asegurando que los logs y configuraciones siempre se ubiquen junto a la aplicación.

```
AetherCore2/
├── main.py                          # Punto de entrada del monitor
├── scripts/                         # Automatización de despliegue
│   ├── install_service.bat          # Registro de servicio portátil
│   └── uninstall_service.bat        # Eliminación del servicio
├── src/
│   ├── core/                        # Lógica de negocio y monitoreo
│   └── io/                          # Lectura, escritura y formateo
├── .env                             # Configuración de rutas locales
└── logs/                            # Auditoría y trazabilidad
```

---

## Implementación y Despliegue

### Modo Portátil (Recomendado para Producción)
Para entornos sin Python instalado:

1. **Compilación**: Generar el ejecutable usando PyInstaller:
   ```bash
   pyinstaller --onefile --windowed --name AetherCore2 main.py
   ```

2. **Preparación de Carpeta**: Colocar en una misma ubicación:
   - AetherCore2.exe
   - nssm.exe
   - .env (configurado con las rutas del cliente)

3. **Instalación**: Ejecutar `scripts/install_service.bat` como Administrador.

### Modo Desarrollo
1. Instalar dependencias: `pip install -r requirements.txt`
2. Ejecutar monitor: `python main.py`

## Flujo de Procesamiento

1. **Detección**: El sistema vigila la carpeta de entrada definida en `.env`.
2. **Mapeo y Limpieza**: Aplica transformaciones de `data_mappings.py` y remueve caracteres no permitidos.
3. **Validación**: Verifica esquemas y tipos de columnas críticas antes de exportar.
4. **Exportación**: Genera archivos `.txt` en UTF-8 con la nomenclatura requerida por el cliente.
5. **Historial**: Registra cada operación en `logs/historial_procesamiento.csv` para auditoría.

## Mantenimiento

- **Logs**: Consultar `logs/app.log` para depuración de la lógica y `service_stderr.log` para errores del servicio de Windows.
- **Nomenclatura**: Los nombres de archivos siguen el formato estricto `LIQ_{TIPO}{TRANSPORTADORA}{BANCO}{DDMMAAAA}.txt`.
- **Licencia**: MIT 2025 Hamir Rocha.

### 2. Limpieza Básica (`cleaning.py`)
- Elimina espacios múltiples y caracteres invisibles (saltos de línea, tabs).
- Normaliza valores nulos (`nan`, `NaN`, `None`, `NULL`).

Aplica transformaciones específicas a columnas de texto:
- **Eliminación de tildes y diacríticos**: "Bogotá" → "Bogota"
- **Normalización Unicode**: Convierte caracteres especiales a ASCII
- **Filtrado de caracteres**: Solo permite letras, números y símbolos comunes (`.`, `,`, `-`, `#`, `(`, `)`, `/`)
- **Espacios**: Elimina múltiples espacios y recorta extremos

**Importante**: La limpieza de texto se aplica **solo** a columnas sin formato numérico o de fecha especificado, preservando la integridad de datos críticos.

---

## Configuración de Mapeos

Para agregar o modificar mapeos de datos, edita el archivo `src/core/data_mappings.py`:

```python
MAPEOS_DATOS = {
    "PROCESAMIENTO": {
        "NOMBRE_TIPO_SERVICIO": {
            "VALOR_ORIGEN_1": "VALOR_DESTINO_1",
            "VALOR_ORIGEN_2": "VALOR_DESTINO_2",
            # Agregar más mapeos aquí...
        },
        # Para mapear otra columna:
        "OTRA_COLUMNA": {
            "ORIGEN_A": "DESTINO_A",
            "ORIGEN_B": "DESTINO_B",
        }
    },
    "TRANSPORTE": {
        # Mapeos futuros para la hoja Transporte
        "NOMBRE_TIPO_SERVICIO": {
            "ORIGEN_X": "DESTINO_X",
        }
    }
}
```

### Ventajas del Sistema de Mapeos
- **Centralizado**: Todos los mapeos en un solo archivo fácil de mantener
- **Extensible**: Agregar nuevas columnas o valores sin modificar código de procesamiento
- **Auditable**: Cada transformación se registra en el logger con estadísticas detalladas
- **Flexible**: Soporta múltiples columnas por tipo de hoja

---

## Configuración `.env`

Ejemplo básico del archivo `.env` para funcionamiento local:

```env
# Ruta base
FACTURACION_BASE_PATH=C:/Facturacion

# Carpetas de entrada/salida (pueden ser subcarpetas dentro de la base)
INPUT_FOLDER=${FACTURACION_BASE_PATH}/Entrada
OUTPUT_FOLDER=${FACTURACION_BASE_PATH}/Salida

# Nivel de logs: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_LEVEL=DEBUG

# Nombre fijo de la transportadora
TRANSPORTADORA=TRANSPORT
```

---

## Ejecución

### Procesamiento manual (un solo archivo):

```bash
python processors/xlsx_to_txt_converter.py --input C:/Facturacion/Entrada/archivo.xlsx
```

### Modo automático (monitoreo continuo):

```bash
python main.py
```

El sistema detectará nuevos `.xlsx` que se copien a la carpeta de entrada y generará automáticamente sus `.txt` correspondientes.

---

## Formato de Salida

Los archivos `.txt` generados cumplen con:
- **Codificación**: UTF-8 sin BOM
- **Separador**: Coma (`,`)
- **Fechas**: `DD/MM/YYYY`
- **Decimales**: Precisión fija (2 o 4 decimales según columna)
- **Porcentajes**: Valores enteros (ej: `10` para 10%)
- **Texto**: Sin tildes ni caracteres especiales
- **Valores Mapeados**: Transformación de valores de origen a valores estándar de destino

### Convención de nombres:
```
LIQ_{TIPO}{TRANSPORTADORA}{BANCO}{DDMMAAAA}.txt
```

Ejemplo: `LIQ_PROCESAMIENTOTRANSPORTBANCO01012025.txt`

---

## Validaciones Implementadas

1. **Validación de Esquema**: Verifica que existan todas las columnas requeridas
2. **Validación de Columnas Críticas**: Asegura que columnas obligatorias no estén vacías
3. **Validación de Tipos**: Confirma que fechas, números y decimales tengan formato correcto
4. **Detección de Columnas Extra**: Advierte sobre columnas no reconocidas sin detener el proceso
5. **Validación de Mapeos**: Asegura que valores mapeados existen en el diccionario

---

## Requisitos

- Python 3.10+
- Dependencias listadas en `requirements.txt`

### Instalación:

```bash
pip install -r requirements.txt
```

---

### Dependencias principales:
- `pandas`: Manipulación de datos
- `openpyxl`: Lectura de archivos Excel
- `watchdog`: Monitoreo de archivos en tiempo real
- `python-dotenv`: Gestión de variables de entorno

---

## Logs y Auditoría

### Archivo de Log (`logs/app.log`)
Registra todos los eventos del sistema con rotación automática (5MB máximo):
- Detección de nuevos archivos
- Inicio y finalización de procesamiento
- Errores y advertencias
- Tiempo de ejecución

### Historial de Procesamiento (`logs/historial_procesamiento.csv`)
Mantiene un registro CSV con:
- Fecha y hora de proceso
- Archivo original
- Acrónimo del banco
- Tipo de hoja procesada
- Número de filas y columnas
- Archivo de salida generado
- Estado (EXITO / ERROR)
- Mensaje de error (si aplica)

---

## Seguridad

- `.env` protegido con `.gitignore`
- Validación de columnas críticas antes de exportar
- Conversión segura con `try/except` y errores claros en logs
- Sin exposición de credenciales o rutas sensibles
- Mapeos configurables sin hardcoding en logica de negocio

---

## Extensibilidad

Gracias a la arquitectura modular, puedes:
- **Agregar nuevos mapeos** en `data_mappings.py` sin modificar código de procesamiento
- Agregar nuevos tipos de validación en `validators.py`
- Incluir nuevos formatos de columna en `tipos_columnas.py`
- Extender reglas de limpieza en `text_cleaner.py`
- Implementar nuevos tipos de hoja en `expected_columns.py`

---

## Licencia

MIT © 2025 Hamir Rocha