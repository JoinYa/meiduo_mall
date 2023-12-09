from django.db import models


class BaseModel(models.Model):
    """抽象的模型基类：定义公共的模型字段"""

    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    is_deleted = models.BooleanField(default=False, verbose_name="是否删除")

    class Meta:
        # 声明这是一个抽象模型类，在执行迁移文件时，不会在数据库中生成表
        abstract = True
        verbose_name_plural = "公共字段模型"
        db_table = "BaseTable"
