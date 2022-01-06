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
import environ
import json

env = environ.Env()
environ.Env.read_env()

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

class CheckoutWebhookView(View):
    def post(self, request, *args, **kwargs):
        webhook_secret = 'whsec_Shm8Swr3TzZoEDak4KSFO6NcbiqPVM2W'
        request_data = json.loads(request.data)

        if webhook_secret:
            # Retrieve the event by verifying the signature using the raw body and secret if webhook signing is configured.
            signature = request.headers.get('stripe-signature')
            try:
                event = stripe.Webhook.construct_event(
                    payload=request.data, sig_header=signature, secret=webhook_secret)
                data = event['data']
            except Exception as e:
                return e
            # Get the type of webhook event sent - used to check the status of PaymentIntents.
            event_type = event['type']
        else:
            data = request_data['data']
            event_type = request_data['type']
        data_object = data['object']
        if event_type == 'checkout.session.completed':
            print('SUCCESSL:', data)
        elif event_type == 'invoice.paid':
            print('INVOICES:')
            print(data)
        elif event_type == 'invoice.payment_failed':
            print('FAILDED:',)
            print(data)
        else:
            print('Unhandled event type {}'.format(event_type))

        return JsonResponse({'status': 'success'})
