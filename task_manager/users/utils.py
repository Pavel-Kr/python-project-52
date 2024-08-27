from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _


class SameUserMixin:
    """Checks that user can trigger dangerous actions,
       such as update and delete only for himself."""

    error_message = _('You do not have permission')
    error_url = '/'

    def dispatch(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk != request.user.pk:
            messages.error(request, self.error_message)
            return redirect(self.error_url)
        return super().dispatch(request, *args, **kwargs)
