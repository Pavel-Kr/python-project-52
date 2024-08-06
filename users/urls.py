from django.urls import path

from users import views


app_name = 'users'
urlpatterns = [
    path('', views.UserListView.as_view(), name='index'),
    path('create/', views.UserCreateView.as_view(), name='create'),
    path('login/', views.UserLoginView.as_view(), name='login')
]
