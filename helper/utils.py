from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth import get_user_model
from django.conf import settings

import six
import stripe

User = get_user_model()


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk)
            + six.text_type(timestamp)
            + six.text_type(user.is_active)
        )


account_activation_token = TokenGenerator()


def create_stripe_customer(email):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    user = User.objects.get(email=email)
    try:
        customer = stripe.Customer.create(
            email=user.email,
            name=user.full_name
        )
        print('C:', customer)
        user.stripe_customer_id = customer.id
        user.save()
    except Exception as e:
        print('EEE:', e)
