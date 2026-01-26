from django.apps import AppConfig


class WorksheetsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.worksheets'
    verbose_name = 'Рабочие листы'

    def ready(self):
        # Импортируем сигналы
        import apps.worksheets.signals
