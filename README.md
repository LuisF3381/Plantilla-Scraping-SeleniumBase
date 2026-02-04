# ScrapeCraft

Plantilla open source para construir web scrapers de forma facil y rapida. Basada en [SeleniumBase](https://github.com/seleniumbase/SeleniumBase), un framework de automatizacion con soporte integrado para evasion de deteccion.

## Proposito

ScrapeCraft busca ser un punto de partida para cualquier persona que quiera aprender web scraping o construir sus propios scrapers para **fines educativos y divertidos**. La plantilla esta disenada para ser:

- **Facil de usar**: Configura tu scraper editando archivos YAML y Python, sin tocar el codigo principal
- **Flexible**: Soporta multiples formatos de salida (CSV, JSON, XML, Excel)
- **Robusta**: Incluye sistema de logging, manejo de errores y evasion de deteccion

## Estructura

```
├── src/                      # Codigo fuente
│   ├── main.py               # Script principal
│   ├── driver_config.py      # Configuracion del driver
│   └── logger.py             # Sistema de logging
├── config/                   # Configuraciones
│   ├── settings.py           # Config del driver, datos y logging
│   └── web_config.yaml       # URL, selectores y waits
├── log/                      # Logs de ejecucion
├── output/                   # Archivos generados
├── tests/                    # Tests
├── requirements.txt
├── CHANGELOG.md
└── LICENSE
```

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
    "naming_mode": "date_suffix"
}
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
# Ejecutar scraping
python -m src.main

# Ejecutar tests
pytest tests/ -v
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

## Requisitos

- Python 3.8+
- SeleniumBase
- pandas
- pyyaml
- pytest

## Licencia

Este proyecto es open source y esta disponible bajo la [Licencia MIT](LICENSE).

## Aviso Legal

Esta plantilla esta destinada exclusivamente para fines educativos y de aprendizaje. Antes de realizar scraping en cualquier sitio web, asegurate de:

- Revisar y respetar los terminos de servicio del sitio
- Consultar el archivo `robots.txt`
- No sobrecargar los servidores con peticiones excesivas
- Respetar la privacidad y los datos personales

El uso responsable del web scraping es responsabilidad del usuario.
