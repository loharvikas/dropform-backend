from re import sub
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from helper.utils import account_activation_token
from submission.models import Submission

User = get_user_model()


def send_activation_email(domain, user_pk):
    user = User.objects.get(pk=user_pk)

    context = {
        "user": user,
        "domain": domain,
        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
        "token": account_activation_token.make_token(user),
    }

    email_subject = "Activate your formstack account"
    html_content = render_to_string(
        "authentication/user_activation_email.html", context
    )

    email_body = "Activate your formstack account"

    email = EmailMultiAlternatives(
        email_subject,
        email_body,
        settings.DEFAULT_FROM_EMAIL,
        [
            user.email,
        ],
    )
    email.attach_alternative(html_content, "text/html")
    email.send(fail_silently=True)


def send_notification_email(submission_pk):
    s = Submission.objects.get(pk=submission_pk)
    formObject = s.form
    context = {"fields": s.fields, "formName": formObject.name}

    html_content = render_to_string("general/notification.html", context)
    email_subject = "New Submission-Formstack"
    email_body = f"New Submission for {formObject.name}"

    email = EmailMultiAlternatives(
        email_subject,
        email_body,
        settings.DEFAULT_FROM_EMAIL,
        [
            formObject.workspace.user.email,
        ],
    )
    email.attach_alternative(html_content, "text/html")
    email.send(fail_silently=False)
