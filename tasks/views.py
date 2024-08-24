from typing import Any
from django.core.exceptions import PermissionDenied
from django.db.models.query import QuerySet
from django.http.response import HttpResponseRedirect
from django.views.generic import (CreateView,
                                  DeleteView,
                                  DetailView,
                                  UpdateView)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.shortcuts import redirect
from django_filters.views import FilterView

from tasks.models import Task
from tasks.forms import TaskForm
from tasks.filters import TaskFilter


class TaskListView(LoginRequiredMixin, FilterView):
    template_name = 'tasks/index.html'
    context_object_name = 'tasks'
    filterset_class = TaskFilter

    def get_queryset(self) -> QuerySet[Any]:
        dummy()
        return Task.objects.select_related(
            'author'
        ).select_related(
            'performer'
        ).select_related(
            'status'
        )

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['self_tasks'] = self.request.GET.get('self_tasks', None)
        return context

    def handle_no_permission(self) -> HttpResponseRedirect:
        messages.error(self.request, _('You are not logged in'))
        return super().handle_no_permission()


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

    def handle_no_permission(self) -> HttpResponseRedirect:
        messages.error(self.request, _('You are not logged in'))
        return super().handle_no_permission()


class TaskCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'tasks/create.html'
    form_class = TaskForm
    success_url = reverse_lazy('tasks:index')
    success_message = _('Task successfully created')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def handle_no_permission(self) -> HttpResponseRedirect:
        messages.error(self.request, _('You are not logged in'))
        return super().handle_no_permission()


class TaskUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'tasks/update.html'
    form_class = TaskForm
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks:index')
    success_message = _('Task successfully updated')

    def handle_no_permission(self) -> HttpResponseRedirect:
        messages.error(self.request, _('You are not logged in'))
        return super().handle_no_permission()


class TaskDeleteView(LoginRequiredMixin,
                     UserPassesTestMixin,
                     SuccessMessageMixin,
                     DeleteView):
    template_name = 'tasks/delete.html'
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks:index')
    success_message = _('Task successfully deleted')
    permission_denied_message = _("Only author can delete his task")

    def test_func(self) -> bool | None:
        task = self.get_object()
        return task.author.pk == self.request.user.pk

    def handle_no_permission(self) -> HttpResponseRedirect:
        try:
            if not self.request.user.is_authenticated:
                messages.error(self.request, _('You are not logged in'))
            return super().handle_no_permission()
        except PermissionDenied:
            messages.error(self.request, self.permission_denied_message)
            return redirect('tasks:index')
