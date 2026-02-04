import logging
import os
from datetime import datetime


def setup_logger(log_folder="log", level="INFO"):
    """
    Configura logger con salida a archivo y consola.

    Args:
        log_folder: Carpeta donde se guardan los logs
        level: Nivel de logging (DEBUG, INFO, WARNING, ERROR)

    Returns:
        Logger configurado
    """
    os.makedirs(log_folder, exist_ok=True)

    log_file = os.path.join(log_folder, f"scrapecraft_{datetime.now():%Y%m%d}.log")

    logger = logging.getLogger("scrapecraft")
    logger.setLevel(getattr(logging, level.upper()))

    # Evitar duplicar handlers si se llama múltiples veces
    if logger.handlers:
        return logger

    # Formato: timestamp - nivel - mensaje
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    # Handler archivo
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(formatter)

    # Handler consola
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
