from django.apps import AppConfig


class ExampleConfig(AppConfig):
    name = 'wd'

    def ready(self):
        import example.signals