from apps.users import views
from django.urls import path

urlpatterns = [
    path('login/', views.LoginViewSet.as_view()),
    path('register/', views.RegisterViewSet.as_view()),
]

from rest_framework.routers import DefaultRouter

# 可以处理视图的路由器
router = DefaultRouter()
# 向路由器中注册视图集
router.register(r'users', views.UserInfoViewSet, basename='user')
# 追加路由
urlpatterns += router.urls
