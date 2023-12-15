from apps.goods import views
from rest_framework.routers import DefaultRouter

urlpatterns = [
]

# 可以处理视图的路由器
router = DefaultRouter()
# 向路由器中注册视图集
router.register(r'products', views.ProductViewSet, basename='product')
router.register(r'categorys', views.CategoryViewSet, basename='category')
router.register(r'carousels', views.CarouselViewSet, basename='carousels')
# 追加路由
urlpatterns += router.urls
