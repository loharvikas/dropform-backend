from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from api.serializers import SubmissionSerializer
from .models import Submission

channel_layer = get_channel_layer()


@receiver(post_save, sender=Submission)
def handler(sender, instance, created, **kwargs):
    if not created:
        serializer = SubmissionSerializer(instance)
        files = instance.files.all()
        async_to_sync(channel_layer.group_send)(
            f"form_{instance.form.uuid}",
            {"type": "send_submission", "message": serializer.data},
        )
