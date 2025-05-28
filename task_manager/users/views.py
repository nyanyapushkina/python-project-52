from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models.deletion import ProtectedError
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.contrib.auth import login
from django.core.exceptions import PermissionDenied
from .models import User
from .forms import CustomUserChangeForm, CustomUserCreationForm


class CustomLoginRequiredMixin(LoginRequiredMixin):
    login_url = reverse_lazy('login')
    redirect_field_name = None

    def handle_no_permission(self) -> HttpResponseRedirect:
        if not self.request.user.is_authenticated:
            messages.error(
                self.request,
                _('You must be logged in to access this page.')
            )
        return super().handle_no_permission()


class UserPermissionMixin(UserPassesTestMixin):
    permission_denied_url = reverse_lazy('users:index')
    permission_denied_message = _("You don't have permission to modify this user.")
    raise_exception = False

    def test_func(self) -> bool:
        target_user = self.get_object()
        return target_user == self.request.user

    def handle_no_permission(self) -> HttpResponseRedirect:
        if self.request.user.is_authenticated:
            messages.error(self.request, self.permission_denied_message)
        return redirect(self.permission_denied_url)


class ProtectErrorMixin:
    protected_object_url = reverse_lazy('users:index')
    protected_object_message = _('Cannot delete user because they are being used')

    def post(self, request, *args, **kwargs) -> HttpResponseRedirect:
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, self.protected_object_message)
            return redirect(self.protected_object_url)


class UserListView(ListView):
    model = User
    template_name = 'users/index.html'
    context_object_name = 'users'
    ordering = ['id']
    paginate_by = 20


class BaseUserView(SuccessMessageMixin):
    """Base view for user operations."""
    model = User
    template_name = 'users/registration_form.html'
    context_object_name = 'user'
    extra_context = {
        'button_text': _('Submit'),
        'form_method': 'post'
    }


class UserCreateView(BaseUserView, CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    success_message = _('User registered successfully! You can now log in.')

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context.update({
            'title': _('Sign Up'),
            'button_text': _('Register'),
        })
        return context

    def form_valid(self, form) -> HttpResponseRedirect:
        response = super().form_valid(form)
        login(self.request, self.object)  # Auto-login after registration
        messages.success(self.request, self.success_message)
        return response


class UserUpdateView(CustomLoginRequiredMixin, UserPermissionMixin, BaseUserView, UpdateView):
    form_class = CustomUserChangeForm
    success_url = reverse_lazy('users:index')
    success_message = _('Profile updated successfully!')

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context.update({
            'title': _('Edit Profile'),
            'button_text': _('Save Changes'),
            'show_password': True,
        })
        return context


class UserDeleteView(CustomLoginRequiredMixin, UserPermissionMixin, ProtectErrorMixin, BaseUserView, DeleteView):
    template_name = 'users/user_delete.html'
    success_url = reverse_lazy('users:index')
    success_message = _('Account deleted successfully')

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context.update({
            'title': _('Confirm Account Deletion'),
            'warning_message': _('This action cannot be undone.'),
        })
        return context

    def post(self, request, *args, **kwargs) -> HttpResponseRedirect:
        if not request.user.check_password(request.POST.get('password', '')):
            messages.error(request, _('Incorrect password'))
            return self.get(request, *args, **kwargs)
        messages.success(request, self.success_message)
        return super().post(request, *args, **kwargs)