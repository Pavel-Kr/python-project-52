from django import forms

from tasks.models import Task


class TaskCreationForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'performer']
