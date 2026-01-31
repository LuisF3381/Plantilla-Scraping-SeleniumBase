# Plantilla Scraping SeleniumBase

Plantilla para proyectos de web scraping usando SeleniumBase con soporte para evasion de deteccion.

## Estructura

```
├── src/                      # Codigo fuente
│   ├── main.py               # Script principal
│   └── driver_config.py      # Configuracion del driver
├── config/                   # Configuraciones
│   ├── settings.py           # Config del driver y output
│   └── web_config.yaml       # URL, selectores y waits
├── tests/                    # Tests
│   └── test_config.py
├── output/                   # Archivos generados
├── requirements.txt
└── CHANGELOG.md
```

## Instalacion

```bash
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

### Datos (`config/settings.py`)

Configura el formato de los datos exportados:

```python
DATA_CONFIG = {
    "format": "csv",            # Formato: "csv", "json", "xml"
    "csv_encoding": "utf-8-sig",
    "json_indent": 2,
    "xml_root": "registros",
    "xml_row": "registro"
}
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
| `test_settings_has_data_config` | Verifica DATA_CONFIG existe |
| `test_data_config_has_required_keys` | Valida claves requeridas |
| `test_data_config_format_is_valid` | Valida formato (csv/json/xml) |

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
