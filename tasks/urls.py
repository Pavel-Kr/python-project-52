from django.urls import path

from tasks import views


app_name = 'tasks'
urlpatterns = [
    path('', views.TaskListView.as_view(), name='index'),
]
