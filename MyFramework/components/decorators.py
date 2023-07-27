class AppRoute:
    def __init__(self, routes: dict, url: str):
        """
        :param routes: Словарь привязок
        :param url: наш url
        """
        self.routes = routes
        self.url = url

    def __call__(self, cls):
        """cls - ссылка на декорируемый класс"""
        self.routes[self.url] = cls()