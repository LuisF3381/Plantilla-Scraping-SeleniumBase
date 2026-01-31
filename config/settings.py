"""
Archivo de configuración para el proyecto de scraping.
"""

# ============================================
# CONFIGURACIÓN DEL DRIVER
# ============================================

DRIVER_CONFIG = {
    # Modo headless: Ejecutar sin interfaz gráfica (útil para producción/servidores)
    "headless": False,

    # Undetected mode: Activar undetected-chromedriver para evadir detección
    "undetected": True,

    # Maximizar ventana: Maximizar automáticamente la ventana del navegador
    "maximize": True,

    # Tamaño de ventana: Tupla (ancho, alto) para tamaño específico
    # Si se define, tiene prioridad sobre maximize
    "window_size": None,  # Ejemplo: (1920, 1080)

    # User agent: User agent personalizado para simular diferentes navegadores
    "user_agent": None,  # Ejemplo: "Mozilla/5.0 (Windows NT 10.0; Win64; x64)..."

    # Proxy: Servidor proxy en formato "ip:puerto"
    "proxy": None  # Ejemplo: "123.45.67.89:8080"
}

# ============================================
# CONFIGURACIÓN DE DATOS (formatos de exportación)
# ============================================

DATA_CONFIG = {
    # Configuración para CSV
    "csv": {
        "encoding": "utf-8",
        "separator": ";",
        "index": False
    },

    # Configuración para JSON
    "json": {
        "indent": 2,
        "force_ascii": False,
        "orient": "records"
    },

    # Configuración para XML
    "xml": {
        "root": "registros",
        "row": "registro"
    },

    # Configuración para Excel
    "xlsx": {
        "sheet_name": "Datos",
        "index": False
    }
}

# ============================================
# CONFIGURACIÓN DE ALMACENAMIENTO
# ============================================

STORAGE_CONFIG = {
    # Carpeta de salida (relativa a la raíz del proyecto)
    "output_folder": "output",

    # Nombre base del archivo (sin extensión)
    "filename": "viviendas",

    # Modo de nombrado del archivo:
    # - "overwrite": Sobrescribe el archivo (viviendas.csv)
    # - "date_suffix": Añade fecha al nombre (viviendas_20260130.csv)
    # - "timestamp_suffix": Añade fecha y hora (viviendas_20260130_143052.csv)
    # - "date_folder": Crea subcarpeta con fecha (20260130/viviendas.csv)
    "naming_mode": "date_suffix"
}
