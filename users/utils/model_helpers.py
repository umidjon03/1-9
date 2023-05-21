import os
import binascii
from datetime import timedelta
from django.utils import timezone


def token_generate():
    return binascii.hexlify(os.urandom(20)).decode()

def expires_default():
    return timezone.now() + timedelta(days=30)