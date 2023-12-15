from rest_framework.viewsets import ModelViewSet
from .models import Product, Carousel, Category
from .serializers import ProductSerializers, CategorySerializers, CarouselSerializers
from utils.pagenumberpagination import LargeResultsSetPagination


# Create your views here.


class BaseModelViewSet(ModelViewSet):
    pagination_class = LargeResultsSetPagination


class ProductViewSet(BaseModelViewSet):
    """商品视图"""

    queryset = Product.objects.all()
    serializer_class = ProductSerializers


class CarouselViewSet(BaseModelViewSet):
    """轮播图视图"""

    queryset = Carousel.objects.all()
    serializer_class = CarouselSerializers


class CategoryViewSet(BaseModelViewSet):
    """商品分类视图"""

    queryset = Category.objects.all()
    serializer_class = CategorySerializers
