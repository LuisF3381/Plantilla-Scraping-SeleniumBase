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
