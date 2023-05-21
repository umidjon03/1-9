from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'firstname', 'username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}, # no need to read password
            #'email': {'read_only': True}
        }