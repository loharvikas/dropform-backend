from enum import unique
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.models import update_last_login
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.contrib.auth import get_user_model

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.email import send_activation_email
from workspace.models import Workspace
from forms.models import Form, Submission
from subscribers.models import Subscriber

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
    workspaces = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "password",
            "full_name" "is_active",
            "date_joined",
            "last_modified_date",
        ]


class RegisterSerializer(UserSerializer):
    full_name = serializers.CharField(max_length=255, required=True)
    password = serializers.CharField(max_length=255, required=True, write_only=True)
    email = serializers.EmailField(
        max_length=255,
        required=True,
        write_only=True,
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
            "date_joined",
            "last_modified_date",
        ]

    def create(self, validated_data):
        try:
            user = User.objects.get(email=validated_data["email"])
        except ObjectDoesNotExist:
            user = User.objects.create_user(**validated_data)
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
    submissions = SubmissionSerializer(many=True, read_only=True)
    subscribers = SubmissionSerializer(many=True, read_only=True)

    class Meta:
        model = Form
        fields = "__all__"
        # depth = 1
