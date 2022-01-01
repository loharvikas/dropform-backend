from django.contrib.auth.models import update_last_login
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.sites.shortcuts import get_current_site

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from user.email import send_activation_email

from workspace.models import Workspace
from form.models import Form
from subscriber.models import Subscriber
from submission.models import Submission

import threading

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Create method for user serializer is defined in RegisterSerializer
    """

    id = serializers.IntegerField(required=False)
    email = serializers.EmailField(required=False)
    password = serializers.CharField(required=False, write_only=True)
    full_name = serializers.CharField(required=False, max_length=255)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "full_name",
            "password",
            "is_active",
            "is_verified",
            "date_joined",
            "last_modified_date",
        ]


class RegisterSerializer(UserSerializer):
    full_name = serializers.CharField(max_length=255, required=True)
    password = serializers.CharField(max_length=255, required=True, write_only=True)
    email = serializers.EmailField(
        max_length=255,
        required=True,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="User with this email address already exist.",
            )
        ],
    )

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "password",
            "full_name",
            "is_active",
            "is_verified",
            "date_joined",
            "last_modified_date",
        ]

    def create(self, validated_data):
        try:
            user = User.objects.get(email=validated_data["email"])
        except ObjectDoesNotExist:
            user = User.objects.create_user(**validated_data)
            requestObject = self.context.get("request")
            if requestObject:
                current_site = get_current_site(requestObject)
                t = threading.Thread(
                    target=send_activation_email, args=(current_site.domain, user.pk)
                )
                t.start()
        return user


class GoogleAuthenticationSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(max_length=255, required=True)
    password = serializers.CharField(max_length=255, required=False, write_only=True)
    email = serializers.EmailField(max_length=255, required=True)

    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):
        try:
            user = User.objects.get(email=validated_data["email"])
        except ObjectDoesNotExist:
            user = User.objects.create_user(**validated_data)
            requestObject = self.context.get("request")
            if requestObject:
                current_site = get_current_site(requestObject)
                t = threading.Thread(
                    target=send_activation_email, args=(current_site.domain, user.pk)
                )
                t.start()
        return user


class LoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data["user"] = UserSerializer(self.user).data
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data


class WorkspaceSerializer(serializers.ModelSerializer):
    forms = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Workspace
        fields = "__all__"

    def create(self, validated_data):
        return Workspace.objects.create(**validated_data)


class SubmissionSerializer(serializers.ModelSerializer):
    fields = serializers.JSONField(required=False)

    class Meta:
        model = Submission
        fields = "__all__"

    def create(self, validated_data):
        print(validated_data)
        return Submission.objects.create(**validated_data)


class SubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriber
        fields = "__all__"


class FormSerializer(serializers.ModelSerializer):
    workspace = WorkspaceSerializer(required=False)

    class Meta:
        model = Form
        fields = "__all__"
        depth = 1

    def create(self, validated_data):
        validated_data = self.update_validated_data(validated_data)
        return Form.objects.create(**validated_data)

    def update_validated_data(self, validated_data):
        workspace = validated_data.pop("workspace")
        workspaceId = workspace.get("id")
        workspaceObject = Workspace.objects.get(id=workspaceId)
        validated_data["workspace"] = workspaceObject
        return validated_data


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
