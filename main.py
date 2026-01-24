from selenium.webdriver.common.by import By
import time
import pandas as pd
import yaml
from driver_config import DriverConfig
import config


def load_web_config(path="web_config.yaml"):
    """Carga la configuracion de la web desde el archivo YAML."""
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def save_data(datos, output_config):
    """
    Guarda los datos en el formato especificado.

    Args:
        datos: Lista de diccionarios con los datos a guardar
        output_config: Diccionario con la configuración de output
    """
    df = pd.DataFrame(datos)
    fmt = output_config["format"]
    filename = output_config["filename"]

    if fmt == "csv":
        filepath = f"{filename}.csv"
        df.to_csv(filepath, index=False, encoding=output_config["csv_encoding"])

    elif fmt == "json":
        filepath = f"{filename}.json"
        df.to_json(filepath, orient="records", indent=output_config["json_indent"], force_ascii=False)

    elif fmt == "xml":
        filepath = f"{filename}.xml"
        df.to_xml(filepath, index=False, root_name=output_config["xml_root"], row_name=output_config["xml_row"])

    else:
        raise ValueError(f"Formato no soportado: {fmt}")

    print(f"✓ Datos guardados en {filepath} ({len(datos)} registros)")


def scrape(driver, web_config):
    """
    Extrae datos desde la URL usando los selectores del archivo de configuracion.

    Args:
        driver: Instancia del driver de SeleniumBase
        web_config: Diccionario con url, xpath_selectors y waits

    Returns:
        list: Lista de diccionarios con los datos extraidos
    """
    url = web_config["url"]
    selectors = web_config["xpath_selectors"]
    waits = web_config["waits"]

    driver.uc_open_with_reconnect(url, waits["reconnect_attempts"])
    driver.uc_gui_handle_captcha()
    print("✓ Página cargada correctamente")

    time.sleep(waits["after_load"])

    items = driver.find_elements(By.XPATH, selectors["container"])

    datos = []
    for i, item in enumerate(items, 1):
        registro = {"Numero": i}
        for field_name, field_xpath in selectors.items():
            if field_name == "container":
                continue
            registro[field_name] = item.find_element(By.XPATH, field_xpath).text
        datos.append(registro)

    return datos


def main():
    web_config = load_web_config()
    driver_config = DriverConfig(**config.DRIVER_CONFIG)
    driver = driver_config.get_driver()

    try:
        datos = scrape(driver, web_config)
        save_data(datos, config.OUTPUT_CONFIG)
    finally:
        driver.quit()


if __name__ == "__main__":
    main()