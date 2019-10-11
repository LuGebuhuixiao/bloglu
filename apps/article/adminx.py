import xadmin
from article.models import Article, Tag, Category, BigCategory,Banner,HotNews


class ArticleAdmin(object):
    # 字段显示
    list_display = ['id', 'title', 'tags', 'views', 'loves', 'create_date', 'update_date',]
    # 检索
    search_fields = ['context', 'desc',]
    # 可 编辑
    list_editable = ['click_num', 'love_num',]
    # 过滤器
    list_filter = ['id', 'title', 'tags', 'views', 'loves', 'create_date', 'update_date',]


# Register your models here.
xadmin.site.register(Article, ArticleAdmin)
xadmin.site.register(Tag)
xadmin.site.register(BigCategory)
xadmin.site.register(Category)
xadmin.site.register(Banner)
xadmin.site.register(HotNews)

