from django.db import models
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext as _

from .forms import StatusForm
from .models import Status
from task_manager.mixins import LoginRequiredMessageMixin


class StatusListView(LoginRequiredMessageMixin, ListView):
    model = Status
    template_name = 'statuses/index.html'
    context_object_name = 'statuses'


class StatusCreateView(LoginRequiredMessageMixin,
                       SuccessMessageMixin,
                       CreateView):
    model = Status
    template_name = 'statuses/create.html'
    form_class = StatusForm
    success_url = reverse_lazy('statuses:index')
    success_message = _('Status successfully created')


class StatusUpdateView(LoginRequiredMessageMixin,
                       SuccessMessageMixin,
                       UpdateView):
    model = Status
    template_name = 'statuses/update.html'
    form_class = StatusForm
    success_url = reverse_lazy('statuses:index')
    context_object_name = 'status'
    success_message = _('Status successfully updated')


class StatusDeleteView(LoginRequiredMessageMixin,
                       SuccessMessageMixin,
                       DeleteView):
    model = Status
    template_name = 'statuses/delete.html'
    success_url = reverse_lazy('statuses:index')
    context_object_name = 'status'
    success_message = _('Status successfully deleted')

    def post(self, request: HttpRequest, *args: str, **kwargs) -> HttpResponse:
        try:
            return super().post(request, *args, **kwargs)
        except models.ProtectedError:
            messages.error(request,
                           _('Cannot delete status because it is in use'))
            return redirect('statuses:index')
