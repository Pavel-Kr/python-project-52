from typing import Any
from django.db.models.query import QuerySet
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from tasks.models import Task


class TaskListView(LoginRequiredMixin, ListView):
    template_name = 'tasks/index.html'
    context_object_name = 'tasks'

    def get_queryset(self) -> QuerySet[Any]:
        return Task.objects.select_related(
            'author'
        ).select_related(
            'performer'
        ).select_related(
            'status'
        )
