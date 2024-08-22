from django.contrib import admin

from tasks.models import Task, LabelTaskConnection


class LTCInline(admin.TabularInline):
    model = LabelTaskConnection


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    fields = ['name', 'description']
    inlines = (LTCInline,)
