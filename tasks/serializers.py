from rest_framework import serializers
from .models import Task
from django.contrib.auth import get_user_model
from datetime import date


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'due_date']

    def validate_due_date(self, value):
        if value < date.today():
            raise serializers.ValidationError('Due date cannot be in the past')
        return value


class UserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField(required=False, allow_blank=True)

    def validate_username(self, value):
        if not value:
            raise serializers.ValidationError('username is required')
        return value


class TaskWithUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'due_date', 'user']

    def validate_due_date(self, value):
        if value < date.today():
            raise serializers.ValidationError('Due date cannot be in the past')
        return value

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        User = get_user_model()
        user, _ = User.objects.get_or_create(username=user_data.get(
            'username'), defaults={'email': user_data.get('email', '')})
        task = Task.objects.create(user=user, **validated_data)
        return task
