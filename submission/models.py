from django.db import models
from form.models import Form
from django.utils import timezone


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


class SubmissionFileUpload(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    file_field = models.FileField(blank=True, null=True)
    submission = models.ForeignKey(
        Submission, on_delete=models.CASCADE, related_name="files"
    )

    def __str__(self):
        return self.submission.form.name
