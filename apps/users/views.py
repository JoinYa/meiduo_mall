from django.views import View
from django.http import JsonResponse
from apps.users.models import User


# Create your views here.

class UserInfoView(View):
    def get(self, request, username):
        user = User.objects.filter(username=username).count()

        return JsonResponse({"code": 200, "count": user, "errmsg": "OK"})
