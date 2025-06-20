from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models.deletion import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.users.forms import (
    CustomUserChangeForm,
    CustomUserCreationForm,
)
from task_manager.users.models import User

USERS_INDEX_URL = reverse_lazy('users:index')
LOGIN_URL = reverse_lazy('login')


class CustomLoginRequiredMixin(LoginRequiredMixin):
    login_url = LOGIN_URL
    redirect_field_name = None
    permission_denied_message = _("You must be logged in to access this page.")

    def handle_no_permission(self):
        messages.error(self.request, self.permission_denied_message)
        return super().handle_no_permission()


class UserPermissionMixin(UserPassesTestMixin):
    permission_denied_url = USERS_INDEX_URL
    permission_denied_message = _("You can only modify your own profile.")

    def test_func(self):
        return self.get_object() == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, self.permission_denied_message)
        return redirect(self.permission_denied_url)


class ProtectErrorMixin:
    protected_redirect_url = USERS_INDEX_URL
    protected_message = _("Cannot delete user with active tasks")

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, self.protected_message)
            return redirect(self.protected_redirect_url)


class UserListView(ListView):
    model = User
    template_name = 'users/index.html'
    context_object_name = 'users'
    ordering = ['id']
    paginate_by = 20

    def get_queryset(self):
        return super().get_queryset().only('id', 
                                           'username', 
                                           'first_name', 
                                           'last_name')


class BaseUserView(SuccessMessageMixin):
    model = User
    template_name = 'users/registration_form.html'
    context_object_name = 'user'
    extra_context = {'form_method': 'post'}


class UserCreateView(BaseUserView, CreateView):
    form_class = CustomUserCreationForm
    success_url = LOGIN_URL
    success_message = _('Registration successful!')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Sign Up')
        context['button_text'] = _('Register')
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class UserUpdateView(CustomLoginRequiredMixin, 
                     UserPermissionMixin, 
                     BaseUserView, 
                     UpdateView):
    form_class = CustomUserChangeForm
    success_url = USERS_INDEX_URL
    success_message = _('Profile updated!')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button_text'] = _('Save')
        return context


class UserDeleteView(CustomLoginRequiredMixin, 
                     UserPermissionMixin, 
                     ProtectErrorMixin, 
                     DeleteView):
    model = User
    template_name = 'users/delete.html'
    success_url = USERS_INDEX_URL
    success_message = _("Account deleted")

    def post(self, request, *args, **kwargs):
        if not request.user.check_password(request.POST.get('password', '')):
            messages.error(request, _("Incorrect password"))
            return self.get(request, *args, **kwargs)
        return super().post(request, *args, **kwargs)
