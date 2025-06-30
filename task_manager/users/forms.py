from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

from task_manager.mixins import FormStyleMixin
from task_manager.users.models import User

MIN_PASSWORD_LENGTH = 3


class BaseUserForm:
    """Base configuration for user forms."""
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username')
        help_texts = {
            'username': _(
                'Required. 150 characters or fewer. '
                'Letters, digits and @/./+/-/_ only.'
            ),
        }


class CustomUserCreationForm(FormStyleMixin, UserCreationForm):
    """User registration form with enhanced validation."""
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
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2:
            if password1 != password2:
                self.add_error("password2", _("Passwords don't match."))
            elif len(password1) < MIN_PASSWORD_LENGTH:
                self.add_error(
                    "password2",
                    _("Password must contain " 
                    "at least %(min_length)d characters.") % {
                        'min_length': MIN_PASSWORD_LENGTH
                    }
                )
        return cleaned_data


class CustomUserChangeForm(FormStyleMixin, forms.ModelForm):
    """User edit form with password change support."""
    password1 = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput,
        required=False,
        help_text=_(
            f"Leave blank if you don't want to change it. "
            f"Minimum {MIN_PASSWORD_LENGTH} characters."
        ),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput,
        required=False,
        help_text=_("Enter the same password for verification."),
    )

    class Meta(BaseUserForm.Meta):
        fields = (*BaseUserForm.Meta.fields,)

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 or password2:
            if password1 != password2:
                self.add_error("password2", _("Passwords don't match."))
            elif len(password1) < MIN_PASSWORD_LENGTH:
                self.add_error(
                    "password2",
                    _("Password must contain "
                    "at least %(min_length)d characters.") % {
                        'min_length': MIN_PASSWORD_LENGTH
                    }
                )
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        if new_password := self.cleaned_data.get("password1"):
            user.set_password(new_password)
        if commit:
            user.save()
        return user
