# ScrapeCraft

Plantilla open source para construir web scrapers de forma facil y rapida. Basada en [SeleniumBase](https://github.com/seleniumbase/SeleniumBase), un framework de automatizacion con soporte integrado para evasion de deteccion.

## Proposito

ScrapeCraft busca ser un punto de partida para cualquier persona que quiera aprender web scraping o construir sus propios scrapers para **fines educativos y divertidos**. La plantilla esta disenada para ser:

- **Facil de usar**: Configura tu scraper editando archivos YAML y Python, sin tocar el codigo principal
- **Flexible**: Soporta multiples procesos de scraping y multiples formatos de salida (CSV, JSON, XML, Excel)
- **Robusta**: Incluye sistema de logging, manejo de errores y evasion de deteccion

## Estructura

```
ScrapeCraft/
├── src/
│   ├── main.py                        # Dispatcher: lanza el job indicado por CLI
│   ├── shared/                        # Modulos reutilizables entre todos los jobs
│   │   ├── driver_config.py           # Configuracion del driver
│   │   ├── logger.py                  # Sistema de logging
│   │   └── storage.py                 # Almacenamiento y exportacion
│   └── viviendas_adonde/              # Job de ejemplo
│       ├── scraper.py                 # Logica de extraccion de datos
│       ├── process.py                 # Transformacion de datos (raw → procesado)
│       └── app_job.py                 # Flujo ETL del job + load_web_config()
├── config/
│   ├── global_settings.py             # Config global: LOG_CONFIG, DATA_CONFIG
│   └── viviendas_adonde/              # Config especifica del job
│       ├── settings.py                # DRIVER_CONFIG, STORAGE_CONFIG, RAW_CONFIG
│       └── web_config.yaml            # URL, selectores XPath y waits
├── tests/
│   ├── test_global.py                 # Tests de configuracion global
│   └── viviendas_adonde/              # Tests especificos del job
│       └── test_config.py
├── log/                               # Logs de ejecucion (compartido)
├── output/
│   └── viviendas_adonde/              # Archivos de salida del job
├── raw/
│   └── viviendas_adonde/              # Archivos intermedios del job
├── requirements.txt
├── CHANGELOG.md
└── LICENSE
```

## Arquitectura

El proyecto sigue un patron **multi-job dispatcher**:

```
main.py (Dispatcher CLI)
    │
    └── importlib → src.<job>.app_job.run(args)
                        │
                        ├── load_web_config()      # Carga config/<job>/web_config.yaml
                        │
                        ├── shared/driver_config.py
                        │   └── DriverConfig        # Inicializa el browser
                        │
                        ├── scraper.py
                        │   └── scrape()            # Extrae datos de la web
                        │
                        ├── shared/storage.py
                        │   ├── save_raw()          # Guarda CSV en raw/<job>/
                        │   ├── cleanup_raw()       # Aplica politica de retencion
                        │   └── save_data()         # Exporta a output/<job>/
                        │
                        └── process.py
                            └── process()           # Transforma raw → procesado
```

### Modulos compartidos (`src/shared/`)

| Modulo | Responsabilidad |
|--------|-----------------|
| `storage.py` | Persistencia: raw, cleanup, construir rutas, exportar en multiples formatos |
| `driver_config.py` | Inicializacion del navegador con opciones anti-deteccion |
| `logger.py` | Sistema de logging dual (archivo + consola) |

### Modulos por job (`src/<job>/`)

| Modulo | Responsabilidad |
|--------|-----------------|
| `app_job.py` | Flujo ETL completo del job, expone `run(args)` como interfaz estandar |
| `scraper.py` | Logica de extraccion: navegar, manejar CAPTCHA, extraer elementos |
| `process.py` | Transformacion de datos entre el raw y el guardado final |

## Instalacion

```bash
git clone https://github.com/tu-usuario/ScrapeCraft.git
cd ScrapeCraft
pip install -r requirements.txt
```

## Uso

```bash
# Ejecutar un job completo (scraping + procesamiento + guardado)
python -m src.main --job viviendas_adonde

# Reprocesar sin volver a scrapear (usa un raw existente)
python -m src.main --job viviendas_adonde --reprocess 20260312_143052

# Ejecutar todos los tests
pytest tests/ -v

# Ejecutar solo tests globales
pytest tests/test_global.py -v

# Ejecutar tests de un job especifico
pytest tests/viviendas_adonde/ -v
```

### Flujo completo

```
scrape() → save_raw() → del datos → process() → cleanup_raw() → save_data()
```

1. Extrae datos de la web y los guarda en `raw/<job>/` como CSV con sufijo timestamp
2. Libera la memoria del raw y aplica las transformaciones definidas en `process.py`
3. Limpia archivos antiguos de `raw/<job>/` segun la politica de retencion configurada
4. Guarda el resultado final en `output/<job>/` en los formatos configurados

### Reprocesamiento

Cuando necesitas volver a aplicar `process.py` sobre datos ya scrapeados (por ejemplo, tras corregir la logica de transformacion) sin lanzar el navegador:

```bash
python -m src.main --job viviendas_adonde --reprocess 20260312_143052
```

El sufijo identifica la ejecucion y corresponde al timestamp del archivo en `raw/<job>/`:

```
raw/viviendas_adonde/
└── viviendas_20260312_143052.csv   ← sufijo: 20260312_143052
```

## Configuracion

### Global (`config/global_settings.py`)

Aplica a todos los jobs. Contiene `LOG_CONFIG` y `DATA_CONFIG`.

```python
LOG_CONFIG = {
    "log_folder": "log",    # Carpeta de logs (compartida entre todos los jobs)
    "level": "INFO"         # Nivel: DEBUG, INFO, WARNING, ERROR
}

DATA_CONFIG = {
    "csv":  {"encoding": "utf-8", "separator": ";", "index": False},
    "json": {"indent": 2, "force_ascii": False, "orient": "records"},
    "xml":  {"root": "registros", "row": "registro"},
    "xlsx": {"sheet_name": "Datos", "index": False}
}
```

### Por job (`config/<job>/settings.py`)

Especifica del job. Contiene `DRIVER_CONFIG`, `STORAGE_CONFIG` y `RAW_CONFIG`.

```python
DRIVER_CONFIG = {
    "headless": False,      # Ejecutar sin interfaz grafica
    "undetected": True,     # Modo anti-deteccion
    "maximize": True,       # Maximizar ventana
    "window_size": None,    # Tamano especifico: (1920, 1080)
    "user_agent": None,     # User agent personalizado
    "proxy": None           # Proxy: "ip:puerto"
}

STORAGE_CONFIG = {
    "output_folder": "output/viviendas_adonde",
    "filename": "viviendas",
    "naming_mode": "date_suffix",    # overwrite | date_suffix | timestamp_suffix | date_folder
    "output_formats": ["csv", "json"]
}

RAW_CONFIG = {
    "raw_folder": "raw/viviendas_adonde",
    "filename": "viviendas",
    "format": "csv",
    "retention": {
        "mode": "keep_last_n",  # keep_all | keep_last_n | keep_days
        "value": 5
    }
}
```

#### Modos de nombrado (`naming_mode`)

| Modo | Resultado | Uso |
|------|-----------|-----|
| `overwrite` | `output/<job>/viviendas.csv` | Sobrescribe siempre |
| `date_suffix` | `output/<job>/viviendas_20260130.csv` | Una ejecucion por dia |
| `timestamp_suffix` | `output/<job>/viviendas_20260130_143052.csv` | Multiples ejecuciones por dia |
| `date_folder` | `output/<job>/20260130/viviendas.csv` | Organizar por carpetas |

#### Politicas de retencion de raw

| Modo | Comportamiento |
|------|----------------|
| `keep_all` | Conserva todos los archivos raw |
| `keep_last_n` | Conserva los ultimos N archivos por fecha de modificacion |
| `keep_days` | Conserva los archivos de los ultimos N dias |

### Web (`config/<job>/web_config.yaml`)

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

## Agregar un nuevo proceso

1. Crear `src/<nombre>/app_job.py` con `def run(args)` que implementa el flujo ETL
2. Crear `src/<nombre>/scraper.py` con la logica de extraccion
3. Crear `src/<nombre>/process.py` con la logica de transformacion
4. Crear `config/<nombre>/settings.py` con `DRIVER_CONFIG`, `STORAGE_CONFIG` y `RAW_CONFIG`
5. Crear `config/<nombre>/web_config.yaml` con la URL y los selectores
6. Crear las carpetas `output/<nombre>/` y `raw/<nombre>/`

Luego ejecutar:

```bash
python -m src.main --job <nombre>
```

No es necesario modificar `main.py`.

## Procesamiento (`src/<job>/process.py`)

Implementa tu logica de transformacion dentro de `process()`:

```python
def process(filename: str, extension: str, suffix: str, raw_config: dict) -> list[dict]:
    filepath = os.path.join(raw_config["raw_folder"], f"{filename}_{suffix}.{extension}")
    df = pd.read_csv(filepath)

    # --- Tu logica aqui ---

    return df.to_dict(orient="records")
```

## API Reference

### `src/shared/storage.py`

```python
def save_data(datos, format, data_config, storage_config) -> None:
    """Guarda los datos en el formato y ubicacion especificados."""

def save_raw(datos, raw_config) -> str:
    """Guarda datos en bruto como CSV. Retorna el sufijo timestamp generado."""

def cleanup_raw(raw_config) -> None:
    """Limpia archivos raw segun la politica de retencion configurada."""

def build_filepath(storage_config, format) -> str:
    """Construye la ruta del archivo segun el modo de nombrado configurado."""
```

### `src/<job>/scraper.py`

```python
def scrape(driver, web_config, logger) -> list[dict]:
    """Extrae datos desde la URL usando los selectores del archivo de configuracion."""
```

### `src/<job>/process.py`

```python
def process(filename, extension, suffix, raw_config) -> list[dict]:
    """Lee el archivo raw y aplica transformaciones a los datos."""
```

### `src/<job>/app_job.py`

```python
def load_web_config(logger=None) -> dict:
    """Carga la configuracion de la web desde el archivo YAML del job."""

def run(args: argparse.Namespace) -> None:
    """
    Punto de entrada del job. Interfaz estandar requerida por el dispatcher.

    Flujo completo:    scrape → save_raw → process → cleanup_raw → save_data
    Flujo reprocess:   process → save_data
    """
```

## Tests

### `tests/test_global.py`

| Clase | Test | Descripcion |
|-------|------|-------------|
| `TestLogConfig` | `test_global_settings_has_log_config` | Verifica que LOG_CONFIG existe |
| `TestLogConfig` | `test_log_config_has_required_keys` | Valida claves requeridas |
| `TestLogConfig` | `test_log_config_level_is_valid` | Valida nivel de logging |
| `TestDataConfig` | `test_global_settings_has_data_config` | Verifica DATA_CONFIG con al menos un formato |
| `TestDataConfig` | `test_data_config_formats_have_required_keys` | Valida que cada formato tiene configuracion |

### `tests/viviendas_adonde/test_config.py`

| Clase | Test | Descripcion |
|-------|------|-------------|
| `TestWebConfig` | `test_web_config_file_exists` | Verifica existencia del YAML |
| `TestWebConfig` | `test_web_config_has_required_keys` | Valida claves requeridas |
| `TestWebConfig` | `test_url_format_is_valid` | Valida formato URL |
| `TestWebConfig` | `test_xpath_selectors_format` | Valida formato XPath |
| `TestWebConfig` | `test_waits_are_positive_numbers` | Valida waits numericos |
| `TestStorageConfig` | `test_settings_has_storage_config` | Verifica STORAGE_CONFIG existe |
| `TestStorageConfig` | `test_storage_config_has_required_keys` | Valida claves requeridas |
| `TestStorageConfig` | `test_storage_config_naming_mode_is_valid` | Valida naming_mode |
| `TestStorageConfig` | `test_storage_config_output_folder_exists` | Verifica carpeta output |
| `TestDriverConfig` | `test_settings_file_has_driver_config` | Verifica DRIVER_CONFIG existe |
| `TestDriverConfig` | `test_driver_instance_created_with_settings_file` | Test de instancia del driver |
| `TestRawConfig` | `test_settings_has_raw_config` | Verifica RAW_CONFIG existe |
| `TestRawConfig` | `test_raw_config_has_required_keys` | Valida claves requeridas |
| `TestRawConfig` | `test_raw_config_format_is_csv` | Verifica formato raw es csv |
| `TestRawConfig` | `test_raw_config_retention_mode_is_valid` | Valida modo de retencion |

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
