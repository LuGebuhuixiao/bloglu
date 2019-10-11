from article.models import Tag, Category, BigCategory,Article,Banner


# 全局变量
def all_template(request):
    tags = Tag.objects.all()
    nodes = BigCategory.objects.all()
    view_articles = Article.objects.all().order_by('-views')[:5]
    banners = Banner.objects.all()
    love_articles = Article.objects.all().order_by('-loves')[:3]
    # for node in nodes:
    #     node.category_set.
    context = {'nodes': nodes, 'tags': tags,'view_articles': view_articles, 'love_articles': love_articles,'banners': banners}
    return context
