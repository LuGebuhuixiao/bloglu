from django.contrib.auth.models import AbstractUser
from django.db import models


class Users(AbstractUser):
    """用户模型类"""
    mobile = models.CharField(max_length=11, unique=True, verbose_name="手机号", help_text="手机号",
                              error_messages={"unique": "此手机号已注册"})
    # 头像
    icon =models.ImageField(upload_to='uploads/%Y/%m/%d')

    class Meta:
        db_table = 'tb_users'  # 指定表名
        verbose_name = '用户表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username