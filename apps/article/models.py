# article/models.py
import markdown

from users.models import Users
from mdeditor.fields import MDTextField
from django.db import models
from mptt.models import MPTTModel
from django.shortcuts import reverse  # 查找URL
from utils.basemodel import ModelBase


class BigCategory(models.Model):
    # 导航名称
    name = models.CharField(verbose_name='导航分类', max_length=20)
    # 分类栏目页描述
    description = models.TextField(verbose_name='描述', max_length=240, )
    class Meta:  # 元信息
        verbose_name = '一级导航'
        verbose_name_plural = verbose_name  # 复数形式相同

    def __str__(self):
        return self.name


# 导航菜单分类下的下拉菜单分类
class Category(models.Model):
    # 分类名字
    name = models.CharField(verbose_name='文章分类', max_length=20)
    # 导航菜单一对多二级菜单,django2.0后定义外键和一对一关系的时候需要加on_delete选项，此参数为了避免两个表里的数据不一致问题
    bigcategory = models.ForeignKey(to=BigCategory, on_delete=models.CASCADE, verbose_name='大分类')

    class Meta:  # 元信息
        verbose_name = '二级导航'
        verbose_name_plural = verbose_name
        # 默认排序
        ordering = ['name']

    def __str__(self):
        return self.name


# 文章标签
class Tag(models.Model):
    """
    文章标签
    """
    name = models.CharField(verbose_name='文章标签', max_length=20)
    number = models.IntegerField(verbose_name='标签数目', default=1)
    class Meta:
        verbose_name = '文章标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 文章
class Article(models.Model):
    author = models.ForeignKey(to=Users, on_delete=models.CASCADE, verbose_name='作者')
    title = models.CharField(max_length=150, verbose_name='文章标题')
    summary = models.TextField(verbose_name='文章摘要', max_length=230, default='文章摘要等同于网页description内容，请务必填写...')
    # 文章内容（普通字段models.TextField(verbose_name='文章内容')）
    body = MDTextField(verbose_name='文章内容')
    # 图片链接
    image = models.ImageField(blank=True, null=True, verbose_name='文章图片', upload_to='uploads/article/%Y/%m/%d')
    # 自动添加创建时间
    create_date = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    # 自动添加修改时间
    update_date = models.DateTimeField(verbose_name='修改时间', auto_now=True)
    # 浏览点赞整数字段
    views = models.IntegerField(verbose_name='阅览量', default=0)
    loves = models.IntegerField(verbose_name='喜爱量', default=0)
    # 分类一对多文章 #related_name反向查询
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE, verbose_name='文章分类')
    # 标签多对多文章
    tags = models.ManyToManyField(to=Tag, verbose_name='标签')


    class Meta:
        verbose_name = '博文'
        verbose_name_plural = verbose_name
        ordering = ['-create_date']

    def __str__(self):
        return self.title[:20]


    # 将内容markdown
    def body_to_markdown(self):
        return markdown.markdown(self.body, extensions=[
            # 包含 缩写、表格等常用扩展
            'markdown.extensions.extra',
            # 语法高亮扩展
            'markdown.extensions.codehilite',
            # 自动生成目录扩展
            'markdown.extensions.toc',
        ])

    # 点赞+1方法
    def update_loves(self):
        self.loves += 1
        self.save(update_fields=['loves'])  # 更新字段

    # 浏览+1方法
    def update_views(self):
        self.views += 1
        self.save(update_fields=['views'])  # 更新字段

    # 前篇方法：当前小于文章并倒序排列的第一个
    def get_pre(self):
        return Article.objects.filter(id__lt=self.id).order_by('-id').first()

    # 后篇方法：当前大于文章并正序排列的第一个
    def get_next(self):
        return Article.objects.filter(id__gt=self.id).order_by('id').first()

    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        else:
            return '/static/images/article/default.jpg'


class Banner(ModelBase):
    PRI_CHOICES = [
        (1, '第一级'),
        (2, '第二级'),
        (3, '第三级'),
        (4, '第四级'),
        (5, '第五级'),
        (6, '第六级'),
    ]
    image_url = models.ImageField(verbose_name='轮播图', upload_to='uploads/article/%Y/%m/%d')
    priority = models.IntegerField(choices=PRI_CHOICES, default=6, verbose_name='轮播图优先级')
    news = models.OneToOneField('Article', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-update_time', '-id']
        db_table = 'tb_banner'
        verbose_name = '轮播图'

    def __str__(self):
        return '轮播图{}'.format(self.id)


class HotNews(ModelBase):
    PRI_CHOICES = [
        (1, '第一级'),
        (2, '第二级'),
        (3, '第三级'),
    ]
    news = models.OneToOneField('Article', on_delete=models.CASCADE)
    priority = models.IntegerField(choices=PRI_CHOICES, verbose_name='热门新闻优先级')

    class Meta:
        ordering = ['-update_time', '-id']
        db_table = 'tb_hot'
        verbose_name = '热门新闻'

    def __str__(self):
        return '热门新闻{}'.format(self.id)