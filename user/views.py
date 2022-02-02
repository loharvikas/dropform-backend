from pprint import pprint
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

import json

from .models import User
from helper.utils import account_activation_token
from helper import constants
import stripe


User = get_user_model()


def activate_user(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_verified = True
        user.save()
        return redirect("https://www.dropform.co")
    else:
        return HttpResponse("Activation link is invalid!")


stripe.api_key = settings.STRIPE_SECRET_KEY
host_url = 'localhost:3000' if settings.DEVELOPMENT_MODE == True else 'www.dropform.co'
host_protocol = 'http' if settings.DEVELOPMENT_MODE == True else 'https'


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
                success_url=f'{host_protocol}://{host_url}',
                cancel_url=f'{host_protocol}://{host_url}',
                customer=user.stripe_customer_id
            )
        except Exception as e:
            return HttpResponse(status=400)
        return redirect(checkout_session.url, code=303)


@method_decorator(csrf_exempt, name='dispatch')
class CreateCustomerPortalView(View):
    def post(self, request, user_pk, *args, **kwargs):
        user = User.objects.get(pk=user_pk)
        try:
            session = stripe.billing_portal.Session.create(
                customer=user.stripe_customer_id,
                return_url=f'{host_protocol}://{host_url}',
            )
        except Exception as e:
            return HttpResponse(status=400)
        return redirect(session.url, code=303)


# WEBHOOKS
@method_decorator(csrf_exempt, name='dispatch')
class CheckoutWebhookView(View):
    def post(self, request, *args, **kwargs):
        payload = json.loads(request.body)
        event = None
        global account_type
        account_type = None
        try:
            event = stripe.Event.construct_from(
                payload, stripe.api_key)
            customer_id = event.data.object.customer
            user = User.objects.get(stripe_customer_id=customer_id)
            price_id = event.data.object.lines.data[0].price.id
            if price_id == settings.STRIPE_PRODUCT_STANDARD_ID:
                account_type = constants.ACCOUNT_STANDARD
            elif price_id == settings.STRIPE_PRODUCT_BUSINESS_ID:
                account_type = constants.ACCOUNT_BUSINESS
            elif price_id == settings.STRIPE_PRODUCT_PRO_ID:
                account_type = constants.ACCOUNT_PROFESSIONAL
            else:
                return HttpResponse(status=400)
        except ValueError as e:
            # Invalid payload
            return HttpResponse(status=400)
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            return HttpResponse(status=400)

        if event.type == 'checkout.session.completed':
            print('Checkout success session completed')
        elif event.type == 'invoice.paid':
            user.paid_user = True
            user.account_type = account_type
            user.save()
        elif event.type == 'invoice.payment_failed':
            user.paid_user = False
            user.account_type = constants.ACCOUNT_TESTING
            user.save()
        elif event.type == 'invoice.payment_succeeded':
            user.paid_user = True
            user.account_type = account_type
            user.save()
        elif event.type == 'invoice.updated':
            user.paid_user = True
            user.account_type = account_type
            user.save()
        else:
            print('Unhandled event type {}'.format(event.type))

        return HttpResponse(status=200)


@method_decorator(csrf_exempt, name='dispatch')
class CustomerPortalWebhookView(View):
    def post(self, request, *args, **kwargs):
        payload = json.loads(request.body)
        event = None
        global account_type
        account_type = None
        try:
            event = stripe.Event.construct_from(
                payload, stripe.api_key)
            customer_id = event.data.object.customer
            user = User.objects.get(stripe_customer_id=customer_id)
            price_id = event.data.object['items'].data[0].price.id
            if price_id == settings.STRIPE_PRODUCT_STANDARD_ID:
                account_type = constants.ACCOUNT_STANDARD
            elif price_id == settings.STRIPE_PRODUCT_BUSINESS_ID:
                account_type = constants.ACCOUNT_BUSINESS
            elif price_id == settings.STRIPE_PRODUCT_PRO_ID:
                account_type = constants.ACCOUNT_PROFESSIONAL
            else:
                return HttpResponse(status=400)
        except ValueError as e:
            # Invalid payload
            return HttpResponse(status=400)
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            return HttpResponse(status=400)

        if event.type == 'customer.subscription.deleted':
            user.paid_user = False
            user.account_type = constants.ACCOUNT_TESTING
            user.save()
        elif event.type == 'customer.subscription.updated':
            user.account_type = account_type
            user.save()
        else:
            print('CUSTOMER PORTAL')
            print('Unhandled event type {}'.format(event.type))
        return HttpResponse(status=200)
