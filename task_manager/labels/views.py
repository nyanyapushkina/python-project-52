from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.labels.forms import LabelForm
from task_manager.labels.models import Label
from task_manager.mixins import CustomLoginRequiredMixin, ProtectErrorMixin


class LabelBaseView(CustomLoginRequiredMixin):
    """Base view for label operations."""
    model = Label
    success_url = reverse_lazy("labels:index")


class LabelListView(LabelBaseView, ListView):
    """Display list of all labels."""
    template_name = 'labels/index.html'
    context_object_name = 'labels'
    ordering = ['id']


class LabelFormMixin(SuccessMessageMixin):
    """Shared form configuration for create/update views."""
    template_name = 'labels/form.html'
    form_class = LabelForm


class LabelCreateView(LabelBaseView, LabelFormMixin, CreateView):
    """Create new label."""
    success_message = _('Label created successfully')
    extra_context = {
        'title': _('Create label'),
        'button_name': _('Create')
    }


class LabelUpdateView(LabelBaseView, LabelFormMixin, UpdateView):
    """Update existing label."""
    success_message = _('Label updated successfully')
    extra_context = {
        'title': _('Update label'),
        'button_name': _('Update')
    }


class LabelDeleteView(LabelBaseView, ProtectErrorMixin, DeleteView):
    """Delete label with protection check."""
    template_name = 'labels/delete.html'
    success_message = _('Label deleted successfully')
    protected_object_url = reverse_lazy('labels:index')
    protected_object_message = _('Cannot delete label in use')
    extra_context = {
        'title': _('Delete label'),
        'button_name': _('Yes, delete')
    }