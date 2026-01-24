from seleniumbase import Driver


class DriverConfig:
    """Configuración para inicializar el driver de SeleniumBase con opciones personalizables."""

    def __init__(
        self,
        headless=False,
        undetected=True,
        maximize=True,
        window_size=None,
        user_agent=None,
        proxy=None
    ):
        """
        Inicializa la configuración del driver.

        Args:
            headless (bool): Ejecutar en modo sin interfaz gráfica. Default: False
            undetected (bool): Activar undetected-chromedriver para evadir detección. Default: True
            maximize (bool): Maximizar la ventana del navegador. Default: True
            window_size (tuple): Tupla (ancho, alto) para establecer tamaño específico. Default: None
            user_agent (str): User agent personalizado. Default: None
            proxy (str): Servidor proxy en formato "ip:puerto". Default: None
        """
        self.headless = headless
        self.undetected = undetected
        self.maximize = maximize
        self.window_size = window_size
        self.user_agent = user_agent
        self.proxy = proxy

    def get_driver(self):
        """
        Crea y retorna un driver de SeleniumBase configurado con las opciones especificadas.

        Returns:
            Driver: Instancia del driver de SeleniumBase configurada.
        """
        # Construir argumentos para el driver
        driver_kwargs = {
            'uc': self.undetected,
            'headless': self.headless
        }

        # Agregar user agent si está especificado
        if self.user_agent:
            driver_kwargs['user_agent'] = self.user_agent

        # Agregar proxy si está especificado
        if self.proxy:
            driver_kwargs['proxy'] = self.proxy

        # Inicializar el driver con las opciones configuradas
        driver = Driver(**driver_kwargs)

        # Configurar tamaño de ventana
        if self.window_size:
            # Si se especifica un tamaño personalizado
            width, height = self.window_size
            driver.set_window_size(width, height)
        elif self.maximize:
            # Si no hay tamaño personalizado y maximize=True
            driver.maximize_window()

        return driver
