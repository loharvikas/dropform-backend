from django.contrib import admin
from django.urls import path, include
from submission.views import SubmissionCreation
from user.views import CheckoutWebhookView, activate_user, CreateCheckoutSessionView, CreateCustomerPortalView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
    path("f/<uuid:uuid>/", SubmissionCreation.as_view(), name="create-submission"),
    path("activate/<uidb64>/<token>/", activate_user, name="activate"),
    path("create-checkout-session/<str:priceType>/<int:user_pk>/", CreateCheckoutSessionView.as_view(),
         name='stripe-checkout-session'),
    path("create-customer-portal/<int:user_pk>/",
         CreateCustomerPortalView.as_view(), name='customer-portal'),
    path('webhooks/create-checkout-session/',
         CheckoutWebhookView.as_view(), name='checkout-webhook')
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
