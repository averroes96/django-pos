from django.apps import AppConfig


class BuysConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'buys'

    def ready(self) -> None:
        import buys.signals