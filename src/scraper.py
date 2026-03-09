from selenium.webdriver.common.by import By
import time


def scrape(driver, web_config, logger):
    """
    Extrae datos desde la URL usando los selectores del archivo de configuracion.

    Args:
        driver: Instancia del driver de SeleniumBase
        web_config: Diccionario con url, xpath_selectors y waits
        logger: Logger para registrar eventos

    Returns:
        list: Lista de diccionarios con los datos extraidos
    """
    url = web_config["url"]
    selectors = web_config["xpath_selectors"]
    waits = web_config["waits"]

    driver.uc_open_with_reconnect(url, waits["reconnect_attempts"])
    driver.uc_gui_handle_captcha()
    logger.info("Pagina cargada correctamente")

    time.sleep(waits["after_load"])

    items = driver.find_elements(By.XPATH, selectors["container"])
    logger.info(f"Encontrados {len(items)} elementos")

    datos = []
    for i, item in enumerate(items, 1):
        registro = {"Numero": i}
        for field_name, field_xpath in selectors.items():
            if field_name == "container":
                continue
            text = item.find_element(By.XPATH, field_xpath).text
            registro[field_name] = text.replace("\n", " | ").strip()
        datos.append(registro)

    return datos
