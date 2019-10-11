# life/models.py
from django.db import models

from article.models import Article


class Message(models.Model):
    username = models.CharField(max_length=50, verbose_name='昵称')
    content = models.TextField(verbose_name='内容', default='请留下联系方式')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='时间')

    class Meta:
        verbose_name = '留言'
        verbose_name_plural = verbose_name
        ordering = ['-create_date']

    def __str__(self):
        return self.username


class Comment(models.Model):
    """文章评论"""
    nickname = models.CharField(max_length=50, verbose_name='昵称')
    content = models.TextField(verbose_name='内容')
    create_date = models.DateTimeField(auto_now=True, verbose_name='评论时间')
    article = models.ForeignKey(to=Article, on_delete=models.CASCADE, verbose_name='对应的文章')

    class Meta:
        verbose_name = '文章评论'
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.nickname