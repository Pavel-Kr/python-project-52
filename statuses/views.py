from django.http.response import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils.translation import gettext as _

from .forms import StatusForm
from .models import Status


class StatusListView(LoginRequiredMixin, ListView):
    model = Status
    template_name = 'statuses/index.html'
    context_object_name = 'statuses'

    def handle_no_permission(self) -> HttpResponseRedirect:
        messages.error(self.request, _('You are not logged in'))
        return super().handle_no_permission()


class StatusCreateView(LoginRequiredMixin, CreateView):
    model = Status
    template_name = 'statuses/create.html'
    form_class = StatusForm
    success_url = reverse_lazy('statuses:index')

    def handle_no_permission(self) -> HttpResponseRedirect:
        messages.error(self.request, _('You are not logged in'))
        return super().handle_no_permission()
