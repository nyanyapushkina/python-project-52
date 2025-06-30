from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView,
    UpdateView,
)

from task_manager.mixins import (
    CustomLoginRequiredMixin,
    ProtectErrorMixin,
    UserPermissionMixin,
)
from task_manager.users.forms import (
    CustomUserChangeForm,
    CustomUserCreationForm,
)
from task_manager.users.models import User

USERS_INDEX_URL = reverse_lazy('users:index')
LOGIN_URL = reverse_lazy('login')
PERMISSION_DENIED_MESSAGE = _("You don't have rights to change another user.")


class UserListView(ListView):
    model = User
    template_name = 'users/index.html'
    context_object_name = 'users'
    ordering = ['id']


class BaseUserView(SuccessMessageMixin):
    """Base class for user views."""
    model = User
    template_name = 'users/form.html'
    context_object_name = 'user'
    permission_denied_url = USERS_INDEX_URL


class UserCreateView(BaseUserView, CreateView):
    class Constants:
        SUCCESS_MESSAGE = _('User was registered successfully')
        TITLE = _('Sign Up')
        BUTTON_NAME = _('Register')

    form_class = CustomUserCreationForm
    success_url = LOGIN_URL
    success_message = Constants.SUCCESS_MESSAGE
    extra_context = {
        'title': Constants.TITLE,
        'button_name': Constants.BUTTON_NAME
    }


class UserUpdateView(CustomLoginRequiredMixin, UserPermissionMixin,
                    BaseUserView, UpdateView):
    form_class = CustomUserChangeForm
    success_url = USERS_INDEX_URL
    success_message = _('User was updated successfully')
    permission_denied_message = PERMISSION_DENIED_MESSAGE
    extra_context = {
        'title': _('Edit profile'),
        'button_name': _('Save changes')
    }


class UserDeleteView(CustomLoginRequiredMixin, UserPermissionMixin,
                    ProtectErrorMixin, BaseUserView, DeleteView):
    template_name = 'users/delete.html'
    success_url = USERS_INDEX_URL
    success_message = _('User was deleted successfully')
    permission_denied_message = PERMISSION_DENIED_MESSAGE
    access_denied_message = PERMISSION_DENIED_MESSAGE
    protected_object_url = USERS_INDEX_URL
    protected_object_message = _('Cannot delete this user '
        'because they are being used')
    extra_context = {
        'title': _('User deletion'),
        'button_name': _('Yes, delete')
    }
