from django.apps import AppConfig


class AkashicrecordsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'akashicrecords'

    def ready(self):
      import akashicrecords.signals