from django.apps import AppConfig

class EngageConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'engage'

    def ready(self):
        import engage.signals  # 👈 Подключаем signals при старте
