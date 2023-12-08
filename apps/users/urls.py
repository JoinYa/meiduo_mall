from django.urls import path
from apps.users.views import UserInfoView

urlpatterns = [
    path('usernames/<username>/count/', UserInfoView.as_view()),
]