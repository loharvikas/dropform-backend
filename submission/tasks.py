from celery import shared_task
from celery.utils.log import get_task_logger
from helper import emails

logger = get_task_logger(__name__)


@shared_task
def send_notification_email_task(submission_pk):
    """
        Sends notification email to user whenever new Submission object is created.
    """
    logger.info(
        f'Sending notification email for Submission_pk: {submission_pk}')
    emails.send_notification_email(submission_pk)
    logger.info(f'Notification sent successfully : {submission_pk}')
