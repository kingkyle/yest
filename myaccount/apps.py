from django.apps import AppConfig


class MyaccountConfig(AppConfig):
    name = 'myaccount'

    def ready(self):
        import myaccount.signals
