from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from task_manager.tasks.forms import TaskForm
from task_manager.tasks.models import Task


class TaskAccessMixin(LoginRequiredMixin):
    login_url = reverse_lazy('login')
    permission_denied_message = _('You are not authorized! Please log in.')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, self.permission_denied_message)
            return redirect(self.login_url)
        return super().dispatch(request, *args, **kwargs)


class TaskListView(TaskAccessMixin, ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'
    ordering = ['-created_at']

    def get_queryset(self):
        return Task.objects.select_related('author', 'executor', 'status')


class TaskDetailView(TaskAccessMixin, DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'


class TaskCreateView(TaskAccessMixin, SuccessMessageMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('tasks')
    success_message = _('Task created successfully!')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(TaskAccessMixin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('tasks')
    success_message = _('Task updated successfully!')


class TaskDeleteView(TaskAccessMixin, SuccessMessageMixin, DeleteView):
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    success_url = reverse_lazy('tasks')
    success_message = _('Task deleted successfully!')
    author_required_message = _('Only the author can delete a task!')

    def dispatch(self, request, *args, **kwargs):
        task = self.get_object()
        if task.author != request.user:
            messages.error(request, self.author_required_message)
            return redirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)