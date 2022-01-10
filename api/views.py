from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site


from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.pagination import PageNumberPagination

from form.models import Form
from submission.models import Submission
from subscriber.models import Subscriber
from workspace.models import Workspace
from helper import constants
from user.tasks import send_activation_email_task


from . import serializers


User = get_user_model()


class WorkspaceListAPIView(generics.ListCreateAPIView):
    queryset = Workspace.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = serializers.WorkspaceSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data.get("user", None)
            if user:
                account_limitaions = constants.ACCOUNT_LIMITATIONS[
                    user.account_type.capitalize()
                ]
                if account_limitaions["total_workspaces"] < user.total_workspaces:
                    return Response(
                        {
                            "message": "Workspace limit exceeded please upgrade your account!"
                        },
                        status=status.HTTP_402_PAYMENT_REQUIRED,
                    )
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk, *args, **kwargs):
        """
            returns all the workspace associated with user.
        """
        qs = Workspace.objects.all().filter(user__id=pk)
        serializer = serializers.WorkspaceSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class WorkspaceDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Workspace.objects.all()
    serializer_class = serializers.WorkspaceSerializer


class FormListAPIView(generics.ListCreateAPIView):
    queryset = Form.objects.all()
    serializer_class = serializers.FormSerializer

    def post(self, request, *args, **kwargs):
        serializer = serializers.FormSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data.get("user", None)
            if user:
                account_limitations = constants.ACCOUNT_LIMITATIONS[
                    user.account_type.capitalize()
                ]
                if account_limitations["total_forms"] < user.total_forms:
                    return Response(
                        {"message": "Form limit exceeded please upgrade your account!"},
                        status=status.HTTP_402_PAYMENT_REQUIRED,
                    )
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk, *args, **kwargs):
        """
            return all forms associated with its workspace instance.
        """
        qs = Form.objects.all().filter(workspace__id=pk).order_by("-created_date")
        serializer = serializers.FormSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FormDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Form.objects.all()
    serializer_class = serializers.FormSerializer
    lookup_field = "uuid"


class SubmissionAPIView(generics.ListCreateAPIView):
    queryset = Submission.objects.all()
    serializer_class = serializers.SubmissionSerializer
    parser_classes = [FormParser, MultiPartParser]
    pagination_class = PageNumberPagination

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

    def get_queryset(self):
        """
            returns all submissions associated with its form instance.
        """
        qs = (
            Submission.objects.all()
            .filter(form__uuid=self.kwargs["uuid"])
            .order_by("-created_date")
        )
        return qs


class SubmissionDetailAPIView(generics.DestroyAPIView):
    queryset = Submission.objects.all()
    serializer_class = serializers.SubmissionSerializer

    def delete(self, request, *args, **kwargs):
        data = request.data["rowIds"]
        submissionObject = Submission.objects.filter(pk__in=data)
        submissionObject.delete()
        return Response({"message": "Successfully deleted"}, status=status.HTTP_200_OK)


class SubscriberListAPIView(generics.ListCreateAPIView):
    queryset = Subscriber.objects.all()
    serializer_class = serializers.SubscriberSerializer


class LoginAPIView(TokenObtainPairView):
    serializer_class = serializers.LoginSerializer
    permission_class = (AllowAny,)


class GoogleLoginAPIView(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        data = request.data

        serializer = serializers.GoogleAuthenticationSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            user.is_verified = True
            user.save()
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "user": serializer.data,
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterAPIView(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = []

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
        if request.user.is_verified == False:
            send_activation_email_task.delay(
                current_site.domain, request.user.pk)
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
