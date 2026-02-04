# Changelog

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
