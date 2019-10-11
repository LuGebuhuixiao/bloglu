# Generated by Django 2.1.7 on 2019-10-11 02:57

from django.db import migrations, models
import django.db.models.deletion
import mdeditor.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='文章标题')),
                ('summary', models.TextField(default='文章摘要等同于网页description内容，请务必填写...', max_length=230, verbose_name='文章摘要')),
                ('body', mdeditor.fields.MDTextField(verbose_name='文章内容')),
                ('image', models.ImageField(blank=True, null=True, upload_to='uploads/article/%Y/%m/%d', verbose_name='文章图片')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('views', models.IntegerField(default=0, verbose_name='阅览量')),
                ('loves', models.IntegerField(default=0, verbose_name='喜爱量')),
            ],
            options={
                'verbose_name': '博文',
                'verbose_name_plural': '博文',
                'ordering': ['-create_date'],
            },
        ),
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='逻辑删除')),
                ('image_url', models.ImageField(upload_to='uploads/article/%Y/%m/%d', verbose_name='轮播图')),
                ('priority', models.IntegerField(choices=[(1, '第一级'), (2, '第二级'), (3, '第三级'), (4, '第四级'), (5, '第五级'), (6, '第六级')], default=6, verbose_name='轮播图优先级')),
                ('news', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='article.Article')),
            ],
            options={
                'verbose_name': '轮播图',
                'db_table': 'tb_banner',
                'ordering': ['-update_time', '-id'],
            },
        ),
        migrations.CreateModel(
            name='BigCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='导航分类')),
                ('description', models.TextField(max_length=240, verbose_name='描述')),
            ],
            options={
                'verbose_name': '一级导航',
                'verbose_name_plural': '一级导航',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='文章分类')),
                ('bigcategory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='article.BigCategory', verbose_name='大分类')),
            ],
            options={
                'verbose_name': '二级导航',
                'verbose_name_plural': '二级导航',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='HotNews',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='逻辑删除')),
                ('priority', models.IntegerField(choices=[(1, '第一级'), (2, '第二级'), (3, '第三级')], verbose_name='热门新闻优先级')),
                ('news', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='article.Article')),
            ],
            options={
                'verbose_name': '热门新闻',
                'db_table': 'tb_hot',
                'ordering': ['-update_time', '-id'],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='文章标签')),
                ('number', models.IntegerField(default=1, verbose_name='标签数目')),
            ],
            options={
                'verbose_name': '文章标签',
                'verbose_name_plural': '文章标签',
            },
        ),
    ]
