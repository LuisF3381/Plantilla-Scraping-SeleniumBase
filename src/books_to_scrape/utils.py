from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


def safe_get_text(element, xpath: str, fallback: str = "") -> str:
    """
    Extrae el texto de un sub-elemento dado su XPath relativo.
    Retorna `fallback` si el elemento no existe.
    """
    try:
        text = element.find_element(By.XPATH, xpath).text
        return text.replace("\n", " | ").strip()
    except NoSuchElementException:
        return fallback


def safe_get_attr(element, xpath: str, attr: str, fallback: str = "") -> str:
    """
    Extrae el valor de un atributo HTML de un sub-elemento dado su XPath relativo.
    Retorna `fallback` si el elemento o el atributo no existe.

    Args:
        element:  Elemento padre desde el que se busca (WebElement de Selenium)
        xpath:    XPath relativo al elemento padre
        attr:     Nombre del atributo HTML a extraer (ej: "title", "class", "href")
        fallback: Valor a retornar si no se encuentra

    Returns:
        Valor del atributo, o `fallback` si no existe
    """
    try:
        value = element.find_element(By.XPATH, xpath).get_attribute(attr)
        return value.strip() if value else fallback
    except NoSuchElementException:
        return fallback


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
