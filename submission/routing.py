from django.urls import path
from django.conf import settings

from . import consumers

websocket_protocol = 'ws' if settings.DEVELOPMENT_MODE == True else 'wss'

websocket_urlpatterns = [
    path(f"{websocket_protocol}/form/<uuid:formId>/",
         consumers.SubmissionConsumer.as_asgi())
]
