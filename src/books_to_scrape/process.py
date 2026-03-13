import logging
import pandas as pd

logger = logging.getLogger(__name__)

# Mapa de rating textual a valor numerico
_RATING_MAP = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5,
}


def process(df: pd.DataFrame) -> list[dict]:
    """
    Aplica transformaciones a los datos raw de books.toscrape.com.

    Transformaciones:
      - Precio_GBP:      extrae el valor numerico del precio (ej: "£51.77" → 51.77)
      - Rating_Numerico: convierte el rating textual a entero (ej: "star-rating Three" → 3)

    Args:
        df: DataFrame con columnas Numero, Titulo, Precio, Rating

    Returns:
        list[dict]: Lista de diccionarios con los datos procesados
    """

    # Limpieza de espacios en columnas de texto
    for col in df.select_dtypes(include=["object", "str"]).columns:
        df[col] = df[col].str.strip()

    # Precio: "£51.77" → 51.77 (float)
    if "Precio" in df.columns:
        df["Precio_GBP"] = (
            df["Precio"]
            .str.replace("£", "", regex=False)
            .str.strip()
            .apply(lambda x: float(x) if x else None)
        )

    # Rating: "star-rating Three" → 3 (int)
    if "Rating" in df.columns:
        df["Rating_Numerico"] = (
            df["Rating"]
            .str.split()
            .str[-1]
            .map(_RATING_MAP)
        )

    logger.info(f"Procesamiento completado: {len(df)} registros")

    return df.to_dict(orient="records")
