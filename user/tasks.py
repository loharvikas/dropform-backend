from django.utils import timezone
from celery import shared_task
from celery.utils.log import get_task_logger

from django.contrib.auth import get_user_model
from django.conf import settings
import stripe

from helper import emails

User = get_user_model()
logger = get_task_logger(__name__)


@shared_task
def create_stripe_customer(user_pk):
    """ 
        Create Stripe customer instance when a user is created.
        To simplify future payments related to user.
    """
    stripe.api_key = settings.STRIPE_SECRET_KEY
    user = User.objects.get(pk=user_pk)
    try:
        logger.info('Create Stripe customer object initialized.')

        customer = stripe.Customer.create(
            email=user.email,
            name=user.full_name
        )
        user.stripe_customer_id = customer.id
        user.save()

        logger.info('Stripe customer object created successfully!')
    except Exception as e:
        logger.error('Stripe customer object created successfully!')
        logger.error(e)


@shared_task
def send_activation_email_task(domain, user_pk):
    """
        Sends activation email to user's registered email.
    """
    logger.info(f'Sending activation email for USER_PK: {user_pk}')
    emails.send_activation_email(domain, user_pk)
    logger.info(f'Activation email sent successfully for USER_PK: {user_pk}')


@shared_task
def change_rotation_date_task():
    """
        This changes the user's last_rotation date every month.
    """
    logger.info('Change rotation date task initialized.')
    current_date = timezone.now()
    user_qs = User.objects.all()
    for user in user_qs:
        date = current_date - user.last_rotation_date
        if date.days() > 30:
            user.last_rotation_date = current_date
            user.save()
            logger.info(
                f'Date changed successfull for USER: {user.email}')
    logger.info('Change rotation date task finished.')
