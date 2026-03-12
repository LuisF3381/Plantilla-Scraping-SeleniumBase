# Changelog

## [0.13.0] - 2026-03-12

### Added
- Nuevo modulo `src/<job>/utils.py` con funciones auxiliares de extraccion reutilizables:
  - `safe_get_text(element, xpath, fallback)`: extrae texto de un sub-elemento con manejo seguro de `NoSuchElementException`
  - `parse_record(item, selectors, index)`: construye el diccionario de un registro a partir de un elemento contenedor

### Changed
- `app_job.py` refactorizado para mayor legibilidad:
  - `run()` queda como dispatcher limpio de ~10 lineas
  - Logica extraida en funciones privadas: `_run_full()`, `_run_reprocess()`, `_save_output()`
  - Bloque de comentario con mapa visual del flujo ETL al inicio del archivo
- `scraper.py` refactorizado para usar `utils.py`:
  - For-loop de extraccion de campos reemplazado por llamada a `parse_record()`
  - Secciones marcadas con `# IMPLEMENTAR` para guiar al data engineer
- `process()` en `process.py` ahora recibe `logger` como parametro opcional en lugar de obtenerlo internamente via `logging.getLogger()`
- `build_filepath()` en `storage.py` ahora crea automaticamente la carpeta de salida con `os.makedirs(exist_ok=True)` si no existe

### Architecture
- `utils.py` como punto de extension natural: el data engineer agrega helpers de extraccion ahi sin tocar el flujo principal de `scraper.py`
- Consistencia en el paso de `logger`: todos los modulos del job (`scraper.py`, `process.py`) lo reciben como parametro

## [0.12.0] - 2026-03-12

### Added
- Soporte para **multiples procesos de scraping** mediante arquitectura multi-job
- Carpeta `src/shared/` con modulos reutilizables entre todos los jobs: `storage.py`, `driver_config.py`, `logger.py`
- Carpeta `src/viviendas_adonde/` como primer job concreto, con `scraper.py`, `process.py` y `app_job.py`
- Modulo `app_job.py` por proceso: encapsula el flujo ETL completo y expone `run(args)` como interfaz estandar
- Funcion `load_web_config()` movida de `main.py` a cada `app_job.py` con su ruta de config propia
- `config/global_settings.py` con configuracion compartida entre todos los jobs: `LOG_CONFIG` y `DATA_CONFIG`
- Carpeta `config/viviendas_adonde/` con `settings.py` (config especifica del job) y `web_config.yaml`
- Carpetas de salida por proceso: `output/viviendas_adonde/` y `raw/viviendas_adonde/`
- Tests globales en `tests/test_global.py`: `TestLogConfig` y `TestDataConfig`
- Tests por proceso en `tests/viviendas_adonde/test_config.py`: `TestWebConfig`, `TestStorageConfig`, `TestDriverConfig`, `TestRawConfig`

### Changed
- `main.py` refactorizado como **dispatcher dinamico**: carga el job indicado via `importlib` y llama `run(args)`
- CLI actualizado: argumento `--job` requerido para indicar el proceso a ejecutar
- `config/viviendas_adonde/settings.py` ahora solo contiene `DRIVER_CONFIG`, `STORAGE_CONFIG` y `RAW_CONFIG`
- `STORAGE_CONFIG["output_folder"]` actualizado a `output/viviendas_adonde`
- `RAW_CONFIG["raw_folder"]` actualizado a `raw/viviendas_adonde`
- Tests reorganizados en subdirectorios por proceso (espejo de la estructura `src/`)

### Removed
- `src/scraper.py`, `src/process.py`, `src/storage.py`, `src/driver_config.py`, `src/logger.py` — movidos a `src/shared/` o `src/viviendas_adonde/`
- `config/settings.py` y `config/web_config.yaml` — reemplazados por `config/global_settings.py` y `config/viviendas_adonde/`
- `tests/test_config.py` — reemplazado por `tests/test_global.py` y `tests/viviendas_adonde/test_config.py`

### Architecture
- Patron **multi-job dispatcher**: `main.py` es generico y delega en cada `app_job.py` segun `--job`
- Convencion de interfaz: todo job debe exponer `def run(args: argparse.Namespace) -> None` en su `app_job.py`
- Agregar un nuevo proceso = crear `src/<nombre>/app_job.py` + `config/<nombre>/` sin modificar `main.py`
- Tests siguen la misma estructura de carpetas que `src/` y `config/`

### CLI
```bash
python -m src.main --job viviendas_adonde
python -m src.main --job viviendas_adonde --reprocess 20260312_143052
```

## [0.11.0] - 2026-03-12

