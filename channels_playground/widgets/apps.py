from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class WidgetsConfig(AppConfig):
    name = 'channels_playground.widgets'
    verbose_name = _("Widgets")

    def ready(self):
        try:
            import channels_playground.widgets.signals  # noqa F401
        except ImportError:
            pass
