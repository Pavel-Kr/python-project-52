from django.contrib.auth.models import User
from django.views.generic import ListView


class UserListView(ListView):
    model = User
    paginate_by = 20
    template_name = 'users/index.html'
    context_object_name = 'users'
