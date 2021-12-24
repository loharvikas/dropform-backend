from django.db import models
from workspace.models import Workspace
from django.utils import timezone
import uuid


class Form(models.Model):
    name = models.CharField("Form Name", max_length=200, null=False, blank=False)
    description = models.TextField(blank=True, null=True)
    workspace = models.ForeignKey(
        Workspace, on_delete=models.CASCADE, related_name="forms"
    )
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    active = models.BooleanField(default=True, null=True, blank=True)
    alerts = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=timezone.now)
    last_modified_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.workspace.name} || {self.name}"

    def save(self, *args, **kwargs):
        self.last_modified_date = timezone.now()
        super(Form, self).save(*args, **kwargs)
