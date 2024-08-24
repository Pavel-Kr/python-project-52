from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from django.http import HttpRequest, HttpResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.utils.translation import gettext_lazy as _

from users.forms import RegisterForm, EditForm
from users.utils import SameUserMixin


class UserListView(ListView):
    model = User
    template_name = 'users/index.html'
    context_object_name = 'users'


class UserCreateView(SuccessMessageMixin, CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'users/create.html'
    success_url = reverse_lazy('login')
    success_message = _('User successfully registered')


class UserLoginView(SuccessMessageMixin, LoginView):
    model = User
    template_name = 'users/login.html'
    success_message = _('You logged in')


class UserLogoutView(LogoutView):
    success_message = _('You logged out')

    def post(self, request, *args, **kwargs):
        messages.success(request, self.success_message)
        return super().post(request, args, kwargs)


class UserUpdateView(LoginRequiredMixin,
                     SameUserMixin,
                     SuccessMessageMixin,
                     UpdateView):
    model = User
    template_name = 'users/update.html'
    form_class = EditForm
    success_url = reverse_lazy('users:index')
    success_message = _('User successfully updated')
    error_url = reverse_lazy('users:index')
    error_message = _('You do not have permission to edit other users!')

    def handle_no_permission(self) -> HttpResponseRedirect:
        messages.error(self.request, _('You are not logged in'))
        return super().handle_no_permission()


class UserDeleteView(LoginRequiredMixin,
                     SameUserMixin,
                     SuccessMessageMixin,
                     DeleteView):
    template_name = 'users/delete_confirm.html'
    model = User
    success_url = reverse_lazy('users:index')
    success_message = _('User successfully deleted')
    template_name_field = 'user'
    error_url = reverse_lazy('users:index')
    error_message = _('You do not have permission to delete other users!')

    def handle_no_permission(self) -> HttpResponseRedirect:
        messages.error(self.request, _('You are not logged in'))
        return super().handle_no_permission()

    def post(self, request: HttpRequest, *args: str, **kwargs) -> HttpResponse:
        try:
            return super().post(request, *args, **kwargs)
        except models.ProtectedError:
            messages.error(request,
                           _('Cannot delete user because it is in use'))
            return redirect('users:index')
