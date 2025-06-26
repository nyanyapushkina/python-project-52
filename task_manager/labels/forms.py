from django.forms import ModelForm

from task_manager.labels.models import Label
from task_manager.mixins import FormStyleMixin


class LabelCreationForm(FormStyleMixin, ModelForm):
    """ModelForm for creating and updating Label instances."""
    class Meta:
        model = Label
        fields = ['name']