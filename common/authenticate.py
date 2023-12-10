"""
自定义认证
"""
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from apps.users.models import User
from rest_framework import serializers


class MyBackend(ModelBackend):
    """
    自定义认证后端
    """

    def authenticate(self, username=None, password=None, **kwargs):
        """
        自定义认证
        :param username: 用户名
        :param password: 密码
        :param kwargs: 其他参数
        :return: 返回用户对象
        """
        try:
            user = User.objects.get(Q(username=username) | Q(mobile=username) | Q(email=username))
        except Exception as e:
            raise serializers.ValidationError({"error": "未找到该用户！"})
        else:
            if user.check_password(password):
                return user
            else:
                raise serializers.ValidationError({"error": "密码不正确！"})
