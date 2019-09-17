from django.apps import AppConfig


class UsersAppConfig(AppConfig):

    name = "sdap.users"
    verbose_name = _("Users")

    def ready(self):
        try:
            import sdap.users.signals  # noqa F401
        except ImportError:
            pass
