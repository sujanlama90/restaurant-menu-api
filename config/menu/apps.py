from django.apps import AppConfig


class MenuConfig(AppConfig):
    name = 'menu'

    def ready(self):
        from .signal import invalid_cach_categories
