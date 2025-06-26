from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.mixins import CustomLoginRequiredMixin, ProtectErrorMixin
from task_manager.statuses.forms import StatusForm
from task_manager.statuses.models import Status


class StatusBaseView(CustomLoginRequiredMixin):
    """Base view for status operations."""
    model = Status
    success_url = reverse_lazy("statuses:index")


class StatusListView(StatusBaseView, ListView):
    """Display list of all statuses."""
    template_name = 'statuses/index.html'
    context_object_name = 'statuses'
    ordering = ['id']


class StatusCreateView(StatusBaseView, SuccessMessageMixin, CreateView):
    """Create new status."""
    template_name = 'statuses/form.html'
    form_class = StatusForm
    success_message = _('Status was created successfully')
    extra_context = {
        'title': _('Create status'),
        'button_name': _('Create')
    }


class StatusUpdateView(StatusBaseView, SuccessMessageMixin, UpdateView):
    """Update existing status."""
    template_name = 'statuses/form.html'
    form_class = StatusForm
    success_message = _('Status was updated successfully')
    extra_context = {
        'title': _('Update status'),
        'button_name': _('Update')
    }


class StatusDeleteView(StatusBaseView, SuccessMessageMixin, ProtectErrorMixin, DeleteView):
    """Delete status with protection check."""
    template_name = 'statuses/delete.html'
    success_message = _('Status was deleted successfully')
    protected_object_url = reverse_lazy('statuses:index')
    protected_object_message = _('Cannot delete status in use')
    extra_context = {
        'title': _('Status deletion'),
        'button_name': _('Yes, delete')
    }
