from django.apps import AppConfig


class NewsPublishingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news_publishing'

    def ready(self):
        import news_publishing.signals
