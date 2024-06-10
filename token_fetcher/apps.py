from django.apps import AppConfig
from django.contrib.auth.apps import AuthConfig


class TokenFetcherConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'token_fetcher'

    def ready(self):
        from .cron import UpdateTokenData
        AuthConfig.init_user_model('token_fetcher.UserProfile')
        from django_cron import CronJobBase
        CronJobBase.register(UpdateTokenData)