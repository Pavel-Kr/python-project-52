from django.contrib.auth.forms import UserCreationForm, BaseUserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']


class EditForm(BaseUserCreationForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']
