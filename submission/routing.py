from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path(f"ws/form/<uuid:formId>/",
         consumers.SubmissionConsumer.as_asgi())
]
