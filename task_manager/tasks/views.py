from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView
from django_filters.views import FilterView

from task_manager.mixins import AuthorPermissionMixin, CustomLoginRequiredMixin
from task_manager.tasks.filters import TaskFilter
from task_manager.tasks.forms import TaskForm
from task_manager.tasks.models import Task


class TaskBaseView(CustomLoginRequiredMixin):
    """Base view for task operations."""
    model = Task
    success_url = reverse_lazy('tasks:index')


class TaskListView(TaskBaseView, FilterView):
    """Display filtered list of tasks."""
    template_name = 'tasks/index.html'
    filterset_class = TaskFilter
    context_object_name = 'tasks'
    ordering = ['id']


class TaskDetailView(TaskBaseView, DetailView):
    """Display task details."""
    template_name = 'tasks/detail.html'
    context_object_name = 'task'


class TaskFormMixin(SuccessMessageMixin):
    """Shared configuration for task forms."""
    template_name = 'tasks/form.html'
    form_class = TaskForm


class TaskCreateView(TaskBaseView, TaskFormMixin, CreateView):
    """Create new task."""
    success_message = _('Task created successfully')
    extra_context = {
        'title': _('Create task'),
        'button_name': _('Create')
    }

    def form_valid(self, form):
        """Set current user as task author."""
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(TaskBaseView, TaskFormMixin, UpdateView):
    """Update existing task."""
    success_message = _('Task updated successfully')
    extra_context = {
        'title': _('Update task'),
        'button_name': _('Update')
    }


class TaskDeleteView(TaskBaseView, AuthorPermissionMixin, SuccessMessageMixin, DeleteView):
    """Delete task with author permission check."""
    template_name = 'tasks/delete.html'
    success_message = _('Task deleted successfully')
    permission_denied_url = reverse_lazy('tasks:index')
    permission_denied_message = _("Only the task's author can delete it")
    extra_context = {
        'title': _('Task deletion'),
        'button_name': _('Yes, delete')
    }
