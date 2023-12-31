from django.db import models
from django.contrib.auth.models import AbstractUser
from common.models import BaseModel


# Create your models here.
class User(AbstractUser, BaseModel):
    """用户模型"""
    email = models.EmailField(verbose_name="邮箱", blank=True, unique=True)
    mobile = models.CharField(verbose_name="手机号", max_length=11, unique=True)
    avatar = models.ImageField(verbose_name="头像", blank=True, null=True, upload_to="image",
                               default="image/default.png")

    class Meta:
        db_table = "tb_user"
        verbose_name = "用户表"
        verbose_name_plural = verbose_name


class Addr(BaseModel):
    """收获地址模型"""
    user = models.ForeignKey(User, verbose_name="用户", on_delete=models.CASCADE)
    name = models.CharField(verbose_name="收货人", max_length=20)
    mobile = models.CharField(verbose_name="手机号", max_length=11)
    province = models.CharField(verbose_name="省份", max_length=20)
    city = models.CharField(verbose_name="城市", max_length=20)
    county = models.CharField(verbose_name="区县", max_length=20)
    address = models.CharField(verbose_name="详细地址", max_length=100)
    is_default = models.BooleanField(verbose_name="是否默认地址", default=False)

    class Meta:
        db_table = "tb_addr"
        verbose_name = "收获地址表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user


class Area(BaseModel):
    """省市县区域模型"""
    pid = models.IntegerField(verbose_name="父级id")
    name = models.CharField(verbose_name="区域名称", max_length=20)
    level = models.CharField(verbose_name="区域等级", max_length=20)

    class Meta:
        db_table = "tb_area"
        verbose_name = "区域表"
        verbose_name_plural = verbose_name

