from rest_framework import serializers
from django.contrib.auth import authenticate
from users.models import User

class SignInSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, trim_whitespace=True)
    password = serializers.CharField(required=True, trim_whitespace=False)

    def validate(self, attrs):
        user = authenticate(
            request=self.context.get('request'),
            username=attrs.get('username').lower(),
            password=attrs.get('password')
        )

        if not user:
            msg = 'Wrong username or password'
            raise serializers.ValidationError({'password': [msg]})
        
        attrs['user'] = user
        return attrs