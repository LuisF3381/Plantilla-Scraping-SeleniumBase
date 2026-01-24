import pytest
import os
import re
from urllib.parse import urlparse
from driver_config import DriverConfig
from main import load_web_config
import config


class TestWebConfig:
    """Tests para validar el archivo web_config.yaml"""

    def test_web_config_file_exists(self):
        """Verifica que existe el archivo web_config.yaml."""
        assert os.path.exists("web_config.yaml"), "No existe web_config.yaml"
        print("✓ web_config.yaml existe")

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


class TestDriverConfig:
    """Tests para verificar que el driver se inicializa correctamente con config.py"""

    def test_config_file_has_driver_config(self):
        """Verifica que config.py tiene la configuración DRIVER_CONFIG."""
        assert hasattr(config, 'DRIVER_CONFIG')
        assert isinstance(config.DRIVER_CONFIG, dict)
        print("✓ config.py contiene DRIVER_CONFIG")

    def test_driver_instance_created_with_config_file(self):
        """
        TEST PRINCIPAL: Verifica que se puede crear una instancia del driver
        con la configuración exacta de config.py
        """
        # Modificar temporalmente para modo headless (más rápido en tests)
        test_config = config.DRIVER_CONFIG.copy()
        test_config['headless'] = True

        driver_config = DriverConfig(**test_config)
        driver = driver_config.get_driver()

        try:
            assert driver is not None
            print("✓ Driver inicializado correctamente con configuración de config.py")
        finally:
            driver.quit()


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
