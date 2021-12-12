from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from forms.models import Form, Submission
from subscribers.models import Subscriber
from workspace.models import Workspace
from .serializers import (
    FormSerializer,
    SubmissionSerializer,
    SubscriberSerializer,
    UserSerializer,
    WorkspaceSerializer,
)
from rest_framework import generics
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework import status
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.models import User
from helper.utils import account_activation_token

User = get_user_model()

# Endpoint: /users/
class UserListAPIView(APIView):
    def post(request, *args, **kwargs):
        serializer = UserSerializer(request.data, conext={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Endpoint: /users/pk/
class UserDetailAPIView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Endpoint: /users/update/pk
class UserUpdateAPIView(generics.UpdateAPIView):
    queryset = User.objects.filter(is_staff=False)
    serializer_class = UserSerializer


class WorkspaceListAPIView(generics.ListCreateAPIView):
    queryset = Workspace.objects.all()
    serializer_class = WorkspaceSerializer


class WorkspaceDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Workspace.objects.all()
    serializer_class = WorkspaceSerializer


class FormListAPIView(generics.ListCreateAPIView):
    queryset = Form.objects.all()
    serializer_class = FormSerializer


class FormDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Form.objects.all()
    serializer_class = FormSerializer


class CreateSubmissionAPIView(APIView):
    parser_classes = [FormParser, MultiPartParser]

    def post(self, request, *args, **kwargs):
        qd = request.data
        fields = qd.dict()
        uuid = kwargs.get("uuid")
        form = Form.objects.get(uuid=uuid)
        data = {"fields": fields, "form": form.id}
        serializer = SubmissionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubmissionListAPIView(generics.ListAPIView):
    parser_classes = [FormParser, MultiPartParser]
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer


class SubscriberListAPIView(generics.ListCreateAPIView):
    queryset = Subscriber.objects.all()
    serializer_class = SubscriberSerializer


# def activate_user(request, uidb64, token):
#     try:
#         uid = force_text(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(pk=uid)
#     except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#         user = None
#     if user is not None and account_activation_token.check_token(user, token):
#         user.is_active = True
#         user.save()
#         return HttpResponse(
#             "Thank you for your email confirmation. Now you can login your account."
#         )
#     else:
#         return HttpResponse("Activation link is invalid!")
