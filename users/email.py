from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from helper.utils import account_activation_token


def send_activation_email(domain, user_pk):
    user = User.objects.get(pk=user_pk)
    mail_subject = "Activate your formstack account."
    message = render_to_string(
        "user_activation_email.html",
        {
            "user": user,
            "domain": domain,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)).decode(),
            "token": account_activation_token.make_token(user),
        },
    )
    email = EmailMessage(mail_subject, message, to=[user.email])
    email.send()
