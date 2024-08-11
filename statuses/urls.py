from django.urls import path

from statuses import views


app_name = 'statuses'
urlpatterns = [
    path('', views.StatusListView.as_view(), name='index'),
]
