from django.apps import AppConfig


class InventoryConfig(AppConfig):
    name = 'inventory'

    def ready(self):
        # Ensure division users exist after migrations in deployed environments.
        print('inventory.AppConfig.ready(): loading inventory signals')
        from . import signals  # noqa: F401
