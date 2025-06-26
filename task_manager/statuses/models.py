from django.db import models
from django.utils.translation import gettext_lazy as _


class Status(models.Model):
    """Model representing task status with name uniqueness enforcement."""
    name = models.CharField(
        max_length=255,
        blank=False,
        verbose_name=_('Name'),
        unique=True,
        error_messages={
            'unique': _('A status with this name already exists.'),
        }
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Status')
        verbose_name_plural = _('Statuses')
        ordering = ['name']