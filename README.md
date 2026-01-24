# Plantilla Scraping SeleniumBase

Plantilla para proyectos de web scraping usando SeleniumBase con soporte para evasión de detección.

## Estructura

```
├── config.py           # Configuración del driver
├── driver_config.py    # Clase DriverConfig para inicializar el navegador
├── main.py             # Script principal de scraping
└── test_driver_config.py  # Tests de configuración
```

## Configuración

Edita `config.py` para ajustar el comportamiento del driver:

```python
DRIVER_CONFIG = {
    "headless": False,      # Ejecutar sin interfaz gráfica
    "undetected": True,     # Modo anti-detección
    "maximize": True,       # Maximizar ventana
    "window_size": None,    # Tamaño específico: (1920, 1080)
    "user_agent": None,     # User agent personalizado
    "proxy": None           # Proxy: "ip:puerto"
}
```

## Uso

```bash
# Instalar dependencias
pip install seleniumbase pandas

# Ejecutar scraping
python main.py

# Ejecutar tests
pytest test_driver_config.py -v
```

## Requisitos

- Python 3.8+
- SeleniumBase
- pandas
