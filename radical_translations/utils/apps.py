from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UtilsConfig(AppConfig):
    name = "radical_translations.utils"
    verbose_name = _("Utils")
