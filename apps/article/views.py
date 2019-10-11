import markdown
from django.core.paginator import Paginator

from django.shortcuts import render, get_object_or_404
from django.views import View

from life.models import Comment
from .models import Article, BigCategory, Category, Banner
from django.http import HttpResponse


# 文章列表
def big_fen_lei(name):
    big_desc = BigCategory.objects.filter(name=name)
    # 查大分类的简介，查到的话，说明点击的是大分类
    if big_desc:
        big_desc = big_desc.first().description
        articles = Article.objects.filter(category__bigcategory__name=name)  # 获得大分类下所有文章
    else:
        articles = Article.objects.filter(category__name=name)  # 获得小分类下所有文章
        big_desc = BigCategory.objects.filter(category__name=name)
        if not big_desc:
            return get_object_or_404(BigCategory, name=name)
        big_desc = big_desc.first().description
    context = {'articles': articles, 'name': name, 'big_desc': big_desc}
    return context


# 分页功能
def page_func(articles, page):
    paginator = Paginator(articles, 10)  # 文章分页对象，第二个参数是每页展示的文章数
    contacts = paginator.get_page(page)  # 当前页面对象
    page = contacts.number  # 当前在第几页

    page_list = [i for i in range(1, paginator.num_pages + 1)]  # 总页面个数列表
    page_paginator = Paginator(page_list, 5)  # 页数分页对象
    # 找到当前页面所在页数分页对象的列表，实现分页功能
    for i in range(1, page_paginator.num_pages + 1):
        page_contacts = page_paginator.get_page(i)
        if page in page_contacts.object_list:
            context = {'contacts': contacts, 'page_contacts': page_contacts, }
            return context


# 主页功能完成
class IndexView(View):
    def get(self, request):
        page = request.GET.get('page')

        # 文章列表list
        articles = Article.objects.all().order_by('-update_date')
        paginator = Paginator(articles, 10)  # 文章分页对象，第二个参数是每页展示的文章数
        contacts = paginator.get_page(page)
        return render(request, 'index.html', context={'articles': articles,})


# 文章详情页完成
class InfoView(View):
    def get(self, request):
        id = request.GET.get('id')
        article = get_object_or_404(Article, id=id)
        # id = request.GET.get('id')
        # article = Article.objects.get(id=id)
        bigcategory = Category.objects.get(name=article.category).bigcategory
        article.update_views()  # 浏览量+1

        comments = article.comment_set.all()
        return render(request, 'info.html', {'article': article, 'bigcategory': bigcategory, 'comments': comments})

    def post(self, request):
        id = request.GET.get('id')
        article = get_object_or_404(Article, id=id)
        nickname = request.POST.get('nickname')
        content = request.POST.get('content')
        Comment.objects.create(nickname=nickname, content=content, article_id=id)
        # commet.save()
        bigcategory = Category.objects.get(name=article.category).bigcategory
        comments = article.comment_set.all()
        return render(request, 'info.html', {'article': article, 'bigcategory': bigcategory, 'comments': comments})


# 文章分类页完成
class StudyView(View):
    def get(self, request, name):
        # 返回文章列表，所处大类名字，大类简介
        context = big_fen_lei(name)
        # 获取所在页码数
        page = request.GET.get('page')
        # 分页
        page_context = page_func(context['articles'], page)
        context = dict(context, **page_context)
        return render(request, 'life.html', context=context)


class TagView(View):
    def get(self, request):
        return render(request, 'life.html')
