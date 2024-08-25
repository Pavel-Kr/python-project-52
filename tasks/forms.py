from django import forms
from django.utils.translation import gettext_lazy as _

from tasks.models import Task
from users.models import User


class UserChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj: User) -> str:
        return obj.get_full_name()


class TaskForm(forms.ModelForm):
    executor = UserChoiceField(queryset=User.objects.all(), label=_('Executor'))

    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'labels']
