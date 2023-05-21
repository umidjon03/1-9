from django.urls import path
from .views import SignUpView, SignInView, SignOutView

urlpatterns = [
    path('sign-up', SignUpView.as_view(), name='signup'),
    path('sign-in', SignInView.as_view(), name='signin'),
    path('sign-out', SignOutView.as_view(), name='signout'),
]