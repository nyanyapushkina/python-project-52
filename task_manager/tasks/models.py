from django.db import models
from django.utils.translation import gettext_lazy as _

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.users.models import User


class Task(models.Model):
    """Task model representing work items with status, executor and labels."""
    name = models.CharField(
        max_length=255,
        blank=False,
        verbose_name=_('Name'),
        unique=True,
        error_messages={
            'unique': _('Task with this name already exists'),
        }
    )
    description = models.TextField(
        verbose_name=_('Description'),
        blank=True,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name=_('Author'),
        related_name='author',
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        verbose_name=_('Status'),
    )
    executor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name=_('Executor'),
        related_name='executor',
        blank=True,
        null=True,
    )
    labels = models.ManyToManyField(
        Label,
        verbose_name=_('Labels'),
        blank=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created at'),
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Task')
        verbose_name_plural = _('Tasks')
        ordering = ['-created_at']