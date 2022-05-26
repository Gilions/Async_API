from django.db import models
from django.utils.translation import gettext_lazy as _


class EtlServices(models.Model):
    process = models.CharField(_('process'), max_length=125, unique=True)
    start = models.DateTimeField(auto_now=False, auto_now_add=False)

    class Meta:
        db_table = "external\".\"etl_services"
        verbose_name = _('EtlService')
        verbose_name_plural = _('EtlServices')
