import pytest
import os
import re
from urllib.parse import urlparse
from src.driver_config import DriverConfig
from src.main import load_web_config
from config import settings


class TestWebConfig:
    """Tests para validar el archivo web_config.yaml"""

    def test_web_config_file_exists(self):
        """Verifica que existe el archivo web_config.yaml."""
        assert os.path.exists("config/web_config.yaml"), "No existe config/web_config.yaml"
        print("✓ config/web_config.yaml existe")

    def test_web_config_has_required_keys(self):
        """Verifica que el YAML tiene las claves requeridas."""
        web_config = load_web_config()
        assert "url" in web_config, "Falta 'url' en web_config.yaml"
        assert "xpath_selectors" in web_config, "Falta 'xpath_selectors' en web_config.yaml"
        assert "waits" in web_config, "Falta 'waits' en web_config.yaml"
        print("✓ web_config.yaml tiene todas las claves requeridas")

    def test_url_format_is_valid(self):
        """Verifica que la URL tiene formato válido."""
        web_config = load_web_config()
        url = web_config["url"]
        parsed = urlparse(url)
        assert parsed.scheme in ("http", "https"), f"URL debe empezar con http/https: {url}"
        assert parsed.netloc, f"URL no tiene dominio válido: {url}"
        print(f"✓ URL válida: {url}")

    def test_xpath_selectors_format(self):
        """Verifica que los selectores XPath tienen formato válido."""
        web_config = load_web_config()
        selectors = web_config["xpath_selectors"]
        xpath_pattern = re.compile(r"^(\.?//|/)")

        assert "container" in selectors, "Falta selector 'container'"

        for name, xpath in selectors.items():
            assert xpath_pattern.match(xpath), f"XPath inválido para '{name}': {xpath} (debe empezar con / o // o .//)"
            print(f"✓ XPath válido para '{name}'")

    def test_waits_are_positive_numbers(self):
        """Verifica que los waits son números positivos."""
        web_config = load_web_config()
        waits = web_config["waits"]

        assert waits.get("reconnect_attempts", 0) > 0, "reconnect_attempts debe ser > 0"
        assert waits.get("after_load", 0) >= 0, "after_load debe ser >= 0"
        print("✓ Waits tienen valores válidos")


class TestDataConfig:
    """Tests para validar DATA_CONFIG en settings.py"""

    def test_settings_has_data_config(self):
        """Verifica que settings.py tiene DATA_CONFIG."""
        assert hasattr(settings, 'DATA_CONFIG')
        assert isinstance(settings.DATA_CONFIG, dict)
        print("✓ settings.py contiene DATA_CONFIG")

    def test_data_config_has_required_keys(self):
        """Verifica que DATA_CONFIG tiene las claves requeridas."""
        required_keys = ["format", "csv_encoding", "json_indent", "xml_root", "xml_row"]
        for key in required_keys:
            assert key in settings.DATA_CONFIG, f"Falta '{key}' en DATA_CONFIG"
        print("✓ DATA_CONFIG tiene todas las claves requeridas")

    def test_data_config_format_is_valid(self):
        """Verifica que el formato es válido."""
        valid_formats = ["csv", "json", "xml"]
        fmt = settings.DATA_CONFIG["format"]
        assert fmt in valid_formats, f"Formato inválido: {fmt}. Debe ser uno de {valid_formats}"
        print(f"✓ Formato válido: {fmt}")


class TestStorageConfig:
    """Tests para validar STORAGE_CONFIG en settings.py"""

    def test_settings_has_storage_config(self):
        """Verifica que settings.py tiene STORAGE_CONFIG."""
        assert hasattr(settings, 'STORAGE_CONFIG')
        assert isinstance(settings.STORAGE_CONFIG, dict)
        print("✓ settings.py contiene STORAGE_CONFIG")

    def test_storage_config_has_required_keys(self):
        """Verifica que STORAGE_CONFIG tiene las claves requeridas."""
        required_keys = ["output_folder", "filename", "naming_mode"]
        for key in required_keys:
            assert key in settings.STORAGE_CONFIG, f"Falta '{key}' en STORAGE_CONFIG"
        print("✓ STORAGE_CONFIG tiene todas las claves requeridas")

    def test_storage_config_naming_mode_is_valid(self):
        """Verifica que naming_mode es válido."""
        valid_modes = ["overwrite", "date_suffix", "timestamp_suffix", "date_folder"]
        mode = settings.STORAGE_CONFIG["naming_mode"]
        assert mode in valid_modes, f"Modo inválido: {mode}. Debe ser uno de {valid_modes}"
        print(f"✓ Modo de nombrado válido: {mode}")

    def test_storage_config_output_folder_exists(self):
        """Verifica que la carpeta de salida existe."""
        folder = settings.STORAGE_CONFIG["output_folder"]
        assert os.path.isdir(folder), f"Carpeta de salida no existe: {folder}"
        print(f"✓ Carpeta de salida existe: {folder}")


class TestDriverConfig:
    """Tests para verificar que el driver se inicializa correctamente con settings.py"""

    def test_settings_file_has_driver_config(self):
        """Verifica que settings.py tiene la configuración DRIVER_CONFIG."""
        assert hasattr(settings, 'DRIVER_CONFIG')
        assert isinstance(settings.DRIVER_CONFIG, dict)
        print("✓ settings.py contiene DRIVER_CONFIG")

    def test_driver_instance_created_with_settings_file(self):
        """
        TEST PRINCIPAL: Verifica que se puede crear una instancia del driver
        con la configuración exacta de settings.py
        """
        # Modificar temporalmente para modo headless (más rápido en tests)
        test_config = settings.DRIVER_CONFIG.copy()
        test_config['headless'] = True

        driver_config = DriverConfig(**test_config)
        driver = driver_config.get_driver()

        try:
            assert driver is not None
            print("✓ Driver inicializado correctamente con configuración de settings.py")
        finally:
            driver.quit()


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
