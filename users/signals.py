from django.db.models.signals import post_save
from subscribers.models import Subscriber
from django.dispatch import receiver
from django.contrib.auth import get_user_model

User = get_user_model()


@receiver(post_save, sender=User)
def handler(sender, created, instance, *args, **kwargs):
    if created:
        email = instance.email
        s, created = Subscriber.objects.get_or_create(email=email)
