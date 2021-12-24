from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode

from .models import User
from helper.utils import account_activation_token


def activate_user(request, uidb64, token):
    try:
        uuid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uuid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_verified = True
        user.save()
        return redirect("http://localhost:3000")
    else:
        return HttpResponse("Activation link is invalid!")
