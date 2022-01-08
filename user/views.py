from django.http import HttpResponse
from django.http.response import JsonResponse
from django.shortcuts import redirect
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.views.generic import View
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model

from .models import User
from helper.utils import account_activation_token
from helper import constants
import stripe
import json


User = get_user_model()


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


stripe.api_key = settings.STRIPE_SECRET_KEY


@method_decorator(csrf_exempt, name='dispatch')
class CreateCheckoutSessionView(View):
    def post(self, request, priceType, user_pk, *args, **kwargs):
        user = User.objects.get(pk=user_pk)
        priceId = None
        if priceType == constants.ACCOUNT_BUSINESS:
            priceId = settings.STRIPE_PRODUCT_BUSINESS_ID
        elif priceType == constants.ACCOUNT_PROFESSIONAL:
            priceId = settings.STRIPE_PRODUCT_PRO_ID
        elif priceType == constants.ACCOUNT_STANDARD:
            priceId = settings.STRIPE_PRODUCT_STANDARD_ID
        else:
            return HttpResponse(status=400)
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price': priceId,
                        'quantity': 1,
                    },
                ],
                mode='subscription',
                success_url='http://127.0.0.1:3000',
                cancel_url='http://127.0.0.1:3000',
                customer=user.stripe_customer_id
            )
        except Exception as e:
            print('EEE;', e)
            return HttpResponse(status=400)
        return redirect(checkout_session.url, code=303)


@method_decorator(csrf_exempt, name='dispatch')
class CreateCustomerPortalView(View):
    def post(self, request, user_pk, *args, **kwargs):
        user = User.objects.get(pk=user_pk)
        try:
            session = stripe.billing_portal.Session.create(
                customer=user.stripe_customer_id,
                return_url='http://127.0.0.1:3000',
            )
        except Exception as e:
            return HttpResponse(status=400)
        return redirect(session.url, code=303)


# WEBHOOKS
@method_decorator(csrf_exempt, name='dispatch')
class CheckoutWebhookView(View):
    def post(self, request, *args, **kwargs):
        endpoint_secret = 'we_1KEwwoSBvjL8IfZ6fhDJyrAi'
        payload = request.body
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        event = None
        print('PAYLOAD::', payload.decode('utf-8'))
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret)
        except ValueError as e:
            print('INVALID PAYLOAD')
            # Invalid payload
            return HttpResponse(status=400)
        except stripe.error.SignatureVerificationError as e:
            print('INVALID SIG')
            # Invalid signature
            return HttpResponse(status=400)

        if event.type == 'checkout.session.completed':
            print('Checkout success PaymentIntent was successful!')
        elif event.type == 'invoice.paid':
            print('Invoice Failed was attached to a Customer!')
        else:
            print('Unhandled event type {}'.format(event.type))

        return HttpResponse(status=200)
