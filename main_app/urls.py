from django.urls import path

from main_app import views


app_name = 'main'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index')
]
