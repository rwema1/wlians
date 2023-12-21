from django.apps import AppConfig


class MyappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    default_app_config = 'myapp.apps.MyAppConfig'
    name = 'myapp'
