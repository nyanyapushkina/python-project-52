from pyexpat.errors import messages

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.labels.forms import LabelForm
from task_manager.labels.models import Label


class LabelListView(LoginRequiredMixin, ListView):
    model = Label
    template_name = 'labels/list.html'
    context_object_name = 'labels'


class LabelCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Label
    form_class = LabelForm
    template_name = 'labels/create.html'
    success_url = reverse_lazy('labels:list')
    success_message = _('Label successfully created')


class LabelUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Label
    form_class = LabelForm
    template_name = 'labels/update.html'
    success_url = reverse_lazy('labels:list')
    success_message = _('Label successfully updated')


class LabelDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Label
    template_name = 'labels/delete.html'
    success_url = reverse_lazy('labels:list')
    success_message = _('Label successfully deleted')
    protected_message = _('Cannot delete label because it is in use')

    def dispatch(self, request, *args, **kwargs):
        label = self.get_object()
        if label.task_set.exists():
            messages.error(request, self.protected_message)
            return redirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)