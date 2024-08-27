from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponseRedirect
from django.contrib import messages
from django.utils.translation import gettext_lazy as _


class LoginRequiredMessageMixin(LoginRequiredMixin):
    login_required_message = _('You are not logged in')

    def handle_no_permission(self) -> HttpResponseRedirect:
        messages.error(self.request, self.login_required_message)
        return super().handle_no_permission()
