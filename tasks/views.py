from typing import Any
from django.db.models.query import QuerySet
from django.views.generic import CreateView, DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from tasks.models import Task
from tasks.forms import TaskCreationForm


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


class TaskDetailView(LoginRequiredMixin, DetailView):
    template_name = 'tasks/show.html'
    model = Task
    context_object_name = 'task'

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().select_related(
            'author'
        ).select_related(
            'performer'
        ).select_related(
            'status'
        )


class TaskCreateView(LoginRequiredMixin, CreateView):
    template_name = 'tasks/create.html'
    form_class = TaskCreationForm
    success_url = reverse_lazy('tasks:index')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
