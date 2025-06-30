from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Custom user model with first and last names required."""

    first_name = models.CharField(
        max_length=150,
        blank=False,
        null=False,
        verbose_name=_('First Name'),
    )
    last_name = models.CharField(
        max_length=150,
        blank=False,
        null=False,
        verbose_name=_('Last Name'),
    )

    USERNAME_FIELD = 'username'

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return self.get_full_name()