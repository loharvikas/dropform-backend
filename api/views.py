from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from forms.models import Form, Submission
from subscribers.models import Subscriber
from workspace.models import Workspace
from . import serializers
from rest_framework import generics
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User

User = get_user_model()

# Endpoint: /users/
class UserListAPIView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    serialzer_class = serializers.UserSerializer


# Endpoint: /users/pk/
class UserDetailAPIView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


# Endpoint: /users/update/pk
class UserUpdateAPIView(generics.UpdateAPIView):
    queryset = User.objects.filter(is_staff=False)
    serializer_class = serializers.UserSerializer


class LoginAPIView(TokenObtainPairView):
    serializer_class = serializers.LoginSerializer
    permission_class = (AllowAny,)


class RegisterAPIView(APIView):
    permission_class = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = serializers.RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            res = {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }

            return Response(
                {
                    "user": serializer.data,
                    "refresh": res["refresh"],
                    "access": res["access"],
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def post(self, request, *args, **kwargs):
    #     serializer = serializers.RegisterSerializer(data=request.data)
    #     print("IM HERE")
    #     serializer.is_valid()
    #     user = serializer.save()
    #     refresh = RefreshToken.for_user(user)

    #     res = {
    #         "refresh": str(refresh),
    #         "access": str(refresh.access_token),
    #     }

    #     return Response(
    #         {
    #             "user": serializer.data,
    #             "refresh": res["refresh"],
    #             "token": res["access"],
    #         },
    #         status=status.HTTP_201_CREATED,
    #     )


class WorkspaceListAPIView(generics.ListCreateAPIView):
    queryset = Workspace.objects.all()
    serializer_class = serializers.WorkspaceSerializer


class WorkspaceDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Workspace.objects.all()
    serializer_class = serializers.WorkspaceSerializer


class FormListAPIView(generics.ListCreateAPIView):
    queryset = Form.objects.all()
    serializer_class = serializers.FormSerializer


class FormDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Form.objects.all()
    serializer_class = serializers.FormSerializer


class CreateSubmissionAPIView(APIView):
    parser_classes = [FormParser, MultiPartParser]

    def post(self, request, *args, **kwargs):
        qd = request.data
        fields = qd.dict()
        uuid = kwargs.get("uuid")
        form = Form.objects.get(uuid=uuid)
        data = {"fields": fields, "form": form.id}
        serializer = serializers.SubmissionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubmissionListAPIView(generics.ListAPIView):
    parser_classes = [FormParser, MultiPartParser]
    queryset = Submission.objects.all()
    serializer_class = serializers.SubmissionSerializer


class SubscriberListAPIView(generics.ListCreateAPIView):
    queryset = Subscriber.objects.all()
    serializer_class = serializers.SubscriberSerializer
