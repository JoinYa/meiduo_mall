import os
from django.http import FileResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from apps.users.models import User, Addr
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView

from meiduo_mall.settings import MEDIA_ROOT
from .serializers import UserSerializers, AddrSerializers
from utils.pagenumberpagination import LargeResultsSetPagination
from rest_framework_simplejwt.views import TokenObtainPairView
from common.permissions import BasePermission
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
import random
import string
import redis
from rest_framework.decorators import action


# Create your views here.
class BaseModelViewSet(ModelViewSet):
    pagination_class = LargeResultsSetPagination
    permission_classes = [IsAuthenticated, BasePermission]

    def update(self, request, *args, **kwargs):
        kwargs["partial"] = request.data.get("partial", False)
        return super().update(request, *args, **kwargs)


class UserViewSet(BaseModelViewSet):
    """用户视图"""
    queryset = User.objects.all()
    serializer_class = UserSerializers
    search_fields = ['username']

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(username=request.user)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def upload_avatar(self, request):
        """上传用户头像"""
        avatar = request.data.get("avatar")
        instance = self.get_object()
        serializer = self.get_serializer(instance, data={"avatar": avatar}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"url": serializer.data["avatar"]})


class RegisterViewSet(APIView):
    """注册"""

    def post(self, request):
        data = request.data
        username = data.get("username")
        password = data.get("password")
        mobile = data.get("mobile")
        email = data.get("email")
        password_confirmtion = data.get("password_confirmtion")

        if not all([username, password, mobile, email, password_confirmtion]):
            return Response({"message": "参数不完整"}, status=status.HTTP_400_BAD_REQUEST)
        if password != password_confirmtion:
            return Response({"message": "两次密码不一致"}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(username=username).exists():
            return Response({"message": "用户名已存在"}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create(username=username, mobile=mobile, email=email)
        user.set_password(password)
        user.save()
        return Response({"message": "注册成功"}, status=status.HTTP_201_CREATED)


class LoginViewSet(TokenObtainPairView):
    """登录"""

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"request": request})

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        result = serializer.validated_data
        result["id"] = serializer.user.id
        result["mobile"] = serializer.user.mobile
        result["email"] = serializer.user.email
        result["username"] = serializer.user.username
        result["avatar"] = "media\image\logo5_922SRQ9.png"
        result["token"] = result.pop("access")
        result["code"] = 0
        result["errmsg"] = "ok"

        return Response(result, status=status.HTTP_200_OK)


class AddrViewSet(BaseModelViewSet):
    """收获地址视图"""
    queryset = Addr.objects.all()
    serializer_class = AddrSerializers

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(user=request.user)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        if request.data.get("partial", False) and self.queryset.filter(is_default=True).exists():
            # 如果已存在默认地址，先取消其默认状态
            self.queryset.filter(is_default=True).update(is_default=False)
        return super(AddrViewSet, self).update(request, *args, **kwargs)


class SendVerifCodeViewSet(APIView):
    """生成验证码"""
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get_random_code(self):
        """生成随机验证码"""
        return ''.join(random.choice(string.digits) for i in range(6))

    def post(self, request):

        mobile = request.data.get("mobile")
        code = self.get_random_code()

        try:
            rs = redis.Redis(host='localhost', port=6379, db=2)
        except Exception as e:
            return Response({"message": "数据库连接失败！"}, status=status.HTTP_404_NOT_FOUND)

        result = rs.set(mobile, code, 60 * 5)
        if result:
            return Response({"message": "发送成功！"}, status=status.HTTP_200_OK)


class CheckSendVerifCodeViewSet(APIView):
    """验证验证码"""

    def post(self, request):
        mobile = request.data.get("mobile")
        code = request.data.get("code")
        try:
            rs = redis.Redis(host='localhost', port=6379, db=2)
        except Exception as e:
            return Response({"message": "数据库连接失败！"}, status=status.HTTP_404_NOT_FOUND)

        returns = rs.get(mobile)
        if not returns:
            return Response({"message": "验证码已过期！"}, status=status.HTTP_404_NOT_FOUND)
        if returns.decode() != code:
            return Response({"message": "无效验证码！"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"message": "验证通过！"}, status=status.HTTP_200_OK)
