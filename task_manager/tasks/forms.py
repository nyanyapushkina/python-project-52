from django.forms import ModelForm

from task_manager.mixins import FormStyleMixin
from task_manager.tasks.models import Task


class TaskForm(FormStyleMixin, ModelForm):
    """Form for creating and updating tasks."""
    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'labels']