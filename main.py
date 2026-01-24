from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
from driver_config import DriverConfig
import config

# ============================================
# CONFIGURACIÓN DEL DRIVER
# ============================================

# Configurar e inicializar driver usando configuración centralizada
driver_config = DriverConfig(**config.DRIVER_CONFIG)
driver = driver_config.get_driver()

# ============================================
# EXTRACCIÓN
# ============================================

# Abrir URL objetivo con reconexión automática
url = "https://www.adondevivir.com/inmuebles-en-alquiler.html"
driver.uc_open_with_reconnect(url, 3)
driver.uc_gui_handle_captcha()

print("✓ Página cargada correctamente")

time.sleep(5)

# Buscar tarjetas de viviendas usando selector configurado
tarjetas_viviendas = driver.find_elements(By.XPATH, '//div[@class="postingCard-module__posting-container"]')

# Lista para almacenar los datos
datos_viviendas = []

for i, vivienda in enumerate(tarjetas_viviendas, 1):
    precio = vivienda.find_element(By.XPATH, './/div[@class="postingPrices-module__price"]').text
    direccion = vivienda.find_element(By.XPATH, './/span[@class="postingLocations-module__location-address postingLocations-module__location-address-in-listing"]').text
    caracteristicas = vivienda.find_element(By.XPATH, './/h3').text
    descripcion = vivienda.find_element(By.XPATH, './/div[@data-qa="POSTING_CARD_DESCRIPTION"]').text

    # Agregar los datos a la lista
    datos_viviendas.append({
        'Numero': i,
        'Precio': precio,
        'Direccion': direccion,
        'Caracteristicas': caracteristicas,
        'Descripcion': descripcion
    })

# ============================================
# GUARDAR DATOS
# ============================================

# Crear DataFrame y guardar en CSV
df = pd.DataFrame(datos_viviendas)
df.to_csv("viviendas.csv", index=False, encoding='utf-8-sig')
print(f"\n✓ Datos guardados en viviendas.csv ({len(datos_viviendas)} viviendas)")

driver.quit()