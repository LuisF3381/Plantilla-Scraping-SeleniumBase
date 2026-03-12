from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


def safe_get_text(element, xpath: str, fallback: str = "") -> str:
    """
    Extrae el texto de un sub-elemento dado su XPath relativo.
    Retorna `fallback` si el elemento no existe en lugar de lanzar una excepcion.

    Args:
        element:  Elemento padre desde el que se busca (WebElement de Selenium)
        xpath:    XPath relativo al elemento padre
        fallback: Valor a retornar si el elemento no se encuentra (por defecto "")

    Returns:
        Texto del elemento limpio, o `fallback` si no existe
    """
    try:
        text = element.find_element(By.XPATH, xpath).text
        return text.replace("\n", " | ").strip()
    except NoSuchElementException:
        return fallback


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
    registro: dict = {"Numero": index}
    for field_name, field_xpath in selectors.items():
        if field_name == "container":
            continue
        registro[field_name] = safe_get_text(item, field_xpath)
    return registro
