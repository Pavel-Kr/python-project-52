from typing import Any
from django.db.models.query import QuerySet
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from tasks.models import Task
from tasks.forms import TaskForm


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


class TaskCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'tasks/create.html'
    form_class = TaskForm
    success_url = reverse_lazy('tasks:index')
    success_message = _('Task successfully created')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'tasks/update.html'
    form_class = TaskForm
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks:index')
    success_message = _('Task successfully updated')
