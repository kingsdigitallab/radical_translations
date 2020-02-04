from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class EventsConfig(AppConfig):
    name = "radical_translations.events"
    verbose_name = _("Events")
