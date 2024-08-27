from django.db import models
from django.utils.translation import gettext_lazy as _

from task_manager.labels.models import Label
from task_manager.users.models import User


class Task(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Name'), unique=True)
    description = models.TextField(verbose_name=_('Description'))
    # Translators: Task executor
    executor = models.ForeignKey(to=User,
                                 on_delete=models.SET_NULL,
                                 blank=True,
                                 null=True,
                                 verbose_name=_('Executor'),
                                 related_name='assiged_tasks')
    status = models.ForeignKey(to='statuses.Status',
                               on_delete=models.PROTECT,
                               verbose_name=_('Status'))
    author = models.ForeignKey(to=User,
                               on_delete=models.PROTECT,
                               verbose_name=_('Author'),
                               related_name='created_tasks')
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_('Creation time'))
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name=_('Last update time'))
    labels = models.ManyToManyField(
        to=Label,
        through='LabelTaskConnection',
        blank=True,
        verbose_name=_('Labels')
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = _('task')
        verbose_name_plural = _('tasks')
        ordering = ['id']


class LabelTaskConnection(models.Model):
    label = models.ForeignKey(to=Label, on_delete=models.PROTECT)
    task = models.ForeignKey(to=Task, on_delete=models.CASCADE)
