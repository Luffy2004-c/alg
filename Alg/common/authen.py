'''自定义用户认证'''
'''实现多字段认证'''




from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from User.models import User
from rest_framework import serializers
class MyBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(
                email=username) | Q(mobile=username))
        except:
            raise serializers.ValidationError({"error": "用户不存在"})
        else:
            if user.check_password(password):
                return user
            else:
                raise serializers.ValidationError({"error": "密码错误"})
