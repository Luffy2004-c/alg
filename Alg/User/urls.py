from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from User.views import *

urlpatterns = [
    # 登录
    path("login/", LoginView.as_view()),
    # 注册
    path("register/", RegisterView.as_view({"post": "create"})),
    # 刷新token
    path("token/refresh/", TokenRefreshView.as_view()),
    # 校验token
    path("token/verify/", TokenVerifyView.as_view()),
    # 获取用户信息
    path("user/<int:pk>/", UserView.as_view({"get": "retrieve"})),
    # 用户上传头像
    path("<int:pk>/avatar/upload/", UserView.as_view({"post": "upload_avatar"})),
    # 获取用户头像
    path("<int:pk>/avatar/get/", UserView.as_view({"get": "avatar_get"})),
]
