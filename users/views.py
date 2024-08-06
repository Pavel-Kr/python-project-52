from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.utils.translation import gettext_lazy as _

from users.forms import RegisterForm


class UserListView(ListView):
    model = User
    paginate_by = 20
    template_name = 'users/index.html'
    context_object_name = 'users'


class UserCreateView(SuccessMessageMixin, CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'users/create.html'
    success_url = reverse_lazy('users:login')
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
