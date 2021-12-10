from django.db.models.signals import post_save
from subscribers.models import Subscriber
from django.dispatch import receiver
from .models import Form


@receiver(post_save, sender=Form)
def handler(sender, created, instance, *args, **kwargs):
    if created:
        email = instance.workspace.user.email
        object, created = Subscriber.objects.get_or_create(email=email)
        instance.subscriber.add(object)
