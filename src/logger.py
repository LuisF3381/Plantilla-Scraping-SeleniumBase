import logging
import os
from datetime import datetime


def setup_logger(log_folder: str = "log", level: str = "INFO") -> logging.Logger:
    """
    Configura logger con salida a archivo y consola.

    Args:
        log_folder: Carpeta donde se guardan los logs
        level: Nivel de logging (DEBUG, INFO, WARNING, ERROR)

    Returns:
        Logger configurado
    """
    os.makedirs(log_folder, exist_ok=True)

    log_file: str = os.path.join(log_folder, f"scrapecraft_{datetime.now():%Y%m%d}.log")

    logger: logging.Logger = logging.getLogger("scrapecraft")
    logger.setLevel(getattr(logging, level.upper()))

    if logger.handlers:
        return logger

    formatter: logging.Formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    file_handler: logging.FileHandler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(formatter)

    console_handler: logging.StreamHandler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
