from django.db import models
from common.models import BaseModel


# Create your models here.
class Category(BaseModel):
    """商品分类模型"""
    name = models.CharField(verbose_name="分类名", max_length=100)

    class Meta:
        db_table = "tb_category"
        verbose_name = "商品分类表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Product(BaseModel):
    """商品模型"""
    name = models.CharField(verbose_name="商品名", max_length=255)
    image = models.ImageField(verbose_name="商品图片", blank=True, null=True)
    description = models.TextField(verbose_name="商品描述")
    price = models.DecimalField(verbose_name="商品价格", max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, verbose_name="商品分类", on_delete=models.CASCADE)
    stock = models.IntegerField(verbose_name="库存", default=1)
    sales = models.IntegerField(verbose_name="销量", default=0)
    is_on = models.BooleanField(verbose_name="是否上架", default=True)
    recommend = models.BooleanField(verbose_name="是否推荐", default=False)


    class Meta:
        db_table = "tb_product"
        verbose_name = "商品表"
        verbose_name_plural = verbose_name


class Carousel(BaseModel):
    """轮播图模型"""
    title = models.CharField(verbose_name="轮播图名称", max_length=100)
    image = models.ImageField(verbose_name="轮播图", blank=True, null=True, upload_to="image")

    class Meta:
        db_table = "tb_carousel"
        verbose_name = "轮播图表"
        verbose_name_plural = verbose_name
