from rest_framework.serializers import ModelSerializer
from .models import User, Addr


class UserSerializers(ModelSerializer):
    """用户序列化器"""

    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {
            'password': {'write_only': True}
        }


class AddrSerializers(ModelSerializer):
    """收货地址序列化器"""

    class Meta:
        model = Addr
        fields = "__all__"
