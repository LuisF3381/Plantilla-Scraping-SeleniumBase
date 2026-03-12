import logging
import os
import pandas as pd


def process(filename: str, extension: str, suffix: str, raw_config: dict) -> list[dict]:
    """
    Lee el archivo raw y aplica transformaciones a los datos.

    Args:
        filename:   Nombre base del archivo (ej: "viviendas")
        extension:  Extension del archivo   (ej: "csv")
        suffix:     Sufijo timestamp de la ejecucion (ej: "20260312_143052")
        raw_config: Diccionario con configuracion del raw

    Returns:
        list[dict]: Lista de diccionarios con los datos procesados
    """
    filepath: str = os.path.join(raw_config["raw_folder"], f"{filename}_{suffix}.{extension}")
    df: pd.DataFrame = pd.read_csv(filepath)

    # --- Inicio del procesamiento ---

    # Limpieza de espacios en todas las columnas de texto
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].str.strip()

    # Extraccion del precio numerico (elimina simbolo de moneda, separadores y texto)
    if "Precio" in df.columns:
        df["Precio_Numerico"] = (
            df["Precio"]
            .str.replace(r"[^\d]", "", regex=True)
            .apply(lambda x: int(x) if x else None)
        )

    # --- Fin del procesamiento ---

    logger: logging.Logger = logging.getLogger("scrapecraft")
    logger.info(f"Procesamiento completado: {len(df)} registros")

    return df.to_dict(orient="records")
