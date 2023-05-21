import re

from rest_framework import serializers

from users.serializers.user import UserSerializer
from users.models import User


class SignUpSerializer(UserSerializer):

    def validate_password(self, value):
        min_length = 8
        if len(value) < min_length:
            raise serializers.ValidationError(
                f"Password should be at least {min_length} characters long."
            )
        
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError("Password must contain an uppercase letter.")

        if not re.search(r'[a-z]', value):
            raise serializers.ValidationError("Password must contain a lowercase letter.")
        
        if not re.search(r'[^a-zA-Z0-9]', value):
            raise serializers.ValidationError("Password must contain a symbol.")

        return value

    def validate_username(self, value):
        if User.objects.filter(username=value.lower()).exists():
            raise serializers.ValidationError("Username already exists.")
        return value

    def validate(self, data):
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("Email is already registered.")
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'].lower(),
            email=validated_data['email'],
            password=validated_data['password']
        )

        return user