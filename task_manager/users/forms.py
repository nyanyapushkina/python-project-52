from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

from task_manager.mixins import FormStyleMixin
from task_manager.users.models import User

MIN_PASSWORD_LENGTH = 3


class BaseUserForm:
    """Basic config for user forms."""
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username')
        help_texts = {
            'username': _(
                'Required. 150 characters or fewer. '
                'Letters, digits and @/./+/-/_ only.'
            ),
        }


class UserFormPasswordMixin:
    """Mixin for custom password validation logic."""
    def custom_validate_passwords(self, cleaned_data):
        """Validate password length and equality."""
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2:
            if password1 != password2:
                self.add_error(
                    "password2",
                    _("Passwords don't match.")
                )
            elif len(password1) < MIN_PASSWORD_LENGTH:
                self.add_error(
                    "password2",
                    _(
                        "This password is too short. "
                        f"It must contain at least "
                        f"{MIN_PASSWORD_LENGTH} characters."
                    ),
                )
        return cleaned_data


class CustomUserCreationForm(FormStyleMixin, 
                             UserCreationForm, 
                             UserFormPasswordMixin):
    """User registration form with custom validation and styling."""
    class Meta(BaseUserForm.Meta):
        fields = (*BaseUserForm.Meta.fields, 'password1', 'password2')
        help_texts = {
            **BaseUserForm.Meta.help_texts,
            'password1': _(
                f"Your password must contain at least "
                f"{MIN_PASSWORD_LENGTH} characters."
            ),
            'password2': _('Please enter your password again to confirm.'),
        }

    def clean(self):
        """Validate password length and equality."""
        cleaned_data = super().clean()
        return self.custom_validate_passwords(cleaned_data)


class CustomUserChangeForm(FormStyleMixin, 
                           forms.ModelForm, 
                           UserFormPasswordMixin):
    """User profile edit form with password update support."""
    password1 = forms.CharField(
        label=_("New Password"),
        widget=forms.PasswordInput,
        required=True,
        help_text=_(
            f"Your password must contain at least "
            f"{MIN_PASSWORD_LENGTH} characters."
        ),
    )
    password2 = forms.CharField(
        label=_("Confirm Password"),
        widget=forms.PasswordInput,
        required=True,
        help_text=_("Please enter your password again to confirm."),
    )

    class Meta(BaseUserForm.Meta):
        fields = (*BaseUserForm.Meta.fields, 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'password' in self.fields:
            del self.fields['password']

    def clean(self):
        """Validate password length and equality."""
        cleaned_data = super().clean()
        return self.custom_validate_passwords(cleaned_data)

    def save(self, commit=True):
        """Save updated user with new password if provided."""
        user = super().save(commit=False)
        if password1 := self.cleaned_data.get("password1"):
            user.set_password(password1)
        if commit:
            user.save()
        return user
