from django.db import models
from django.utils.translation import gettext_lazy as _


class Label(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Name'), unique=True)
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Creation time')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Last update time')
    )

    class Meta:
        ordering = ['pk']

    def __str__(self) -> str:
        return self.name
