from django.apps import AppConfig
from django.db.models.signals import post_migrate


class BrokensiteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'brokensite'

    def ready(self):
        from .signals import create_required_objects
        post_migrate.connect(create_required_objects, sender=self)

