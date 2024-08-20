from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User


class Task(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    description = models.TextField(verbose_name=_('Description'))
    # Translators: Task performer
    performer = models.ForeignKey(to=User,
                                  on_delete=models.SET_NULL,
                                  blank=True,
                                  null=True,
                                  verbose_name=_('Performer'),
                                  related_name='assiged_tasks')
    status = models.ForeignKey(to='statuses.Status',
                               on_delete=models.PROTECT,
                               verbose_name=_('Status'))
    author = models.ForeignKey(to=User,
                               on_delete=models.PROTECT,
                               verbose_name=_('Author'),
                               related_name='created_tasks')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Creation time'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Last update time'))

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = _('task')
        verbose_name_plural = _('tasks')
