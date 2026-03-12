import argparse
import logging
import yaml
from src.shared.driver_config import DriverConfig
from src.shared.logger import setup_logger
from src.shared.storage import save_data, save_raw, cleanup_raw
from src.viviendas_adonde.scraper import scrape
from src.viviendas_adonde.process import process
from config import global_settings
from config.viviendas_adonde import settings

# ---------------------------------------------------------------------------
# FLUJO ETL — vision general
#
#   FLUJO COMPLETO:
#     run() → _run_full() → scrape()    → [scraper.py]   <- implementar aqui
#                         → save_raw()
#                         → process()   → [process.py]   <- implementar aqui
#                         → cleanup_raw()
#           → _save_output()
#
#   FLUJO REPROCESS (--reprocess <sufijo>):
#     run() → _run_reprocess() → process()  → [process.py]
#           → _save_output()
#
#   Como data engineer solo debes implementar scraper.py y process.py.
#   Este archivo no requiere modificaciones.
# ---------------------------------------------------------------------------

WEB_CONFIG_PATH = "config/viviendas_adonde/web_config.yaml"


def load_web_config(logger: logging.Logger | None = None) -> dict:
    """Carga la configuracion de la web desde el archivo YAML."""
    with open(WEB_CONFIG_PATH, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    if logger:
        logger.info(f"Configuracion cargada: {config['url']}")
    return config


# ---------------------------------------------------------------------------
# Flujos internos (no modificar)
# ---------------------------------------------------------------------------

def _run_full(logger: logging.Logger) -> list[dict]:
    """Flujo completo: scraping → raw → procesamiento → limpieza de raw."""
    logger.info("Iniciando scraper...")

    web_config = load_web_config(logger)
    driver = DriverConfig(**settings.DRIVER_CONFIG).get_driver()

    try:
        datos = scrape(driver, web_config, logger)
    finally:
        driver.quit()

    suffix: str = save_raw(datos, settings.RAW_CONFIG)
    del datos

    processed = process(
        filename=settings.RAW_CONFIG["filename"],
        extension=settings.RAW_CONFIG["format"],
        suffix=suffix,
        raw_config=settings.RAW_CONFIG,
        logger=logger,
    )

    cleanup_raw(settings.RAW_CONFIG)
    return processed


def _run_reprocess(suffix: str, logger: logging.Logger) -> list[dict]:
    """Flujo reprocess: omite el scraping y reprocesa un raw existente."""
    logger.info(f"Iniciando reprocesamiento: sufijo {suffix}")
    return process(
        filename=settings.RAW_CONFIG["filename"],
        extension=settings.RAW_CONFIG["format"],
        suffix=suffix,
        raw_config=settings.RAW_CONFIG,
        logger=logger,
    )


def _save_output(processed: list[dict], logger: logging.Logger) -> None:
    """Guarda los datos procesados en todos los formatos configurados."""
    output_formats = settings.STORAGE_CONFIG.get("output_formats", ["csv"])
    for formato in output_formats:
        save_data(processed, formato, global_settings.DATA_CONFIG, settings.STORAGE_CONFIG)
    logger.info("Proceso finalizado")


# ---------------------------------------------------------------------------
# Punto de entrada del job (no modificar)
# ---------------------------------------------------------------------------

def run(args: argparse.Namespace) -> None:
    """
    Punto de entrada del job viviendas_adonde.

    Args:
        args.reprocess (str | None): sufijo del raw a reprocesar.
                                     Si es None se ejecuta el flujo completo.
    """
    logger = setup_logger(**global_settings.LOG_CONFIG)

    try:
        if args.reprocess:
            processed = _run_reprocess(args.reprocess, logger)
        else:
            processed = _run_full(logger)

        _save_output(processed, logger)

    except Exception as e:
        logger.error(f"Error durante la ejecucion: {e}", exc_info=True)
        raise
