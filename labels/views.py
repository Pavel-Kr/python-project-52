from django.http.response import HttpResponseRedirect
from django.views.generic import CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy

from labels.models import Label
from labels.forms import LabelForm


class LabelListView(LoginRequiredMixin, ListView):
    model = Label
    template_name = 'labels/index.html'
    context_object_name = 'labels'

    def handle_no_permission(self) -> HttpResponseRedirect:
        messages.error(self.request, _('You are not logged in'))
        return super().handle_no_permission()


class LabelCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Label
    template_name = 'labels/create.html'
    form_class = LabelForm
    success_message = _('Label successfully created')
    success_url = reverse_lazy('labels:index')

    def handle_no_permission(self) -> HttpResponseRedirect:
        messages.error(self.request, _('You are not logged in'))
        return super().handle_no_permission()
