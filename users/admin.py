from django.contrib import admin

from .models import User, Token

@admin.register(User)
class UsersCustom(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'password')
    fields = ('id', 'username', 'email', 'password')


@admin.register(Token)
class Tokens(admin.ModelAdmin):
    list_display = ('key', 'user')
    fields = ('key', 'user')
