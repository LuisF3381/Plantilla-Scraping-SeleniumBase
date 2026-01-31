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
# CONFIGURACIÓN DE DATOS (formato de la broad)
# ============================================

DATA_CONFIG = {
    # Formato de salida: "csv", "json", "xml"
    "format": "csv",

    # Opciones específicas por formato:
    # CSV: encoding para caracteres especiales
    "csv_encoding": "utf-8-sig",

    # JSON: indent para formato legible (None para compacto)
    "json_indent": 2,

    # XML: nombre del elemento raíz y de cada registro
    "xml_root": "registros",
    "xml_row": "registro"
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
