from rest_framework.serializers import ModelSerializer
from .models import Product, Carousel, Category


class ProductSerializers(ModelSerializer):
    """商品序列化器"""

    class Meta:
        model = Product
        fields = "__all__"


class CarouselSerializers(ModelSerializer):
    """轮播图序列化器"""

    class Meta:
        model = Carousel
        fields = "__all__"


class CategorySerializers(ModelSerializer):
    """商品分类序列化器"""

    class Meta:
        model = Category
        fields = "__all__"
