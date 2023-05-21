from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

from users.models import Token
from users.serializers.sign_in import SignInSerializer
from users.serializers.sign_up import SignUpSerializer
from users.utils.responses import sign_in_response

class SignUpView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = SignUpSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            return Response(sign_in_response(user), status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignInView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = SignInSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        return Response(sign_in_response(user), status=status.HTTP_200_OK)


class SignOutView(GenericAPIView):
    def delete(self, request):
        Token.objects.filter(key=request.auth.key, user=request.user).delete()
        return Response()   
