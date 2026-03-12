# ScrapeCraft

Plantilla open source para construir web scrapers de forma facil y rapida. Basada en [SeleniumBase](https://github.com/seleniumbase/SeleniumBase), un framework de automatizacion con soporte integrado para evasion de deteccion.

## Proposito

ScrapeCraft busca ser un punto de partida para cualquier persona que quiera aprender web scraping o construir sus propios scrapers para **fines educativos y divertidos**. La plantilla esta disenada para ser:

- **Facil de usar**: Configura tu scraper editando archivos YAML y Python, sin tocar el codigo principal
- **Flexible**: Soporta multiples formatos de salida (CSV, JSON, XML, Excel)
- **Robusta**: Incluye sistema de logging, manejo de errores y evasion de deteccion

## Estructura

```
ScrapeCraft/
├── src/                      # Codigo fuente
│   ├── main.py               # Orquestacion principal
│   ├── scraper.py            # Logica de extraccion de datos
│   ├── process.py            # Transformacion de datos (raw → procesado)
│   ├── storage.py            # Almacenamiento y exportacion
│   ├── driver_config.py      # Configuracion del driver
│   └── logger.py             # Sistema de logging
├── config/                   # Configuraciones
│   ├── settings.py           # Config del driver, datos, logging y raw
│   └── web_config.yaml       # URL, selectores y waits
├── tests/                    # Tests de validacion
│   └── test_config.py
├── log/                      # Logs de ejecucion
├── raw/                      # Archivos de datos en bruto (intermedios)
├── output/                   # Archivos generados (resultado final)
├── requirements.txt
├── CHANGELOG.md
└── LICENSE
```

## Arquitectura

El proyecto sigue el principio de **separacion de responsabilidades**:

```
main.py (Orquestacion)
    │
    ├── load_web_config()     # Carga config/web_config.yaml
    │
    ├── scraper.py
    │   └── scrape()          # Extrae datos de la web
    │
    ├── storage.py
    │   ├── save_raw()        # Guarda datos en bruto como CSV (raw/)
    │   ├── cleanup_raw()     # Limpia raw/ segun politica de retencion
    │   ├── build_filepath()  # Construye rutas segun naming_mode
    │   └── save_data()       # Exporta a CSV/JSON/XML/Excel (output/)
    │
    └── process.py
        └── process()         # Transforma datos: raw → procesado
```

### Modulos

| Modulo | Responsabilidad |
|--------|-----------------|
| `main.py` | Orquestacion del flujo completo y del reprocesamiento |
| `scraper.py` | Logica de extraccion: navegar, manejar CAPTCHA, extraer elementos |
| `process.py` | Transformacion de datos entre el raw y el guardado final |
| `storage.py` | Persistencia: raw, cleanup, construir rutas, exportar en multiples formatos |
| `driver_config.py` | Inicializacion del navegador con opciones anti-deteccion |
| `logger.py` | Sistema de logging dual (archivo + consola) |

## Instalacion

```bash
git clone https://github.com/tu-usuario/ScrapeCraft.git
cd ScrapeCraft
pip install -r requirements.txt
```

## Configuracion

### Driver (`config/settings.py`)

```python
DRIVER_CONFIG = {
    "headless": False,      # Ejecutar sin interfaz grafica
    "undetected": True,     # Modo anti-deteccion
    "maximize": True,       # Maximizar ventana
    "window_size": None,    # Tamano especifico: (1920, 1080)
    "user_agent": None,     # User agent personalizado
    "proxy": None           # Proxy: "ip:puerto"
}
```

### Logging (`config/settings.py`)

```python
LOG_CONFIG = {
    "log_folder": "log",    # Carpeta de logs
    "level": "INFO"         # Nivel: DEBUG, INFO, WARNING, ERROR
}
```

Los logs se guardan en `log/scrapecraft_YYYYMMDD.log` y tambien se muestran en consola.

### Datos (`config/settings.py`)

Configuraciones independientes para cada formato de exportacion:

```python
DATA_CONFIG = {
    "csv": {
        "encoding": "utf-8-sig",
        "separator": ",",
        "index": False
    },
    "json": {
        "indent": 2,
        "force_ascii": False,
        "orient": "records"
    },
    "xml": {
        "root": "registros",
        "row": "registro"
    },
    "xlsx": {
        "sheet_name": "Datos",
        "index": False
    }
}
```

Uso en codigo:

```python
from src.storage import save_data

# Exportar a un formato
save_data(datos, "csv", settings.DATA_CONFIG, settings.STORAGE_CONFIG)

# Exportar a multiples formatos
for formato in ["csv", "json", "xlsx"]:
    save_data(datos, formato, settings.DATA_CONFIG, settings.STORAGE_CONFIG)
```

### Almacenamiento (`config/settings.py`)

Configura donde y como se guardan los archivos:

```python
STORAGE_CONFIG = {
    "output_folder": "output",
    "filename": "viviendas",
    "naming_mode": "date_suffix",
    "output_formats": ["csv"]  # Opciones: "csv", "json", "xml", "xlsx"
}
```

Para exportar a múltiples formatos simultáneamente:
```python
"output_formats": ["csv", "json", "xlsx"]
```

#### Modos de nombrado (`naming_mode`)

| Modo | Resultado | Uso |
|------|-----------|-----|
| `overwrite` | `output/viviendas.csv` | Sobrescribe siempre |
| `date_suffix` | `output/viviendas_20260130.csv` | Una ejecucion por dia |
| `timestamp_suffix` | `output/viviendas_20260130_143052.csv` | Multiples ejecuciones por dia |
| `date_folder` | `output/20260130/viviendas.csv` | Organizar por carpetas |

### Web (`config/web_config.yaml`)

```yaml
url: "https://ejemplo.com"

xpath_selectors:
  container: '//div[@class="item"]'
  Campo1: './/span[@class="dato1"]'
  Campo2: './/span[@class="dato2"]'

waits:
  reconnect_attempts: 3
  after_load: 5
```

## Uso

```bash
# Ejecutar flujo completo (scraping + procesamiento + guardado)
python -m src.main

# Reprocesar una ejecucion anterior sin volver a scrapear
python -m src.main --reprocess <SUFFIX>

# Ejecutar tests
pytest tests/ -v
```

### Flujo completo

Ejecuta todas las etapas en orden:

```
scrape() → save_raw() → del datos → process() → cleanup_raw() → save_data()
```

1. Extrae datos de la web y los guarda en `raw/` como CSV con sufijo timestamp
2. Libera la memoria del raw y aplica las transformaciones definidas en `process.py`
3. Limpia archivos antiguos de `raw/` segun la politica de retencion configurada
4. Guarda el resultado final en `output/` en los formatos configurados

### Reprocesamiento

Cuando necesitas volver a aplicar `process.py` sobre datos ya scrapeados (por ejemplo, tras corregir la logica de transformacion) sin lanzar el navegador:

```bash
python -m src.main --reprocess 20260312_143052
```

El sufijo identifica la ejecucion y corresponde al timestamp del archivo en `raw/`:

```
raw/
└── viviendas_20260312_143052.csv   ← sufijo: 20260312_143052
```

Para ver los sufijos disponibles, lista la carpeta `raw/`.

## Configuracion

### Raw (`config/settings.py`)

Configura el almacenamiento intermedio y la politica de limpieza:

```python
RAW_CONFIG = {
    "raw_folder": "raw",       # Carpeta de archivos raw
    "filename": "viviendas",   # Nombre base del archivo
    "format": "csv",           # Formato del raw (siempre csv)
    "retention": {
        "mode": "keep_last_n", # "keep_all" | "keep_last_n" | "keep_days"
        "value": 5             # N archivos o N dias a conservar
    }
}
```

| Modo | Comportamiento |
|------|----------------|
| `keep_all` | Conserva todos los archivos raw (sin limpieza) |
| `keep_last_n` | Conserva los ultimos N archivos por fecha de modificacion |
| `keep_days` | Conserva los archivos de los ultimos N dias |

### Procesamiento (`src/process.py`)

Implementa tu logica de transformacion dentro de `process()`. La funcion recibe los parametros del archivo raw y devuelve una lista de diccionarios con los datos procesados:

```python
def process(filename: str, extension: str, suffix: str, raw_config: dict) -> list[dict]:
    filepath = os.path.join(raw_config["raw_folder"], f"{filename}_{suffix}.{extension}")
    df = pd.read_csv(filepath)

    # --- Tu logica aqui ---

    return df.to_dict(orient="records")
```

## API Reference

### scraper.py

```python
def scrape(driver, web_config, logger) -> list[dict]:
    """
    Extrae datos desde la URL usando los selectores del archivo de configuracion.

    Args:
        driver: Instancia del driver de SeleniumBase
        web_config: Diccionario con url, xpath_selectors y waits
        logger: Logger para registrar eventos

    Returns:
        Lista de diccionarios con los datos extraidos
    """
```

### storage.py

```python
def save_data(datos, format, data_config, storage_config) -> None:
    """
    Guarda los datos en el formato y ubicacion especificados.

    Args:
        datos: Lista de diccionarios con los datos a guardar
        format: Formato de salida (csv, json, xml, xlsx)
        data_config: Diccionario con configuraciones de cada formato
        storage_config: Diccionario con configuracion de almacenamiento
    """

def build_filepath(storage_config, format) -> str:
    """
    Construye la ruta del archivo segun el modo de nombrado configurado.

    Args:
        storage_config: Diccionario con configuracion de almacenamiento
        format: Formato de salida (csv, json, xml, xlsx)

    Returns:
        Ruta completa del archivo a guardar
    """
```

### process.py

```python
def process(filename: str, extension: str, suffix: str, raw_config: dict) -> list[dict]:
    """
    Lee el archivo raw y aplica transformaciones a los datos.

    Args:
        filename:   Nombre base del archivo (ej: "viviendas")
        extension:  Extension del archivo   (ej: "csv")
        suffix:     Sufijo timestamp de la ejecucion (ej: "20260312_143052")
        raw_config: Diccionario con configuracion del raw

    Returns:
        Lista de diccionarios con los datos procesados
    """
```

### storage.py

```python
def save_raw(datos: list[dict], raw_config: dict) -> str:
    """
    Guarda los datos en bruto como CSV con sufijo timestamp.

    Returns:
        Sufijo timestamp generado (ej: "20260312_143052")
    """

def cleanup_raw(raw_config: dict) -> None:
    """
    Limpia archivos raw segun la politica de retencion configurada.
    """
```

### main.py

```python
def load_web_config(logger=None, path="config/web_config.yaml") -> dict:
    """
    Carga la configuracion de la web desde el archivo YAML.

    Args:
        logger: Logger opcional para registrar eventos
        path: Ruta al archivo de configuracion

    Returns:
        Diccionario con url, xpath_selectors y waits
    """

def main() -> None:
    """
    Orquesta el flujo completo o el reprocesamiento segun los argumentos CLI.

    Flujo completo:
    1. Configura el logger
    2. Carga la configuracion web desde YAML
    3. Inicializa el driver y ejecuta el scraping
    4. Guarda los datos en bruto (raw/)
    5. Aplica transformaciones con process()
    6. Limpia archivos raw segun politica de retencion
    7. Guarda el resultado final en output/

    Flujo reprocess (--reprocess SUFFIX):
    1. Configura el logger
    2. Aplica transformaciones con process() sobre el raw indicado
    3. Guarda el resultado final en output/
    """
```

## Tests

### WebConfig
| Test | Descripcion |
|------|-------------|
| `test_web_config_file_exists` | Verifica existencia del YAML |
| `test_web_config_has_required_keys` | Valida claves requeridas |
| `test_url_format_is_valid` | Valida formato URL |
| `test_xpath_selectors_format` | Valida formato XPath |
| `test_waits_are_positive_numbers` | Valida waits numericos |

### DataConfig
| Test | Descripcion |
|------|-------------|
| `test_settings_has_data_config` | Verifica DATA_CONFIG existe y tiene al menos un formato |

### StorageConfig
| Test | Descripcion |
|------|-------------|
| `test_settings_has_storage_config` | Verifica STORAGE_CONFIG existe |
| `test_storage_config_has_required_keys` | Valida claves requeridas |
| `test_storage_config_naming_mode_is_valid` | Valida naming_mode |
| `test_storage_config_output_folder_exists` | Verifica carpeta output |

### DriverConfig
| Test | Descripcion |
|------|-------------|
| `test_settings_file_has_driver_config` | Verifica DRIVER_CONFIG |
| `test_driver_instance_created_with_settings_file` | Test de instancia del driver |

### RawConfig
| Test | Descripcion |
|------|-------------|
| `test_settings_has_raw_config` | Verifica que RAW_CONFIG existe |
| `test_raw_config_has_required_keys` | Valida claves requeridas |
| `test_raw_config_format_is_csv` | Verifica que el formato raw es csv |
| `test_raw_config_retention_mode_is_valid` | Valida el modo de retencion |

## Requisitos

- Python 3.8+
- SeleniumBase
- pandas
- pyyaml
- pytest
- openpyxl

## Licencia

Este proyecto es open source y esta disponible bajo la [Licencia MIT](LICENSE).

## Aviso Legal

Esta plantilla esta destinada exclusivamente para fines educativos y de aprendizaje. Antes de realizar scraping en cualquier sitio web, asegurate de:

- Revisar y respetar los terminos de servicio del sitio
- Consultar el archivo `robots.txt`
- No sobrecargar los servidores con peticiones excesivas
- Respetar la privacidad y los datos personales

El uso responsable del web scraping es responsabilidad del usuario.
