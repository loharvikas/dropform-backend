from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from helper.utils import create_stripe_customer
import threading


User = get_user_model()


@receiver(post_save, sender=User)
def handler(sender, created, instance, *args, **kwargs):
    if created:
        t = threading.Thread(target=create_stripe_customer,
                             args=(instance.email, ))
        t.start()
