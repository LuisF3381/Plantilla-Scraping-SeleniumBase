# Changelog

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
