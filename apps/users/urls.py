from apps.users import views
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('login/', views.LoginViewSet.as_view()),
    path('register/', views.RegisterViewSet.as_view()),
    # 刷新token
    path('token/refresh/', TokenRefreshView.as_view()),
    # 校验token
    path('token/verify/', TokenVerifyView.as_view()),
    # 上传头像
    path('<int:pk>/upload_avatar/', views.UserViewSet.as_view({"post": "upload_avatar"})),
    # 发送短信验证码
    path('verifcodes/send_verifcode/', views.SendVerifCodeViewSet.as_view()),
    # 验证短信验证码
    path('verifcodes/check_verifcode/', views.CheckSendVerifCodeViewSet.as_view())
]

# 可以处理视图的路由器
router = DefaultRouter()
# 向路由器中注册视图集
router.register(r'users', views.UserViewSet, basename='user')
router.register(r'addrs', views.AddrViewSet, basename='addr')
# 追加路由
urlpatterns += router.urls
