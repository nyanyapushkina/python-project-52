from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from task_manager.users.models import User


class BaseUserForm:
    """Shared configuration for all user forms."""
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username')
        labels = {
            'first_name': _('First Name'),
            'last_name': _('Last Name'),
        }
        help_texts = {
            'username': _(
                'Required. 150 characters or fewer. '
                'Letters, digits and @/./+/-/_ only.'
            ),
        }


class CustomUserCreationForm(UserCreationForm):
    """User registration form."""
    class Meta(BaseUserForm.Meta):
        fields = (*BaseUserForm.Meta.fields, 'password1', 'password2')
        help_texts = {
            **BaseUserForm.Meta.help_texts,
            'password1': _('Minimum 3 characters.'),
            'password2': _('Enter the same password for verification.'),
        }
    
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError(_('This username is already taken.'))
        return username

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error('password2', _("Passwords don't match."))
            if len(password1) < 3:
                self.add_error(
                    "password2",
                    _("This password is too short. "
                    "It must contain at least 3 characters.")
                )
        return cleaned_data


class CustomUserChangeForm(forms.ModelForm):
    """User profile edit form with optional password change."""
    password1 = forms.CharField(
        label=_('New Password'),
        widget=forms.PasswordInput,
        required=False,
        help_text=_('Minimum 3 characters. ' 
        'Leave empty to keep current password.'),
    )
    password2 = forms.CharField(
        label=_('Confirm Password'),
        widget=forms.PasswordInput,
        required=False,
        help_text=_('Enter the same password for verification.'),
    )

    class Meta(BaseUserForm.Meta):
        fields = (*BaseUserForm.Meta.fields, 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'password' in self.fields:
            del self.fields['password']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 or password2:
            if password1 != password2:
                self.add_error('password2', _("Passwords don't match."))
            elif len(password1) < 3:
                self.add_error('password1', 
                               _('Password too short (min 3 characters).'))
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        if password1 := self.cleaned_data.get("password1"):
            user.set_password(password1)
        if commit:
            user.save()
        return user
