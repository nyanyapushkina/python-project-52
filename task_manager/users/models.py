from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.
    Requires first_name and last_name fields to be non-empty.
    """
    first_name = models.CharField(
        max_length=150,
        blank=False,
        verbose_name=_('First Name'),
        help_text=_('Required. 150 characters or fewer.')
    )
    last_name = models.CharField(
        max_length=150,
        blank=False,
        verbose_name=_('Last Name'),
        help_text=_('Required. 150 characters or fewer.')
    )

    USERNAME_FIELD = 'username'

    def __str__(self):
        """Display user as 'First Last'."""
        return f'{self.first_name} {self.last_name}'
