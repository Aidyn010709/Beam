from django.db import models
from django.utils.translation import gettext_lazy as _

class DisabledAPI(models.Model):
    disable = models.BooleanField(default=False, verbose_name=_("Отключить API"))

    def __str__(self):
        return f"{self.disable}"

    class Meta:
        verbose_name = "Временное отключение API"
        verbose_name_plural = "Временное отключение API"