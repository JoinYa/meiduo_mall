from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from apps.users.models import User
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from .serializers import UserSerializers
from utils.pagenumberpagination import LargeResultsSetPagination
from rest_framework_simplejwt.views import TokenObtainPairView
from common.permissions import Userpermission
from rest_framework.decorators import action


# Create your views here.
class ModelViewSetBase(ModelViewSet):
    pagination_class = LargeResultsSetPagination


class UserViewSet(ModelViewSetBase):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    permission_classes = [IsAuthenticated, Userpermission]

    # @action(methods=['post'], detail=False, url_path='upload_avatar')
    def upload_avatar(self, request, pk=None):
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
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        result = serializer.validated_data
        result["id"] = serializer.user.id
        result["mobile"] = serializer.user.mobile
        result["email"] = serializer.user.email
        result["username"] = serializer.user.username
        result["token"] = result.pop("access")
        result["code"] = 0
        result["errmsg"] = "ok"

        return Response(result, status=status.HTTP_200_OK)
