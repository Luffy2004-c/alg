from django.db import models

# django中自带的用户模型
from django.contrib.auth.models import AbstractUser
from utils.generate_bv_code import enc
from common.db import BaseModel

# Create your models here.


class User(BaseModel, AbstractUser):  # username,email,password,id从AbstractUser继承
    """用户模型"""

    mobile = models.CharField(
        max_length=11, default=" ", verbose_name="手机号码", null=True
    )
    avatar = models.ImageField(verbose_name="用户头像", blank=True, null=True)
    profile = models.TextField(verbose_name="个人简介", default=" ")

    class Meta:
        db_table = "users_table"
        verbose_name = "用户表"

    def __str__(self):
        return self.username

