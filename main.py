from selenium.webdriver.common.by import By
import time
import pandas as pd
from driver_config import DriverConfig
import config


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


def scrape(driver, url):
    """
    Extrae datos de viviendas desde la URL especificada.

    Args:
        driver: Instancia del driver de SeleniumBase
        url: URL a scrapear

    Returns:
        list: Lista de diccionarios con los datos extraídos
    """
    driver.uc_open_with_reconnect(url, 3)
    driver.uc_gui_handle_captcha()
    print("✓ Página cargada correctamente")

    time.sleep(5)

    tarjetas = driver.find_elements(By.XPATH, '//div[@class="postingCard-module__posting-container"]')

    datos = []
    for i, vivienda in enumerate(tarjetas, 1):
        precio = vivienda.find_element(By.XPATH, './/div[@class="postingPrices-module__price"]').text
        direccion = vivienda.find_element(By.XPATH, './/span[@class="postingLocations-module__location-address postingLocations-module__location-address-in-listing"]').text
        caracteristicas = vivienda.find_element(By.XPATH, './/h3').text
        descripcion = vivienda.find_element(By.XPATH, './/div[@data-qa="POSTING_CARD_DESCRIPTION"]').text

        datos.append({
            'Numero': i,
            'Precio': precio,
            'Direccion': direccion,
            'Caracteristicas': caracteristicas,
            'Descripcion': descripcion
        })

    return datos


def main():
    driver_config = DriverConfig(**config.DRIVER_CONFIG)
    driver = driver_config.get_driver()

    try:
        url = "https://www.adondevivir.com/inmuebles-en-alquiler.html"
        datos = scrape(driver, url)
        save_data(datos, config.OUTPUT_CONFIG)
    finally:
        driver.quit()


if __name__ == "__main__":
    main()