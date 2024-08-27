from django.db.models import ProtectedError
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy

from .models import Label
from .forms import LabelForm
from task_manager.mixins import LoginRequiredMessageMixin


class LabelListView(LoginRequiredMessageMixin, ListView):
    model = Label
    template_name = 'labels/index.html'
    context_object_name = 'labels'


class LabelCreateView(LoginRequiredMessageMixin,
                      SuccessMessageMixin,
                      CreateView):
    model = Label
    template_name = 'labels/create.html'
    form_class = LabelForm
    success_message = _('Label successfully created')
    success_url = reverse_lazy('labels:index')


class LabelUpdateView(LoginRequiredMessageMixin,
                      SuccessMessageMixin,
                      UpdateView):
    model = Label
    template_name = 'labels/update.html'
    form_class = LabelForm
    success_message = _('Label successfully updated')
    success_url = reverse_lazy('labels:index')
    context_object_name = 'label'


class LabelDeleteView(LoginRequiredMessageMixin,
                      SuccessMessageMixin,
                      DeleteView):
    model = Label
    template_name = 'labels/delete.html'
    success_message = _('Label succsessfully deleted')
    success_url = reverse_lazy('labels:index')
    context_object_name = 'label'

    def post(self, request: HttpRequest, *args: str, **kwargs) -> HttpResponse:
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(
                self.request,
                _('Cannot delete label because it is used')
            )
            return redirect('labels:index')
