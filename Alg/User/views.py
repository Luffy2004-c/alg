from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework.viewsets import ViewSet, GenericViewSet
from User.models import *
import re
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser
from rest_framework.mixins import *
from .serializer import *
from rest_framework.permissions import IsAuthenticated
from .permission import Userpermission
from common.file_upload import *


class RegisterView(ViewSet):  # 注册视图
    def create(self, request):
        # 接受参数
        username = request.data.get("username")
        password = request.data.get("password")
        email = request.data.get("email")
        password_comfirm = request.data.get("password_comfirm")
        # 校验是否为空
        if not all([username, password, email, password_comfirm]):
            return Response(
                {"error": "字段不能为空"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
        # 校验是否已注册
        if User.objects.filter(username=username).exists():
            return Response(
                {"error": "用户名已存在"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
        # 检验密码是否一致
        if password != password_comfirm:
            return Response(
                {"error": "两次输入的密码不一致"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
        # 校验密码长度
        if not 6 < len(password) < 18:
            return Response(
                {"error": "密码长必须为6-18位"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
        # 校验邮箱格式
        if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
            return Response(
                {"error": "邮箱格式不正确"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
        user = User.objects.create_user(
            username=username, password=password, email=email
        )
        res = {"id": user.id, "username": user.username, "email": user.email}
        return Response(res, status=status.HTTP_201_CREATED)


class LoginView(TokenObtainPairView):  # 登录视图
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        # 自定义登录成功的返回结果
        result = serializer.validated_data
        result["email"] = serializer.user.email

        return Response(result, status=status.HTTP_200_OK)


class UserAvatarUploadAPIView(APIView):
    parser_classes = [FileUploadParser]

    def post(self, request, format=None):
        avatar_file = request.FILES["avatar"]
        file_name = "avatars/" + avatar_file.name  # 保存到 COS 指定文件夹下
        request.user.avatar.save(file_name, avatar_file)

        return Response({"message": "头像上传成功"})


class UserView(GenericViewSet, RetrieveModelMixin):  # 获取用户信息
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # 设置认证用户才有权限访问
    permission_classes = [IsAuthenticated, Userpermission]

    def upload_avatar(self, request, *arsg, **kwargs):  # 上传用户头像
        user = self.get_object()
        avatar = request.data.get("avatar")
        print(type(avatar))
        if not avatar:
            return Response({"message": "上传失败1"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            filetype = avatar.name.rsplit(".")[-1]  # 获取文件后缀
            avatar.name = (
                "{}".format(user.username) + "_avatar" + ".{}".format(filetype)
            )
            serializers = self.get_serializer(
                user, data={"avatar": avatar}, partial=True
            )  # 只对部分字段校验
            print(serializers.is_valid())
            if serializers.is_valid():
                serializers.save()
                upload_obj_avatar(user, avatar)
                return Response(
                    {"message": "上传成功", "filename": avatar.name},
                    status=status.HTTP_200_OK,
                )
            else:
                print(serializers.errors)
                return Response(
                    {"message": "上传失败！"}, status=status.HTTP_400_BAD_REQUEST
                )

    # def get_avatars(self, request, *args, **kwargs):  # 获取用户头像
    #     user = self.get_object()
    #     avatar = get_avatar(user)
    #     return
    #     if not avatar:
    #         return Response({"error": "用户没有上传头像"}, status=status.HTTP_404_NOT_FOUND)
    #     else:
    #         file_prefix = "{}".format(user.username) + "_avatar"  # 获取文件前缀



