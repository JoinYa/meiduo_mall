from django.http import FileResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
import os

from meiduo_mall.settings import MEDIA_ROOT


class FileViewSet(APIView):
    """文件视图类"""

    def get(self, request, file):
        path = os.path.join(MEDIA_ROOT, "image", file)
        if os.path.isfile(path):
            return FileResponse(open(path, 'rb'))
        return Response({'message': '文件不存在'}, status=status.HTTP_404_NOT_FOUND)
