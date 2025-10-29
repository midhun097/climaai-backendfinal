from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    # Your custom fields
    name = models.CharField(max_length=255)

    # Fix reverse accessor conflicts
    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_set",  # <- change this
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_permissions_set",  # <- change this
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )
