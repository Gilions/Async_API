from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ExternalServicesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'external_services'
    verbose_name = _('external_services')