### Added
- Modulo `src/process.py` con funcion `process()` para transformacion de datos entre scraping y guardado final
- Funcion `save_raw()` en `storage.py`: guarda datos en bruto como CSV con sufijo timestamp, retorna el sufijo generado
- Funcion `cleanup_raw()` en `storage.py`: aplica politica de retencion sobre la carpeta `raw/`
- Configuracion `RAW_CONFIG` en `config/settings.py` con `raw_folder`, `filename`, `format` y `retention`
- Soporte CLI con `argparse`: flag `--reprocess <SUFFIX>` para reprocesar un raw existente sin volver a scrapear
- Carpeta `raw/` para almacenar archivos intermedios
- Clase `TestRawConfig` en `tests/test_config.py` con 4 tests de validacion

### Changed
- `main.py` ampliado con dos flujos diferenciados:
  - **Flujo completo**: scraping → save_raw → process → cleanup_raw → save_data
  - **Flujo reprocess** (`--reprocess SUFFIX`): process → save_data
- `main.py` libera memoria (`del datos`) entre save_raw y process para soportar datasets grandes

### Architecture
- Pipeline de datos en tres etapas: raw (CSV) → process (list[dict]) → output (formatos configurados)
- `process()` recibe `filename`, `extension` y `suffix`; resuelve el path internamente desde `raw_config`
- El sufijo timestamp es el identificador unico de cada ejecucion de scraping

## [0.10.0] - 2026-03-09

### Added
- Campo `output_formats` en `STORAGE_CONFIG` para configurar formatos de salida
- Soporte para exportar a multiples formatos simultaneamente
- Type hints en todos los modulos: `main.py`, `scraper.py`, `storage.py`, `driver_config.py`, `logger.py`

### Changed
- `main.py` ahora itera sobre `output_formats` para exportar a todos los formatos configurados
- Formato de salida ya no esta hardcodeado, es configurable via `STORAGE_CONFIG`

## [0.9.0] - 2026-03-09

### Added
- Modulo `src/scraper.py` con funcion `scrape()` para logica de extraccion
- Modulo `src/storage.py` con funciones `save_data()` y `build_filepath()`
- Seccion "Arquitectura" en README con diagrama de flujo
- Seccion "API Reference" en README con documentacion de funciones publicas

### Changed
- Refactorizacion de `main.py` aplicando Single Responsibility Principle
- `main.py` reducido de 177 a 39 lineas (solo orquestacion)
- `load_web_config()` ahora tiene logger como parametro opcional (compatibilidad con tests)
- README actualizado con nueva estructura de archivos

### Architecture
- Separacion de responsabilidades en 3 modulos:
  - `main.py`: Orquestacion del flujo
  - `scraper.py`: Logica de extraccion de datos
  - `storage.py`: Persistencia y exportacion

## [0.8.0] - 2026-02-03

### Added
- Sistema de logging con salida dual (archivo + consola)
- Modulo `src/logger.py` con funcion `setup_logger()`
- Configuracion `LOG_CONFIG` en `config/settings.py`
- Carpeta `log/` para almacenar archivos de log
- Logs nombrados por fecha: `scrapecraft_YYYYMMDD.log`
- Logging en puntos clave: inicio, carga config, driver, scraping, guardado, fin
- Manejo de errores con traceback en logs

### Changed
- Proyecto renombrado a **ScrapeCraft**
- `print()` reemplazado por `logger.info()` / `logger.error()` en todo el proyecto
- `load_web_config()` ahora recibe logger como parametro
- `scrape()` ahora recibe logger como parametro
- README actualizado con nuevo nombre, seccion de proposito y aviso legal

### Updated
- `.gitignore` ahora ignora archivos `.log` pero mantiene `log/.gitkeep`

## [0.7.0] - 2026-01-30

### Changed
- `DATA_CONFIG` reestructurado como diccionario anidado con configuraciones independientes por formato
- Cada formato (csv, json, xml, xlsx) tiene su propia configuracion separada
- Funcion `save_data()` ahora recibe `format` como parametro independiente
- Funcion `build_filepath()` ahora recibe `format` como parametro en lugar de `data_config`

### Added
- Soporte para formato Excel (`xlsx`) con opciones `sheet_name` e `index`
- Nuevas opciones para CSV: `separator`, `index`
- Nuevas opciones para JSON: `orient`, `force_ascii`

### Tests
- Simplificado `TestDataConfig` a un solo test que valida existencia y al menos un formato
- Total de tests: 12 (antes 14)

### Removed
- Campo `format` de nivel superior en DATA_CONFIG (ahora el formato se pasa como parametro)

## [0.6.0] - 2026-01-30

