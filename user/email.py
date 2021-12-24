from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from helper.utils import account_activation_token

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
    email.send(fail_silently=False)
