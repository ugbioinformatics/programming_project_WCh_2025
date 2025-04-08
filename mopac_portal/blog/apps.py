from django.apps import AppConfig

#tworzy nazwe naszej aplikacji

class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'

    def ready(self):
        from . import signals
