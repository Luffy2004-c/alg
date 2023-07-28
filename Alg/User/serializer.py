from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):  # 用户模型序列化器
    class Meta:
        model = User
        fields = "__all__"