### Added
- Nueva configuracion `DATA_CONFIG` para formato de datos (csv_encoding, json_indent, xml_root, xml_row)
- Nueva configuracion `STORAGE_CONFIG` para almacenamiento (output_folder, filename, naming_mode)
- Funcion `build_filepath()` en `main.py` para construir rutas segun modo de nombrado
- Soporte para 4 modos de nombrado de archivos:
  - `overwrite`: Sobrescribe el archivo existente (viviendas.csv)
  - `date_suffix`: Añade fecha al nombre (viviendas_20260130.csv)
  - `timestamp_suffix`: Añade fecha y hora (viviendas_20260130_143052.csv)
  - `date_folder`: Crea subcarpeta con fecha (20260130/viviendas.csv)

### Changed
- `OUTPUT_CONFIG` separado en `DATA_CONFIG` y `STORAGE_CONFIG` para mejor organizacion
- Funcion `save_data()` ahora recibe `data_config` y `storage_config` como argumentos separados
- Carpeta de salida ahora es configurable via `STORAGE_CONFIG["output_folder"]`

### Removed
- `OUTPUT_CONFIG` reemplazado por las nuevas configuraciones separadas

### Tests
- Clase `TestDataConfig` con 3 tests para validar DATA_CONFIG
- Clase `TestStorageConfig` con 4 tests para validar STORAGE_CONFIG
- Total de tests: 14 (antes 7)

## [0.5.0] - 2026-01-24

### Added
- Carpeta `src/` para codigo fuente
- Carpeta `config/` para archivos de configuracion
- Carpeta `tests/` para tests
- Carpeta `output/` para archivos generados
- Archivos `__init__.py` en cada paquete
- Archivo `.gitkeep` en `output/`

### Changed
- Reorganizacion del proyecto siguiendo estandar Python (src layout)
- `config.py` renombrado a `config/settings.py`
- `web_config.yaml` movido a `config/`
- `main.py` y `driver_config.py` movidos a `src/`
- `test_driver_config.py` movido a `tests/test_config.py`
- Archivos de salida ahora se guardan en `output/`
- Actualizados imports en todos los modulos

## [0.4.0] - 2026-01-24

### Added
- Archivo `requirements.txt` con dependencias del proyecto
- Clase `TestWebConfig` con validaciones:
  - `test_web_config_file_exists`: Verifica existencia del YAML
  - `test_web_config_has_required_keys`: Valida claves requeridas
  - `test_url_format_is_valid`: Valida formato de URL (http/https + dominio)
  - `test_xpath_selectors_format`: Valida formato XPath (/, // o .//)
  - `test_waits_are_positive_numbers`: Valida que waits sean numeros positivos

## [0.3.0] - 2026-01-24

### Added
- Archivo `web_config.yaml` para configuracion de la web a scrapear
- Funcion `load_web_config()` en `main.py` para cargar configuracion YAML
- Dependencia de `pyyaml` para parsing de archivos YAML

### Changed
- `scrape()` ahora recibe `web_config` en lugar de `url`, usa selectores del YAML
- Selectores XPath externalizados a `web_config.yaml` (url, xpath_selectors, waits)
- La extraccion de campos es dinamica: itera sobre los selectores definidos en el YAML

## [0.2.0] - 2026-01-24

### Added
- Funcion `scrape(driver, url)` en `main.py` para encapsular la logica de extraccion
- Funcion `save_data(datos, output_config)` en `main.py` para guardar datos en multiples formatos
- Soporte para exportar a CSV, JSON y XML usando pandas
- Seccion `OUTPUT_CONFIG` en `config.py` con opciones:
  - `format`: Formato de salida (csv/json/xml)
  - `filename`: Nombre del archivo sin extension
  - `csv_encoding`: Encoding para CSV
  - `json_indent`: Indentacion para JSON
  - `xml_root` / `xml_row`: Nombres de elementos XML

### Changed
- Refactorizado `main.py` con estructura modular: `scrape()`, `save_data()`, `main()`
- `main()` ahora usa `try/finally` para asegurar cierre del driver
- Agregado `if __name__ == "__main__":` para ejecucion como script

### Removed
- Import no utilizado de `selenium.webdriver`
- Comentarios redundantes en `main.py`

## [0.1.0] - 2026-01-23

### Added
- Estructura inicial del proyecto
- `config.py` con `DRIVER_CONFIG` para configuracion centralizada del driver
- `driver_config.py` con clase `DriverConfig` para inicializar SeleniumBase
- `main.py` con script de scraping basico
- `test_driver_config.py` con tests para verificar inicializacion del driver
- Soporte para opciones: headless, undetected, maximize, window_size, user_agent, proxy
