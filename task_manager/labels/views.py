from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.labels.forms import LabelForm
from task_manager.labels.models import Label
from task_manager.mixins import CustomLoginRequiredMixin, ProtectErrorMixin


class LabelBaseView(CustomLoginRequiredMixin):
    model = Label
    success_url = reverse_lazy("labels:index")


class LabelListView(LabelBaseView, ListView):
    template_name = 'labels/index.html'
    context_object_name = 'labels'
    ordering = ['id']


class LabelFormMixin(SuccessMessageMixin):
    template_name = 'labels/form.html'
    form_class = LabelForm


class LabelCreateView(LabelBaseView, LabelFormMixin, CreateView):
    success_message = _('Label created successfully')
    extra_context = {
        'title': _('Create label'),
        'button_name': _('Create')
    }


class LabelUpdateView(LabelBaseView, LabelFormMixin, UpdateView):
    success_message = _('Label updated successfully')
    extra_context = {
        'title': _('Update label'),
        'button_name': _('Update')
    }


class LabelDeleteView(LabelBaseView, SuccessMessageMixin, 
                      ProtectErrorMixin, DeleteView):
    template_name = 'labels/delete.html'
    success_message = _('Label deleted successfully')
    protected_object_url = reverse_lazy('labels:index')
    protected_object_message = _('Cannot delete label in use')
    extra_context = {
        'title': _('Label deletion'),
        'button_name': _('Yes, delete')
    }