import pytest
from driver_config import DriverConfig
import config


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
