from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AgentsConfig(AppConfig):
    name = "radical_translations.agents"
    verbose_name = _("Agents")
