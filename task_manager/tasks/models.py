from django.db import models
from django.utils.translation import gettext_lazy as _

from task_manager.statuses.models import Status
from task_manager.users.models import User


class Task(models.Model):
    name = models.CharField(
        max_length=255,
        blank=False,
        unique=True,
        verbose_name=_('Name'),
        help_text=_('Required. Max 255 characters.'),
        error_messages={
            'unique': _('This task already exists. '
            'Select another name and try again.'),
        }
    )
    description = models.TextField(
        blank=True,
        verbose_name=_('Description'),
        help_text=_('Optional task details.')
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        verbose_name=_('Status'),
        related_name='tasks'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='authored_tasks',
        verbose_name=_('Author'),
        editable=False
    )
    executor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='assigned_tasks',
        verbose_name=_('Executor'),
        blank=True,
        null=True,
        help_text=_('Select task executor (optional)')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created at')
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Task')
        verbose_name_plural = _('Tasks')
        ordering = ['-created_at']