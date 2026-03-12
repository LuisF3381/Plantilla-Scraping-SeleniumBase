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

WEB_CONFIG_PATH = "config/viviendas_adonde/web_config.yaml"


def load_web_config(logger: logging.Logger | None = None) -> dict:
    """Carga la configuracion de la web desde el archivo YAML."""
    with open(WEB_CONFIG_PATH, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    if logger:
        logger.info(f"Configuracion cargada: {config['url']}")
    return config


def run(args: argparse.Namespace) -> None:
    """
    Punto de entrada del job viviendas_adonde.
    Ejecuta el flujo ETL completo o solo el reprocesamiento segun los argumentos.

    Args:
        args: Namespace de argparse con los argumentos de linea de comandos.
              Atributos esperados:
                - reprocess (str | None): sufijo del raw a reprocesar
    """
    logger = setup_logger(**global_settings.LOG_CONFIG)
    output_formats = settings.STORAGE_CONFIG.get("output_formats", ["csv"])

    try:
        if args.reprocess:
            # Flujo reprocess: salta el scraping y va directo al procesamiento
            logger.info(f"Iniciando reprocesamiento: sufijo {args.reprocess}")
            processed = process(
                filename=settings.RAW_CONFIG["filename"],
                extension=settings.RAW_CONFIG["format"],
                suffix=args.reprocess,
                raw_config=settings.RAW_CONFIG
            )
        else:
            # Flujo completo: scraping → raw → procesamiento → limpieza
            logger.info("Iniciando scraper...")
            web_config = load_web_config(logger)
            driver_config = DriverConfig(**settings.DRIVER_CONFIG)
            driver = driver_config.get_driver()

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
                raw_config=settings.RAW_CONFIG
            )

            cleanup_raw(settings.RAW_CONFIG)

        for formato in output_formats:
            save_data(processed, formato, global_settings.DATA_CONFIG, settings.STORAGE_CONFIG)

        logger.info("Proceso finalizado")

    except Exception as e:
        logger.error(f"Error durante la ejecucion: {e}", exc_info=True)
        raise
