from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

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


class UserURLs:
    """Container for user-related URLs to avoid string duplication."""
    INDEX = reverse_lazy('users:index')
    LOGIN = reverse_lazy('login')


class UserMessages:
    """Container for user-related messages to avoid string duplication."""
    PERMISSION_DENIED = _("You don't have rights to change another user.")
    REGISTER_SUCCESS = _('User was registered successfully')
    UPDATE_SUCCESS = _('User was updated successfully')
    DELETE_SUCCESS = _('User was deleted successfully')
    PROTECTED_USER = _('Cannot delete this user because they are being used')


class UserViewTexts:
    """Container for user-related UI texts."""
    USERS_TITLE = _('Users')
    SIGNUP_TITLE = _('Sign Up')
    SIGNUP_BUTTON = _('Register')
    EDIT_TITLE = _('Edit profile')
    EDIT_BUTTON = _('Save changes')
    DELETE_TITLE = _('User deletion')
    DELETE_BUTTON = _('Yes, delete')


class UserListView(ListView):
    """Display list of all users with ordering by ID."""
    model = User
    template_name = 'users/index.html'
    context_object_name = 'users'
    ordering = ['id']


class BaseUserView(SuccessMessageMixin):
    """
    Base configuration for user-related views.
    Provides common settings for create/update/delete views.
    """
    model = User
    template_name = 'users/registration_form.html'
    context_object_name = 'user'
    permission_denied_url = UserURLs.INDEX


class UserCreateView(BaseUserView, CreateView):
    """Handle new user registration."""
    form_class = CustomUserCreationForm
    success_url = UserURLs.LOGIN
    success_message = UserMessages.REGISTER_SUCCESS

    def get_page_title(self):
        return UserViewTexts.SIGNUP_TITLE

    def get_button_text(self):
        return UserViewTexts.SIGNUP_BUTTON


class UserUpdateView(CustomLoginRequiredMixin, UserPermissionMixin, 
                     BaseUserView, UpdateView):
    """Handle user profile updates."""
    form_class = CustomUserChangeForm
    success_url = UserURLs.INDEX
    success_message = UserMessages.UPDATE_SUCCESS
    permission_denied_message = UserMessages.PERMISSION_DENIED

    def get_page_title(self):
        return UserViewTexts.EDIT_TITLE

    def get_button_text(self):
        return UserViewTexts.EDIT_BUTTON


class UserDeleteView(CustomLoginRequiredMixin, UserPermissionMixin, 
                     ProtectErrorMixin, BaseUserView, DeleteView):
    """Handle user account deletion."""
    template_name = 'users/delete.html'
    success_url = UserURLs.INDEX
    success_message = UserMessages.DELETE_SUCCESS
    permission_denied_message = UserMessages.PERMISSION_DENIED
    protected_object_url = UserURLs.INDEX
    protected_object_message = UserMessages.PROTECTED_USER

    def get_page_title(self):
        return UserViewTexts.DELETE_TITLE

    def get_button_text(self):
        return UserViewTexts.DELETE_BUTTON

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = self.get_object()
        return context
