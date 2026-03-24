from src.shared.utils import safe_get_text, safe_get_attr


def parse_record(item, selectors: dict, index: int) -> dict:
    """
    Construye el diccionario de un registro para books.toscrape.com.

    Logica especial por campo:
      - Titulo:  extrae el atributo @title del <a> (evita texto truncado)
      - Rating:  extrae el atributo @class del <p> (ej: "star-rating Three")
      - Precio:  extrae el texto directamente (ej: "£51.77")

    Args:
        item:      WebElement que representa un libro (el contenedor <article>)
        selectors: Diccionario {nombre_campo: xpath} del web_config.yaml
        index:     Numero de registro (se guarda como campo "Numero")

    Returns:
        dict con todos los campos extraidos
    """
    # =========================================================================
    # ZONA DATA ENGINEER — implementar extraccion campo a campo
    # =========================================================================
    registro: dict = {"Numero": index}
    for field_name, field_xpath in selectors.items():
        if field_name == "container":
            continue
        if field_name == "Titulo":
            registro[field_name] = safe_get_attr(item, field_xpath, "title")
        elif field_name == "Rating":
            registro[field_name] = safe_get_attr(item, field_xpath, "class")
        else:
            registro[field_name] = safe_get_text(item, field_xpath)
    return registro
