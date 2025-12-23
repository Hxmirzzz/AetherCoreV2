# AetherCore2 – Procesamiento de Archivos Bancarios

## Descripción

**AetherCore 2** es una aplicación modular en Python diseñada para:

- Monitorear una carpeta de entrada en tiempo real.
- Procesar archivos `.xlsx` con conceptos de **Procesamiento** y **Transporte**.
- Aplicar limpieza avanzada de datos eliminando tildes, caracteres especiales y normalizando texto.
- Generar automáticamente archivos `.txt` separados por tipo, respetando formatos estrictos y codificación UTF-8.
- Mantener un registro detallado de eventos y errores.
- Cumplir principios SOLID para fácil mantenimiento y extensibilidad.

---

## Funcionalidades

### Procesamiento de Datos
- Lee archivos `.xlsx` desde la carpeta de entrada.
- Aplica formato limpio y validaciones por tipo de dato (`fecha`, `decimal2`, `decimal4`, `porcentaje`, etc.).
- **Limpieza avanzada de texto**: Elimina automáticamente tildes, diacríticos y caracteres especiales de columnas de texto, manteniendo la integridad de datos numéricos y fechas.
- Convierte porcentajes, fechas y decimales al formato exigido.
- Valida columnas requeridas y columnas críticas antes de exportar.

### Exportación y Validación
- Genera archivos `.txt` para cada concepto, separados por carpeta (`Procesamiento` / `Transporte`).
- Valida si el archivo `.txt` ya existe antes de exportar.
- Verifica estructura de datos y tipos de columnas.
- Logging centralizado con niveles configurables (`DEBUG`, `INFO`, etc.).

### Arquitectura
- Separación de responsabilidades en módulos (`io`, `core`, `processors`).
- Configuración mediante archivo `.env` para rutas dinámicas.
- Diccionario de mapeos centralizado para transformacion de datos.
- Historial de procesamiento en CSV para auditoría.

---

## Estructura del Proyecto

```
AetherCore2/
├── main.py                          # Punto de entrada
├── processors/
│   └── xlsx_to_txt_converter.py     # Lógica principal de procesamiento
├── src/
│   ├── core/
│   │   ├── cleaning.py              # Limpieza básica de DataFrames
│   │   ├── text_cleaner.py          # Limpieza avanzada: tildes y caracteres especiales
│   │   ├── data_mappings.py         # Diccionario de mapeos origen -> destino
│   │   ├── config.py                # Configuración y carga de .env
│   │   ├── expected_columns.py      # Columnas requeridas por hoja
│   │   ├── file_operations.py       # Orquestación general del flujo
│   │   ├── history_log.py           # Registro histórico por archivo
│   │   ├── logger_config.py         # Configuración de logger
│   │   ├── monitor.py               # Monitoreo de la carpeta de entrada
│   │   ├── schema_validator.py      # Validación estructural y crítica
│   │   ├── tipos_columnas.py        # Tipos de datos por columna
│   │   ├── validators.py            # Validadores específicos
│   │   └── text_cleaner.py          # Limpiador de texto
│   └── io/
│       ├── formatter.py             # Transformación y limpieza de columnas
│       ├── naming.py                # Generación de nombre de archivo final
│       ├── pathing.py               # Rutas dinámicas de entrada/salida
│       ├── reader.py                # Lectura de archivos Excel
│       └── writer.py                # Exportación a .txt
├── logs/                            # Carpeta donde se almacenan los logs
├── .env.example                     # Plantilla de configuración
├── requirements.txt                 # Librerías necesarias
└── README.md                        # Este archivo
```

---

## Procesamiento de Datos

AetherCore 2 implementa un sistema de procesamiento de datos en tres etapas:

### 1. Mapeo de Datos (`data_mappings.py`)
**Primera etapa del procesamiento** - Transforma valores de origen (Excel) a valores estándar de destino (TXT):

- **Sistema centralizado**: Diccionario configurable por tipo de hoja y columna
- **Comparación robusta**: Case-insensitive para mayor tolerancia a variaciones
- **Auditable**: Registra en logs todas las transformaciones realizadas
- **Preservación de datos**: Si no existe mapeo, mantiene el valor original

#### Ejemplo de Mapeos Actuales (PROCESAMIENTO - TIPO_SERVICIO):
```
Origen (Excel)                           → Destino (TXT)
─────────────────────────────────────────────────────────────
ALMACENAMIENTO BILLETE                   → ALMACENAMIENTO
ALMACENAMIENTO MONEDA                    → ALMACENAMIENTO
CLASIFICACION EFECTIVO FAJADO (ALTA)     → CLASIFICACION
CLASIFICACION EFECTIVO FAJADO (BAJA)     → CLASIFICACION
VERIFICACION DE MONEDAS                  → VERIFICACION
PAQUETEO BANCO REPUBLICA                 → PAQUETEO
```

**Nota**: Los mapeos se aplican **antes** de cualquier limpieza de texto, permitiendo capturar valores con tildes o caracteres especiales exactamente como aparecen en el Excel.

### 2. Limpieza Básica (`cleaning.py`)
- Elimina espacios múltiples y caracteres invisibles (saltos de línea, tabs).
- Normaliza valores nulos (`nan`, `NaN`, `None`, `NULL`).

### 3. Limpieza Avanzada de Texto (`text_cleaner.py`)
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
        "TIPO_SERVICIO": {
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
        "TIPO_SERVICIO": {
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