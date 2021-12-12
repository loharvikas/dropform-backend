from django.contrib.sites.shortcuts import get_current_site
from users.email import send_activation_email
from rest_framework import serializers
from workspace.models import Workspace
from users.models import User
from forms.models import Form, Submission
from subscribers.models import Subscriber


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    email = serializers.EmailField(required=False)
    password = serializers.CharField(required=False, write_only=True)
    full_name = serializers.CharField(required=False, max_length=255)
    workspaces = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):
        u = User.objects.create_user(**validated_data)
        print("CONTEXT:", self.context)
        current_site = get_current_site(self.context.get("request"))
        send_activation_email(current_site.domain, u.pk)
        return u


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
