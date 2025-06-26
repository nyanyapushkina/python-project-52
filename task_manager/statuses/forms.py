from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from task_manager.mixins import FormStyleMixin
from task_manager.statuses.models import Status


class StatusForm(FormStyleMixin, ModelForm):
    """Form for creating and updating Status instances."""
    class Meta:
        model = Status
        fields = ['name']
        labels = {
            'name': _('Name'),
        }
