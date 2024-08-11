from django.http.response import HttpResponseRedirect
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils.translation import gettext as _

from .models import Status


class StatusListView(LoginRequiredMixin, ListView):
    model = Status
    template_name = 'statuses/index.html'
    context_object_name = 'statuses'

    def handle_no_permission(self) -> HttpResponseRedirect:
        messages.error(self.request, _('You are not logged in'))
        return super().handle_no_permission()
