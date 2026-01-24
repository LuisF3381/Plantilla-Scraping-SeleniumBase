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
# CONFIGURACIÓN DE OUTPUT
# ============================================

OUTPUT_CONFIG = {
    # Formato de salida: "csv", "json", "xml"
    "format": "csv",

    # Nombre del archivo (sin extensión, se agrega automáticamente)
    "filename": "viviendas",

    # Opciones específicas por formato:
    # CSV: encoding para caracteres especiales
    "csv_encoding": "utf-8-sig",

    # JSON: indent para formato legible (None para compacto)
    "json_indent": 2,

    # XML: nombre del elemento raíz y de cada registro
    "xml_root": "registros",
    "xml_row": "registro"
}
