import django_filters
from django import forms
from django.utils.translation import gettext_lazy as _

from tasks.models import Task
from labels.models import Label


class TaskFilter(django_filters.FilterSet):
    labels = django_filters.ModelChoiceFilter(
        queryset=Label.objects.all(),
        label=_('Label')
    )
    self_tasks = django_filters.BooleanFilter(
        method='filter_user',
        widget=forms.CheckboxInput,
        label=_('My tasks only')
    )

    def filter_user(self, queryset, name, value):
        if value:
            user = getattr(self.request, 'user', None)
            queryset = queryset.filter(author=user)
        return queryset

    class Meta:
        model = Task
        fields = ['status', 'executor']
