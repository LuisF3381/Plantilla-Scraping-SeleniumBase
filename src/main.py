from selenium.webdriver.common.by import By
import time
import os
from datetime import datetime
import pandas as pd
import yaml
from src.driver_config import DriverConfig
from config import settings


def load_web_config(path="config/web_config.yaml"):
    """Carga la configuracion de la web desde el archivo YAML."""
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def build_filepath(storage_config, data_config):
    """
    Construye la ruta del archivo según el modo de nombrado configurado.

    Args:
        storage_config: Diccionario con configuración de almacenamiento
        data_config: Diccionario con configuración de datos (para obtener extensión)

    Returns:
        str: Ruta completa del archivo a guardar
    """
    output_folder = storage_config["output_folder"]
    filename = storage_config["filename"]
    naming_mode = storage_config["naming_mode"]
    extension = data_config["format"]

    now = datetime.now()
    date_str = now.strftime("%Y%m%d")
    timestamp_str = now.strftime("%Y%m%d_%H%M%S")

    if naming_mode == "overwrite":
        filepath = os.path.join(output_folder, f"{filename}.{extension}")

    elif naming_mode == "date_suffix":
        filepath = os.path.join(output_folder, f"{filename}_{date_str}.{extension}")

    elif naming_mode == "timestamp_suffix":
        filepath = os.path.join(output_folder, f"{filename}_{timestamp_str}.{extension}")

    elif naming_mode == "date_folder":
        folder_path = os.path.join(output_folder, date_str)
        os.makedirs(folder_path, exist_ok=True)
        filepath = os.path.join(folder_path, f"{filename}.{extension}")

    else:
        raise ValueError(f"Modo de nombrado no soportado: {naming_mode}")

    return filepath


def save_data(datos, data_config, storage_config):
    """
    Guarda los datos en el formato y ubicación especificados.

    Args:
        datos: Lista de diccionarios con los datos a guardar
        data_config: Diccionario con configuración del formato de datos
        storage_config: Diccionario con configuración de almacenamiento
    """
    df = pd.DataFrame(datos)
    fmt = data_config["format"]
    filepath = build_filepath(storage_config, data_config)

    if fmt == "csv":
        df.to_csv(filepath, index=False, encoding=data_config["csv_encoding"])

    elif fmt == "json":
        df.to_json(filepath, orient="records", indent=data_config["json_indent"], force_ascii=False)

    elif fmt == "xml":
        df.to_xml(filepath, index=False, root_name=data_config["xml_root"], row_name=data_config["xml_row"])

    else:
        raise ValueError(f"Formato no soportado: {fmt}")

    print(f"Datos guardados en {filepath} ({len(datos)} registros)")


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
    driver_config = DriverConfig(**settings.DRIVER_CONFIG)
    driver = driver_config.get_driver()

    try:
        datos = scrape(driver, web_config)
        save_data(datos, settings.DATA_CONFIG, settings.STORAGE_CONFIG)
    finally:
        driver.quit()


if __name__ == "__main__":
    main()