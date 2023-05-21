from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

from users.utils.model_helpers import token_generate, expires_default

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        user = self.model(username=username, email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    firstname = models.CharField(max_length=50, blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email'] # email is required

    objects = UserManager()

    class Meta:
        db_table = 'user_users'
    

class Token(models.Model):
    key = models.CharField(max_length=40, unique=True)
    user = models.ForeignKey(User, models.CASCADE, related_name='tokens')
    is_active = models.BooleanField(default=True)
    expires_at = models.DateTimeField(default=expires_default)  # token expires in 30 days

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = token_generate()
        return super(Token, self).save(*args, **kwargs)

    def __str__(self):
        return self.key

    class Meta:
        db_table = 'user_tokens'