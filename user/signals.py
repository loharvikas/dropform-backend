from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from .tasks import create_stripe_customer


User = get_user_model()


@receiver(post_save, sender=User)
def handler(sender, created, instance, *args, **kwargs):
    if created:
        create_stripe_customer.delay(instance.pk)
