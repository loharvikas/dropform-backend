import threading
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

from form.models import Form
from submission.models import Submission
from subscriber.models import Subscriber
from user.email import send_activation_email
from workspace.models import Workspace


from . import serializers


User = get_user_model()


class WorkspaceListAPIView(generics.ListCreateAPIView):
    queryset = Workspace.objects.all()
    serializer_class = serializers.WorkspaceSerializer


class WorkspaceUserListAPIView(APIView):
    def get(self, request, pk, *args, **kwargs):
        qs = Workspace.objects.all().filter(user__id=pk)
        serializer = serializers.WorkspaceSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class WorkspaceDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Workspace.objects.all()
    serializer_class = serializers.WorkspaceSerializer


class FormListAPIView(generics.ListCreateAPIView):
    queryset = Form.objects.all()
    serializer_class = serializers.FormSerializer


class FormWorkspaceAPIView(APIView):
    queryset = Form.objects.all()
    serializer_class = serializers.FormSerializer

    def get(self, request, pk, *args, **kwargs):
        qs = Form.objects.all().filter(workspace__id=pk).order_by("-created_date")
        serializer = serializers.FormSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FormDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Form.objects.all()
    serializer_class = serializers.FormSerializer
    lookup_field = "uuid"


class SubmissionFormAPIView(APIView):
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

    def get(self, request, uuid, *args, **kwargs):
        qs = Submission.objects.all().filter(form__uuid=uuid).order_by("-created_date")
        serializer = serializers.SubmissionSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SubmissionListAPIView(generics.ListAPIView):
    parser_classes = [FormParser, MultiPartParser]
    queryset = Submission.objects.all()
    serializer_class = serializers.SubmissionSerializer


class SubscriberListAPIView(generics.ListCreateAPIView):
    queryset = Subscriber.objects.all()
    serializer_class = serializers.SubscriberSerializer


class LoginAPIView(TokenObtainPairView):
    serializer_class = serializers.LoginSerializer
    permission_class = (AllowAny,)


class RegisterAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = serializers.RegisterSerializer(
            data=request.data, context={"request": request}
        )
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


# Endpoint: /users/
class UserListAPIView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = serializers.UserSerializer
    model = User

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer_class(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.erros, status=status.HTTP_400_BAD_REQUEST)


# Endpoint: /users/pk/
class UserDetailAPIView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


# Endpoint: /users/update/pk
class UserUpdateAPIView(generics.UpdateAPIView):
    queryset = User.objects.filter(is_staff=False)
    serializer_class = serializers.UserSerializer


class ActivateEmailAPIView(APIView):
    def post(self, request, *args, **kwargs):
        current_site = get_current_site(request)
        if request.user.is_verified == True:
            t = threading.Thread(
                target=send_activation_email,
                args=(current_site.domain, request.user.pk),
            )
            t.start()
            return Response(
                {"message": "email sent successfully"}, status=status.HTTP_200_OK
            )
        return Response(
            {"message": "User already verified"}, status=status.HTTP_400_BAD_REQUEST
        )


class PasswordChangeAPIView(generics.UpdateAPIView):
    serializer_class = serializers.PasswordChangeSerializer
    model = User

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response(
                    {"message": "Wrong password"}, status=status.HTTP_400_BAD_REQUEST
                )
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response(
                {
                    "status": "success",
                    "code": status.HTTP_200_OK,
                    "message": "Password updated successfully",
                    "data": [],
                }
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
