from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from form.models import Form

User = get_user_model()


class Subscriber(models.Model):
    email = models.EmailField(unique=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    form = models.ForeignKey(
        Form,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="subscribers",
    )
    verified = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=timezone.now)
    last_modified_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        self.last_modified_date = timezone.now()
        super(Subscriber, self).save(*args, **kwargs)
