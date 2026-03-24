from src.shared.utils import safe_get_text, safe_get_attr


def parse_record(item, selectors: dict, index: int) -> dict:
    """
    Construye el diccionario de un registro a partir de un elemento contenedor.
    Omite automaticamente el selector "container" ya que es el padre, no un campo.

    Args:
        item:      Elemento WebElement que representa un registro (el contenedor)
        selectors: Diccionario {nombre_campo: xpath} del web_config.yaml
        index:     Numero de registro (se guarda como campo "Numero")

    Returns:
        dict con todos los campos extraidos del elemento
    """
    # =========================================================================
    # ZONA DATA ENGINEER — implementar extraccion campo a campo
    # =========================================================================
    registro: dict = {"Numero": index}
    for field_name, field_xpath in selectors.items():
        if field_name == "container":
            continue
        registro[field_name] = safe_get_text(item, field_xpath)
    return registro
