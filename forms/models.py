from django.db import models
from workspace.models import Workspace
from django.utils import timezone
from subscribers.models import Subscriber


class Form(models.Model):
    name = models.CharField("Form Name", max_length=200, null=False, blank=False)
    workspace = models.ForeignKey(
        Workspace, on_delete=models.CASCADE, related_name="forms"
    )
    subscriber = models.ManyToManyField(Subscriber, blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    last_modified_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.workspace.name} || {self.name}"

    def save(self, *args, **kwargs):
        self.last_modified_date = timezone.now()
        super(Form, self).save(*args, **kwargs)


class Submission(models.Model):
    fields = models.JSONField(null=True)
    form = models.ForeignKey(
        Form,
        on_delete=models.CASCADE,
        related_name="submissions",
        null=True,
        blank=True,
    )
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.form.name} || {self.pk}"
