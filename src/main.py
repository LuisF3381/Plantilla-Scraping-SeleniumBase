import argparse
import logging
import yaml
from src.driver_config import DriverConfig
from src.logger import setup_logger
from src.scraper import scrape
from src.storage import save_data, save_raw, cleanup_raw
from src.process import process
from config import settings


def load_web_config(logger: logging.Logger | None = None, path: str = "config/web_config.yaml") -> dict:
    """Carga la configuracion de la web desde el archivo YAML."""
    with open(path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    if logger:
        logger.info(f"Configuracion cargada: {config['url']}")
    return config


def main() -> None:
    parser = argparse.ArgumentParser(description="ScrapeCraft - Web scraper configurable")
    parser.add_argument(
        "--reprocess",
        metavar="SUFFIX",
        help="Reprocesar raw existente indicando su sufijo (ej: 20260312_143052)"
    )
    args = parser.parse_args()

    logger = setup_logger(**settings.LOG_CONFIG)
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
            save_data(processed, formato, settings.DATA_CONFIG, settings.STORAGE_CONFIG)

        logger.info("Proceso finalizado")

    except Exception as e:
        logger.error(f"Error durante la ejecucion: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
