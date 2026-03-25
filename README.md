# ScrapeCraft

Plantilla open source para construir web scrapers de forma facil y rapida. Basada en [SeleniumBase](https://github.com/seleniumbase/SeleniumBase), un framework de automatizacion con soporte integrado para evasion de deteccion.

## Proposito

ScrapeCraft busca ser un punto de partida para cualquier persona que quiera aprender web scraping o construir sus propios scrapers para **fines educativos y divertidos**. La plantilla esta disenada para ser:

- **Facil de usar**: Configura tu scraper editando archivos YAML y Python, sin tocar el codigo principal
- **Flexible**: Soporta multiples procesos de scraping y multiples formatos de salida (CSV, JSON, XML, Excel)
- **Robusta**: Incluye sistema de logging, manejo de errores y evasion de deteccion

> **Nuevo proyecto?** Usa el [ScrapeCraft Generator](../scrapecraft-generator/) para generar la estructura completa de tu proyecto de forma interactiva, sin copiar ni modificar esta plantilla manualmente.

## Estructura

```
ScrapeCraft/
├── src/
│   ├── main.py                        # Dispatcher: lanza el job indicado por CLI
│   ├── shared/                        # Modulos reutilizables entre todos los jobs
│   │   ├── driver_config.py           # Inicializacion del driver (create_driver)
│   │   ├── job_runner.py              # Orquestacion ETL generica
│   │   ├── logger.py                  # Sistema de logging
│   │   ├── storage.py                 # Almacenamiento y exportacion
│   │   └── utils.py                   # Funciones auxiliares de extraccion
│   ├── consolidadores/                # Modulos de consolidacion (uno por pipeline)
│   │   └── ejemplo.py                 # Consolidador de ejemplo
│   ├── viviendas_adonde/              # Job: portal de alquiler de inmuebles
│   │   ├── settings.py                # Config del job: DRIVER, STORAGE, RAW, SKIP_PROCESS
│   │   ├── web_config.yaml            # URL, selectores y waits
│   │   ├── scraper.py
│   │   ├── process.py
│   │   └── utils.py
│   └── books_to_scrape/               # Job: catalogo de libros (sitio de practica)
│       ├── settings.py
│       ├── web_config.yaml
│       ├── scraper.py
│       ├── process.py
│       └── utils.py
├── config/
│   ├── global_settings.py             # Config global: LOG_CONFIG, DATA_CONFIG
│   └── pipelines/
│       ├── diario.yaml                # Ejemplo de pipeline multi-job
│       └── diario_consolidado.yaml    # Ejemplo de pipeline con consolidacion
├── tests/
│   ├── test_global.py                 # Tests de configuracion global
│   ├── test_pipelines.py              # Tests de todos los pipelines (auto-discovery)
│   ├── viviendas_adonde/
│   │   └── test_viviendas_adonde.py
│   └── books_to_scrape/
│       └── test_books_to_scrape.py
├── log/                               # Logs de ejecucion (compartido)
├── output/
│   ├── consolidados/                  # Output de consolidaciones
│   ├── viviendas_adonde/
│   └── books_to_scrape/
├── raw/
│   ├── viviendas_adonde/
│   └── books_to_scrape/
├── requirements.txt
├── CHANGELOG.md
└── LICENSE
```

## Arquitectura

El proyecto sigue un patron **multi-job dispatcher**:

```
main.py (Dispatcher CLI)
    │
    └── importlib → src.<job>.{scraper, process, settings}
                        │
                        └── shared/job_runner.run()     # Orquestacion ETL generica
                                │
                                ├── load_web_config()   # Carga src/<job>/web_config.yaml
                                │
                                ├── shared/driver_config.py
                                │   └── DriverConfig    # Inicializa el browser
                                │
                                ├── scraper.py
                                │   └── scrape()        # Extrae datos de la web
                                │
                                ├── shared/storage.py
                                │   ├── save_raw()      # Guarda raw en raw/<job>/
                                │   ├── cleanup_raw()   # Aplica politica de retencion
                                │   └── save_data()     # Exporta a output/<job>/
                                │
                                └── process.py
                                    └── process()       # Transforma raw → procesado
```

### Modulos compartidos (`src/shared/`)

| Modulo | Responsabilidad |
|--------|-----------------|
| `job_runner.py` | Orquestacion ETL generica: `_run_full`, `_run_reprocess`, `_save_output`, `run` |
| `storage.py` | Persistencia: raw, cleanup, construir rutas, exportar en multiples formatos, cargar outputs para consolidacion |
| `driver_config.py` | `create_driver(config)`: inicializa el navegador con opciones anti-deteccion |
| `logger.py` | Sistema de logging dual (archivo + consola) |
| `utils.py` | Funciones auxiliares de extraccion reutilizables: `safe_get_text`, `safe_get_attr` |

### Modulos consolidadores (`src/consolidadores/`)

| Modulo | Responsabilidad |
|--------|-----------------|
| `ejemplo.py` | Consolidador de ejemplo: combina todos los jobs por concatenacion con columna `_fuente` |

Cada consolidador define su propio `STORAGE_CONFIG` y una funcion `consolidate(job_dataframes, params)`. El framework gestiona el I/O — el consolidador solo implementa logica.

### Modulos por job (`src/<job>/`)

| Modulo | Responsabilidad |
|--------|-----------------|
| `scraper.py` | Logica de extraccion: navegar, manejar CAPTCHA, extraer elementos |
| `process.py` | Transformacion de datos entre el raw y el guardado final |
| `utils.py` | `parse_record()` con logica especifica del job; importa `safe_get_text`/`safe_get_attr` de shared |

## Requisitos previos

- Python **3.10 o superior** (el codigo usa union types `X | Y` disponibles desde 3.10)
- Google Chrome instalado (SeleniumBase gestiona el chromedriver automaticamente)

## Instalacion

**1. Clonar o descargar el repositorio**

```bash
git clone <url-del-repositorio>
cd Plantilla-Scraping-SeleniumBase
```

**2. Crear y activar el entorno virtual**

```bash
# Crear
python -m venv venv

# Activar en Windows
venv\Scripts\activate

# Activar en macOS / Linux
source venv/bin/activate
```

**3. Instalar dependencias**

```bash
pip install -r requirements.txt
```

> Todos los comandos del proyecto deben ejecutarse desde la **raiz del repositorio** con el entorno virtual activo.

## Uso

```bash
# Ver los jobs disponibles
python -m src.main --list

# --- Job individual ---
python -m src.main --job books_to_scrape
python -m src.main --job viviendas_adonde

# --- Reprocesar raw existente sin volver a scrapear ---
python -m src.main --job books_to_scrape --reprocess 20260313_142546

# --- Ejecucion en serie (pipeline) ---
python -m src.main --pipeline config/pipelines/diario.yaml

# --- Ejecucion en serie con consolidacion ---
python -m src.main --pipeline config/pipelines/diario_consolidado.yaml
```

## Tests

Los tests estan divididos en dos grupos segun si requieren o no un navegador:

**Tests de configuracion** — rapidos, sin browser:

```bash
# Todos los tests de configuracion y pipeline (recomendado para validacion rapida)
pytest tests/test_global.py tests/test_pipelines.py -v

# Solo configuracion global
pytest tests/test_global.py -v

# Solo pipelines
pytest tests/test_pipelines.py -v
```

**Tests de job** — incluyen un test que abre el browser en modo headless:

```bash
# Job books_to_scrape
pytest tests/books_to_scrape/ -v -s

# Job viviendas_adonde
pytest tests/viviendas_adonde/ -v -s

# Todos los tests (configuracion + todos los jobs)
pytest tests/ -v -s
```

> El test `test_driver_instance_created_with_settings_file` abre Chrome en modo headless para verificar que el driver se inicializa correctamente. Requiere Chrome instalado.

## Ejecucion en serie

ScrapeCraft tiene dos modos de ejecucion mutuamente excluyentes:

| Modo | Comando | Uso |
|------|---------|-----|
| Job individual | `--job nombre` | Un job, con `--reprocess` opcional |
| Pipeline YAML | `--pipeline ruta.yaml` | Uno o mas jobs con params, `enabled` y consolidacion opcional |

Para correr multiples jobs o pasar params, usa siempre `--pipeline`. El reprocesamiento (`--reprocess`) es una operacion manual exclusiva de `--job`.

### Pipeline YAML

Permite definir pipelines nombrados y reutilizables con params independientes por job:

```yaml
# config/pipelines/diario.yaml
name: diario
description: "Scraping diario de catalogo y viviendas"   # opcional

jobs:
  - name: books_to_scrape
    params:               # opcional, dict nativo YAML
      categoria: mystery
      pagina: 1           # llega como int, no como str

  - name: viviendas_adonde
    params:
      pais: peru
      max_paginas: 5
      solo_nuevos: true   # llega como bool

  # Desactivar un job sin borrarlo:
  # - name: otro_job
  #   enabled: false
```

```bash
python -m src.main --pipeline config/pipelines/diario.yaml
```

Los params se definen como dict YAML nativo — los tipos (`int`, `bool`, `float`, `str`) se preservan directamente en el scraper sin conversion manual.

### Consolidacion

Un pipeline puede incluir un paso de consolidacion opcional que combina los outputs de todos los jobs en un unico dataset. Solo se ejecuta si **todos** los jobs del pipeline finalizaron exitosamente.

```yaml
# config/pipelines/diario_consolidado.yaml
name: diario_consolidado

jobs:
  - name: books_to_scrape
  - name: viviendas_adonde

consolidate:
  enabled: true
  module: ejemplo       # src/consolidadores/ejemplo.py
  format: csv           # todos los jobs deben incluir este formato en output_formats
  params: {}            # opcional, recibido en consolidate() como dict
```

```bash
python -m src.main --pipeline config/pipelines/diario_consolidado.yaml
```

El bloque `consolidate` requiere:
- `enabled` (bool): activa o desactiva la consolidacion
- `module` (str): nombre del modulo en `src/consolidadores/` (sin `.py`)
- `format` (str): formato compartido por todos los jobs (`csv`, `json`, `xml`, `xlsx`); todos deben incluirlo en su `output_formats`
- `params` (dict, opcional): parametros adicionales para la logica del consolidador

El framework valida estos requisitos **antes de lanzar cualquier job** — fallo rapido si algun job no cumple el formato requerido.

### Crear un consolidador

1. Crea `src/consolidadores/<nombre>.py` copiando `ejemplo.py`
2. Ajusta `STORAGE_CONFIG` (carpeta, nombre, naming_mode, formatos de salida)
3. Implementa `consolidate()` — el framework entrega los DataFrames listos, sin I/O

```python
# src/consolidadores/<nombre>.py
import pandas as pd

STORAGE_CONFIG = {
    "output_folder": "output/consolidados",
    "filename": "mi_consolidado",
    "naming_mode": "date_suffix",
    "output_formats": ["csv"],
}

def consolidate(job_dataframes: dict[str, pd.DataFrame], params: dict = None) -> list[dict]:
    df_a = job_dataframes["job_a"]
    df_b = job_dataframes["job_b"]
    # ... logica de combinacion
    return resultado.to_dict(orient="records")
```

El framework se encarga de leer los archivos de cada job con la configuracion correcta de `DATA_CONFIG` y entrega los DataFrames listos. El data engineer solo escribe logica.

### Comportamiento ante fallos en serie

Si un job falla, el error se registra y la ejecucion continua con el siguiente. Al finalizar se muestra un resumen:

```
==================================================
Serie finalizada: 2/2 jobs exitosos
```

o en caso de error parcial:

```
==================================================
Serie finalizada: 1/2 jobs exitosos
Jobs con error: viviendas_adonde
```

### Flujo completo (`skip_process=False`)

```
scrape() → save_raw() → normalize_in_memory() → process() → save_data() → cleanup_raw()
```

1. Extrae datos de la web y los guarda en `raw/<job>/` como CSV con sufijo timestamp
2. Normaliza el raw en memoria (`fillna("").astype(str)`) y aplica las transformaciones definidas en `process.py`
3. Guarda el resultado final en `output/<job>/` en los formatos configurados
4. Limpia archivos antiguos de `raw/<job>/` segun la politica de retencion configurada — siempre, tanto si el job finaliza exitosamente como si falla durante `process()`

### Flujo sin procesamiento (`skip_process=True`)

```
scrape() → save_raw() → normalize_in_memory() → save_data() → cleanup_raw()
```

Util cuando la web ya devuelve datos normalizados y no se requiere transformacion. Se activa con `SKIP_PROCESS = True` en `settings.py`.

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
```

Cada ejecucion genera su propio archivo de log: `log/<job>_YYYYMMDD_HHMMSS.log`. El timestamp completo garantiza que multiples ejecuciones del mismo dia no mezclen sus logs.

```python
DATA_CONFIG = {
    "csv":  {"encoding": "utf-8", "separator": ";", "index": False},
    "json": {"indent": 2, "force_ascii": False, "orient": "records"},
    "xml":  {"root": "registros", "row": "registro", "encoding": "utf-8"},
    "xlsx": {"sheet_name": "Datos", "index": False}
}
```

`DATA_CONFIG` es la unica fuente de verdad para los parametros de cada formato. Se aplica tanto al output final (`save_data`) como al raw intermedio (`save_raw`, `load_raw`, `process.py`).

### Por job (`src/<job>/settings.py`)

Especifica del job. Contiene `DRIVER_CONFIG`, `STORAGE_CONFIG`, `RAW_CONFIG` y `SKIP_PROCESS`.

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
    "format": "csv",             # csv | json | xml | xlsx
    "retention": {
        "mode": "keep_last_n",  # keep_all | keep_last_n | keep_days
        "value": 5
    }
}

SKIP_PROCESS = False   # True: omite process.py y guarda el raw directamente
```

#### Modos de nombrado (`naming_mode`)

| Modo | Resultado | Uso |
|------|-----------|-----|
| `overwrite` | `output/<job>/viviendas.csv` | Sobrescribe siempre |
| `date_suffix` | `output/<job>/viviendas_20260130.csv` | Una ejecucion por dia |
| `timestamp_suffix` | `output/<job>/viviendas_20260130_143052.csv` | Multiples ejecuciones por dia |
| `date_folder` | `output/<job>/20260130/viviendas.csv` | Organizar por carpetas |

#### Formato de raw (`format`)

El campo `format` determina en que formato se persiste el raw intermedio. El pipeline usa automaticamente la configuracion de `DATA_CONFIG[format]` para leer y escribir.

| Formato | Config aplicada | Archivo generado |
|---------|-----------------|------------------|
| `csv`  | `DATA_CONFIG["csv"]`  | `viviendas_20260312_143052.csv`  |
| `json` | `DATA_CONFIG["json"]` | `viviendas_20260312_143052.json` |
| `xml`  | `DATA_CONFIG["xml"]`  | `viviendas_20260312_143052.xml`  |
| `xlsx` | `DATA_CONFIG["xlsx"]` | `viviendas_20260312_143052.xlsx` |

#### Politicas de retencion de raw

| Modo | Comportamiento |
|------|----------------|
| `keep_all` | Conserva todos los archivos raw |
| `keep_last_n` | Conserva los ultimos N archivos, ordenados por timestamp en el nombre |
| `keep_days` | Conserva los archivos cuyo timestamp en el nombre no supere N dias de antiguedad |

### Web (`src/<job>/web_config.yaml`)

```yaml
url: "https://ejemplo.com"

# Selectores — indica el tipo usado (XPath o CSS) en un comentario.
selectors:
  container: '//div[@class="item"]'
  Campo1: './/span[@class="dato1"]'
  Campo2: './/span[@class="dato2"]'

waits:
  reconnect_attempts: 3
  after_load: 5
```

## Zonas del data engineer

Cada archivo marca con `# ZONA DATA ENGINEER` las secciones que debes modificar. El resto es codigo de framework y no requiere cambios.

| Archivo | Zona | Que implementar |
|---------|------|-----------------|
| `src/<job>/web_config.yaml` | Completo | `url`, `selectors`, `waits` |
| `src/<job>/settings.py` | Completo | `DRIVER_CONFIG`, `STORAGE_CONFIG`, `RAW_CONFIG`, `SKIP_PROCESS` |
| `src/<job>/scraper.py` | Cuerpo de `scrape()` | Navegacion, manejo de CAPTCHA, extraccion de elementos |
| `src/<job>/utils.py` | Cuerpo de `parse_record()` | Extraccion campo a campo (texto, atributo, logica especial) |
| `src/<job>/process.py` | Cuerpo de `process()` + constantes de apoyo | Transformaciones, castings de tipo, columnas derivadas |
| `src/consolidadores/<nombre>.py` | `STORAGE_CONFIG` + cuerpo de `consolidate()` | Desempaquetar DataFrames y logica de combinacion |
| `config/pipelines/<nombre>.yaml` | Completo | Jobs, params, bloque `consolidate` |
| `config/global_settings.py` | Completo (casos excepcionales) | Encoding, separadores, estructura XML, nivel de log |

Lo que **no** toca el data engineer:
- `src/main.py`
- `src/shared/` (job_runner, storage, driver_config, logger, utils)

## Agregar un nuevo proceso

1. Crear `src/<nombre>/scraper.py` con la logica de extraccion
2. Crear `src/<nombre>/utils.py` con `parse_record()` (importa `safe_get_text`/`safe_get_attr` desde `src.shared.utils`)
3. Crear `src/<nombre>/process.py` con la logica de transformacion
4. Crear `src/<nombre>/settings.py` con `DRIVER_CONFIG`, `STORAGE_CONFIG`, `RAW_CONFIG` y `SKIP_PROCESS`
5. Crear `src/<nombre>/web_config.yaml` con la URL y los selectores

Las carpetas `output/<nombre>/` y `raw/<nombre>/` se crean automaticamente en la primera ejecucion. No es necesario modificar `main.py` ni ningun otro modulo del framework — el dispatcher descubre el job automaticamente por la presencia de `scraper.py`.

Luego ejecutar:

```bash
python -m src.main --job <nombre>
```

No es necesario modificar `main.py`.

## Procesamiento (`src/<job>/process.py`)

Implementa tu logica de transformacion dentro de `process()`. Recibe un DataFrame con todas las columnas como `str` — convierte los tipos que necesites explicitamente:

```python
def process(df: pd.DataFrame) -> list[dict]:
    # todas las columnas llegan como str (lineamiento string-first)

    # --- Tu logica aqui ---
    # Convierte tipos donde sea necesario, por ejemplo:
    # df["precio"] = df["precio"].str.replace(r"[^\d]", "", regex=True).astype(int)

    return df.to_dict(orient="records")
```

`job_runner.py` se encarga de normalizar el raw y construir el DataFrame antes de llamar a `process()`. El modulo no tiene dependencias de I/O — solo recibe datos y devuelve datos.

### Lineamiento string-first

El raw intermedio se persiste siempre como `str`. El output final preserva los tipos que `process.py` asigne:

- **Al escribir raw** (`save_raw`): se aplica `df.fillna("").astype(str)` — los `NaN` reales se rellenan con `""` antes de convertir a string, preservando el literal `"nan"` como dato valido en campos de texto
- **Normalizacion en memoria**: tras `save_raw`, el raw se normaliza en memoria con `pd.DataFrame(datos).fillna("").astype(str)` — todas las columnas llegan a `process()` como `str` sin un ciclo de lectura a disco adicional; `load_raw` queda exclusivo para el flujo `--reprocess`, donde retorna directamente un `pd.DataFrame` listo para pasar a `process()`
- **Al escribir output** (`save_data`): se preservan los tipos que `process.py` asigno (`float`, `int`, `datetime`, etc.) — en JSON los numeros se guardan como numeros, en XLSX las celdas mantienen su tipo

Esto garantiza que valores como `"001"`, `"N/A"`, `"1.500,00"` o registros danados se preserven exactamente como llegan del scraper. La conversion de tipos es responsabilidad exclusiva de `process.py`.

## API Reference

### `src/shared/job_runner.py`

```python
def load_web_config(job_name: str) -> dict:
    """Carga y valida la configuracion de la web desde src/<job_name>/web_config.yaml.
    Lanza ValueError si faltan las claves requeridas (url, selectors, waits)."""

def run(args, scrape_fn, process_fn, settings, job_name: str, params: dict | None = None) -> dict[str, Path]:
    """
    Punto de entrada generico para cualquier job. Llamado directamente desde main.py.
    params: dict nativo con los parametros definidos en el pipeline YAML (vacio si no se definio ninguno).
    Retorna mapa de formato -> ruta del archivo guardado (ej: {"csv": Path(...), "json": Path(...)}).

    Flujo completo:    scrape → save_raw → normalize_in_memory → process(df) → cleanup_raw → save_data
    Sin proceso:       scrape → save_raw → normalize_in_memory → cleanup_raw → save_data
    Flujo reprocess:   load_raw → process(df) → save_data
    """
```

### `src/shared/storage.py`

```python
def save_data(datos, format, data_config, storage_config, now=None) -> Path:
    """Guarda los datos en el formato y ubicacion especificados preservando los tipos de cada campo.
    now: datetime opcional; si se omite se usa datetime.now(). Pasar el mismo valor que a save_raw()
    garantiza timestamps coherentes entre el raw y el output de una misma ejecucion.
    Retorna la ruta del archivo guardado."""

def save_raw(datos: pd.DataFrame, raw_config, data_config, now=None) -> str:
    """Guarda datos en bruto en el formato de raw_config["format"]. Retorna el sufijo timestamp.
    datos: DataFrame ya construido (string-first). El caller es responsable de construirlo.
    now: datetime opcional; si se omite se usa datetime.now(). Pasar el mismo valor que a save_data()
    garantiza coherencia de timestamps entre raw y output."""

def load_output(filepath: Path, format: str, data_config: dict) -> pd.DataFrame:
    """Lee un archivo de output y lo retorna como DataFrame usando la config correcta de DATA_CONFIG.
    Usada por el runner para preparar los DataFrames antes de pasarlos al consolidador."""

def load_raw(suffix, raw_config, data_config) -> pd.DataFrame:
    """Lee un raw existente y lo retorna como DataFrame sin transformar. Lee todo como str."""

def cleanup_raw(raw_config) -> None:
    """Limpia archivos raw segun la politica de retencion configurada."""

def build_filepath(storage_config, format, now=None) -> Path:
    """Construye la ruta del archivo segun el modo de nombrado configurado.
    now: datetime opcional; si se omite se usa datetime.now()."""
```

### `src/shared/utils.py`

```python
def safe_get_text(element, xpath, fallback="") -> str:
    """Extrae el texto de un sub-elemento. Retorna fallback si no existe."""

def safe_get_attr(element, xpath, attr, fallback="") -> str:
    """Extrae el valor de un atributo HTML de un sub-elemento. Retorna fallback si no existe.
    Util cuando el dato esta en un atributo (ej: @title, @class, @href) en lugar del texto."""
```

### `src/<job>/scraper.py`

```python
def scrape(driver, web_config, params: dict) -> list[dict]:
    """
    Extrae datos desde la URL usando los selectores del archivo de configuracion.
    params: dict nativo con los parametros definidos en el pipeline YAML.
    Los tipos se preservan directamente (int, bool, float, str) — no se requiere conversion manual.
    """
```

### `src/<job>/process.py`

```python
def process(df: pd.DataFrame) -> list[dict]:
    """Recibe un DataFrame con columnas en str y aplica transformaciones y castings de tipo."""
```

### `src/<job>/utils.py`

```python
def parse_record(item, selectors, index) -> dict:
    """Construye el diccionario de un registro a partir de un elemento contenedor.
    Implementa la logica especifica del job para cada campo (texto, atributo, etc.).
    Importa safe_get_text y safe_get_attr desde src.shared.utils."""
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

### `tests/test_pipelines.py`

Valida automaticamente todos los `.yaml` presentes en `config/pipelines/` — no requiere actualizacion al agregar nuevos pipelines.

| Clase | Test | Descripcion |
|-------|------|-------------|
| `TestPipelineYAML` | `test_at_least_one_pipeline_exists` | Existe al menos un pipeline en `config/pipelines/` |
| `TestPipelineYAML` | `test_pipelines_have_jobs_list` | `jobs` existe, es lista y no esta vacia |
| `TestPipelineYAML` | `test_pipeline_jobs_have_name` | Cada job tiene `name` como string no vacio |
| `TestPipelineYAML` | `test_pipeline_job_names_exist_in_src` | Los nombres de job corresponden a jobs reales en `src/` |
| `TestPipelineYAML` | `test_pipeline_params_are_dicts_if_present` | `params` es dict nativo YAML, no string |
| `TestPipelineYAML` | `test_pipeline_enabled_is_bool_if_present` | `enabled` es `true` o `false` |
| `TestPipelineYAML` | `test_pipeline_metadata_types_if_present` | `name` y `description` del pipeline son strings |
| `TestPipelineYAML` | `test_consolidate_structure_if_present` | Valida estructura del bloque `consolidate` cuando esta presente |
| `TestPipelineYAML` | `test_consolidate_module_exists_if_enabled` | El modulo consolidador existe en `src/consolidadores/` cuando `enabled: true` |
| `TestPipelineYAML` | `test_consolidate_format_in_all_jobs_if_enabled` | Todos los jobs activos incluyen el `format` de consolidacion en su `output_formats` |

### `tests/viviendas_adonde/test_viviendas_adonde.py`

| Clase | Test | Descripcion |
|-------|------|-------------|
| `TestWebConfig` | `test_web_config_file_exists` | Verifica existencia del YAML |
| `TestWebConfig` | `test_web_config_has_required_keys` | Valida claves requeridas |
| `TestWebConfig` | `test_url_format_is_valid` | Valida formato URL |
| `TestWebConfig` | `test_selectors_format` | Valida que cada selector es una cadena no vacia (XPath o CSS) |
| `TestWebConfig` | `test_waits_are_positive_numbers` | Valida waits numericos |
| `TestStorageConfig` | `test_settings_has_storage_config` | Verifica STORAGE_CONFIG existe |
| `TestStorageConfig` | `test_storage_config_has_required_keys` | Valida claves requeridas |
| `TestStorageConfig` | `test_storage_config_naming_mode_is_valid` | Valida naming_mode |
| `TestStorageConfig` | `test_storage_config_output_folder_is_valid_path` | Verifica que output_folder es una cadena no vacia |
| `TestDriverConfig` | `test_settings_file_has_driver_config` | Verifica DRIVER_CONFIG existe |
| `TestDriverConfig` | `test_driver_instance_created_with_settings_file` | Test de instancia del driver |
| `TestRawConfig` | `test_settings_has_raw_config` | Verifica RAW_CONFIG existe |
| `TestRawConfig` | `test_raw_config_has_required_keys` | Valida claves requeridas |
| `TestRawConfig` | `test_raw_config_format_is_valid` | Verifica que el formato raw es uno de los soportados |
| `TestRawConfig` | `test_raw_config_retention_mode_is_valid` | Valida modo de retencion |

### `tests/books_to_scrape/test_books_to_scrape.py`

| Clase | Test | Descripcion |
|-------|------|-------------|
| `TestWebConfig` | `test_web_config_file_exists` | Verifica existencia del YAML |
| `TestWebConfig` | `test_web_config_has_required_keys` | Valida claves requeridas |
| `TestWebConfig` | `test_url_format_is_valid` | Valida formato URL |
| `TestWebConfig` | `test_selectors_format` | Valida que cada selector es una cadena no vacia (XPath o CSS) |
| `TestWebConfig` | `test_selectors_has_expected_fields` | Verifica campos Titulo, Precio y Rating |
| `TestWebConfig` | `test_waits_are_positive_numbers` | Valida waits numericos |
| `TestStorageConfig` | `test_settings_has_storage_config` | Verifica STORAGE_CONFIG existe |
| `TestStorageConfig` | `test_storage_config_has_required_keys` | Valida claves requeridas |
| `TestStorageConfig` | `test_storage_config_naming_mode_is_valid` | Valida naming_mode |
| `TestStorageConfig` | `test_storage_config_output_folder_is_valid_path` | Verifica que output_folder es una cadena no vacia |
| `TestStorageConfig` | `test_storage_config_output_formats_are_valid` | Valida formatos de salida |
| `TestDriverConfig` | `test_settings_file_has_driver_config` | Verifica DRIVER_CONFIG existe |
| `TestDriverConfig` | `test_driver_instance_created_with_settings_file` | Test de instancia del driver |
| `TestRawConfig` | `test_settings_has_raw_config` | Verifica RAW_CONFIG existe |
| `TestRawConfig` | `test_raw_config_has_required_keys` | Valida claves requeridas |
| `TestRawConfig` | `test_raw_config_format_is_valid` | Verifica que el formato raw es uno de los soportados |
| `TestRawConfig` | `test_raw_config_retention_mode_is_valid` | Valida modo de retencion |

## Dependencias

| Paquete | Uso |
|---|---|
| `seleniumbase` | Automatizacion de navegador con soporte anti-deteccion |
| `pandas` | Manipulacion y exportacion de datos |
| `pyyaml` | Lectura de archivos de configuracion YAML |
| `pytest` | Framework de tests |
| `openpyxl` | Exportacion a Excel (.xlsx) |

## Licencia

Este proyecto es open source y esta disponible bajo la [Licencia MIT](LICENSE).

## Aviso Legal

Esta plantilla esta destinada exclusivamente para fines educativos y de aprendizaje. Antes de realizar scraping en cualquier sitio web, asegurate de:

- Revisar y respetar los terminos de servicio del sitio
- Consultar el archivo `robots.txt`
- No sobrecargar los servidores con peticiones excesivas
- Respetar la privacidad y los datos personales

El uso responsable del web scraping es responsabilidad del usuario.
