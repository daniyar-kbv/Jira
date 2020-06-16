from django.apps import AppConfig


class AutheConfig(AppConfig):
    name = 'authe'

    def ready(self):
        import authe.signals