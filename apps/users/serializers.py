from rest_framework.serializers import ModelSerializer
from .models import User, Addr


class UserSerializers(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {
            'password': {'write_only': True}
        }


class AddrSerializers(ModelSerializer):
    class Meta:
        model = Addr
        fields = "__all__"
