from django.shortcuts import render
from django.http import HttpResponse
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from .models import User
from helper.utils import account_activation_token

# Create your views here.


def activate_user(request, uidb64, token):
    try:
        uuid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uuid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse(
            "Thank you for your email confirmation. Now you can login your account."
        )
    else:
        return HttpResponse("Activation link is invalid!")
