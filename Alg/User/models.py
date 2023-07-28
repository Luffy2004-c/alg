from django.db import models

# django中自带的用户模型
from django.contrib.auth.models import AbstractUser
from utils.generate_bv_code import enc
from common.db import BaseModel

# Create your models here.


class User(BaseModel, AbstractUser):  # username,email,password,id从AbstractUser继承
    """用户模型"""

    # username = models.CharField(
    #     max_length=150,
    #     default="用户",
    #     verbose_name="用户名"

    # ),
    # password = models.CharField(
    #     max_length=32, default=" ", verbose_name="密码")
    # email = models.EmailField(verbose_name="邮箱", default=" ", null=True)
    mobile = models.CharField(
        max_length=11, default=" ", verbose_name="手机号码", null=True
    )
    # ,upload_to='avatar/%Y%m%d/')
    avatar = models.ImageField(verbose_name="用户头像", blank=True, null=True)
    profile = models.TextField(verbose_name="个人简介", default=" ")

    class Meta:
        db_table = "users_table"
        verbose_name = "用户表"

    def __str__(self):
        return self.username

    # def save(self, *args, **kwargs):  # 方法重写，并确保父类方法正常被调用
    #     if not self.pk:  # 如果是新创建的文章
    #         # 生成BV编码，可以使用算法或其他方式自定义
    #         # bv_code = enc(self.pk)
    #         print(self.pk)
    #         self.bv_code = 1
    #     super().save(*args, **kwargs)
