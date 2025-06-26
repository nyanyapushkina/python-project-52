from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models.deletion import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


class FormStyleMixin:
    """Adds Bootstrap styles to form fields."""
    # Base CSS classes
    BASE_INPUT_CLASS = (
        'form-control bg-secondary bg-opacity-50 border-secondary'
        )
    BASE_SELECT_CLASS = (
        'form-select bg-secondary bg-opacity-50 border-secondary'
        )
    
    # Field-specific configurations
    FIELD_CONFIGS = {
        'description': {
            'class': BASE_INPUT_CLASS,
            'rows': '3'
        },
        'status': {
            'class': BASE_SELECT_CLASS
        },
        'executor': {
            'class': BASE_SELECT_CLASS
        }
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._apply_field_styles()

    def _apply_field_styles(self):
        """Applies configured styles to all form fields."""
        for field_name, field in self.fields.items():
            attrs = {
                'placeholder': field.label,
                **self.FIELD_CONFIGS.get(field_name, 
                                         {'class': self.BASE_INPUT_CLASS})
            }
            field.widget.attrs.update(attrs)


class BasePermissionMixin(UserPassesTestMixin):
    """
    Base mixin for permission checks with customizable messages and redirects.
    """
    permission_denied_url = reverse_lazy('users:index')
    permission_denied_message = _('Permission denied')
    redirect_field_name = None

    def handle_no_permission(self):
        """
        Handles permission denial with appropriate redirect and messaging.
        For authenticated users: shows error and redirects to denied_url
        For anonymous users: falls back to default login redirect
        """
        if self.request.user.is_authenticated:
            messages.error(self.request, self.permission_denied_message)
            return redirect(self.permission_denied_url)
        return super().handle_no_permission()


class CustomLoginRequiredMixin(LoginRequiredMixin):
    """
    Enhanced login required mixin with custom messaging.
    Overrides default behavior to not use 'next' parameter.
    """
    login_url = reverse_lazy('login')
    redirect_field_name = None
    not_authenticated_message = _('You are not authorized! Please, log in.')

    def handle_no_permission(self):
        """Adds error message for unauthenticated users before redirect."""
        if not self.request.user.is_authenticated:
            messages.error(self.request, self.not_authenticated_message)
        return super().handle_no_permission()


class UserPermissionMixin(BasePermissionMixin):
    """Restricts access to the profile owner only."""
    permission_denied_message = _('You do not have permission '
    'to change another user.')

    def test_func(self):
        """Determines if the requesting user matches the object's user."""
        return self.get_object() == self.request.user


class AuthorPermissionMixin(BasePermissionMixin):
    """Restricts access to the object's author only."""
    permission_denied_message = _('You do not have permission '
    'to change this object.')

    def test_func(self):
        """Determines if the requesting user is the object's author."""
        return self.get_object().author == self.request.user


class ProtectErrorMixin:
    """
    Provides protected object deletion handling.
    Should be mixed in with DeleteView or similar.
    """
    protected_object_message = _('Cannot delete object '
    'because it is being used.')
    protected_object_url = None

    def post(self, request, *args, **kwargs):
        """
        Attempts deletion and handles ProtectedError gracefully.
        Returns appropriate redirect with error message on failure.
        """
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, self.protected_object_message)
            return redirect(self.protected_object_url)
