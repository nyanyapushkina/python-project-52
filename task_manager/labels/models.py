from django.db import models
from django.db.models.deletion import ProtectedError
from django.utils.translation import gettext_lazy as _


class Label(models.Model):
    """Label model for task categorization."""
    name = models.CharField(
        max_length=255,
        blank=False,
        verbose_name=_('Name'),
        unique=True,
        error_messages={
            'unique': _('A label with this name already exists.'),
        }
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def delete(self, *args, **kwargs):
        """Prevents deletion if label is referenced by any tasks."""
        if self.task_set.exists():
            raise ProtectedError(
                _("Cannot delete label in use"),
                self
            )
        return super().delete(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Label')
        verbose_name_plural = _('Labels')
        ordering = ['name']
