from typing_extensions import Required
from django.db.models.aggregates import Max
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
        return User.objects.create_user(**validated_data)


class WorkspaceSerializer(serializers.ModelSerializer):
    forms = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Workspace
        fields = "__all__"

    def create(self, validated_data):
        return Workspace.objects.create(**validated_data)


class FormSerializer(serializers.ModelSerializer):
    submissions = serializers.StringRelatedField(many=True, required=False)
    # subscribers = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Form
        fields = "__all__"


class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = "__all__"


class SubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriber
        fields = "__all__"
