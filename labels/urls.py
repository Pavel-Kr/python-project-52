from django.urls import path

from labels import views


app_name = 'labels'
urlpatterns = [
    path('', views.LabelListView.as_view(), name='index'),
]
