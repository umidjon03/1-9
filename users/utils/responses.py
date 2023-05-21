from users.models import Token
from users.serializers.user import UserSerializer


def sign_in_response(user):
    """
    Sends what params needs for logging
    """
    token = Token.objects.create(user=user)
    data = UserSerializer(user).data
    return dict(token=token.key,  user=data)
