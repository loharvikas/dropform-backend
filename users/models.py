from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField("Email Address", unique=True)
    is_active = models.BooleanField(default=False)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)
    last_modified_date = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        self.last_modified_date = timezone.now()
        super(User, self).save(*args, **kwargs)
