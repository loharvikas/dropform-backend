from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path("ws/form/<uuid:formId>/", consumers.SubmissionConsumer.as_asgi())
]
