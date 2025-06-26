from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from task_manager.forms import CustomLoginForm


class CustomLoginView(SuccessMessageMixin, LoginView):
    """Custom login view with success message."""
    template_name = 'login_form.html'
    form_class = CustomLoginForm
    next_page = 'index'
    success_message = _('You were logged in')


class CustomLogoutView(SuccessMessageMixin, LogoutView):
    """Custom logout view with info message."""
    next_page = 'index'

    def dispatch(self, request, *args, **kwargs):
        """Adds an info message when user logs out."""
        messages.info(request, _('You were logged out'))
        return super().dispatch(request, *args, **kwargs)
