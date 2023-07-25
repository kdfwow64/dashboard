from django.apps import AppConfig


class DaepV2Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'daep_v2'

    def ready(self):
        import daep_v2.dashboards
