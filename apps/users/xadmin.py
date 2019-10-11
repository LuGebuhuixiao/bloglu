import xadmin
# from django.contrib import admin
from users.models import Users

# Register your models here.
from xadmin import views

# xadmin.site.register(Users)


# 主题设置
class BaseSetting(object):
    # 开启主题功能
    enable_themes = True
    # 使用Bootstrap主题样式库
    use_bootswatch = True


# 后台管理系统全局设置
class GlobalSetting(object):
    # 左上角标题
    site_title = '博客后台管理'
    # 页尾
    site_footer = '路远的博客'
    # 菜单风格-->可伸缩菜单， 默认为全部显示，不可伸缩
    # menu_style = 'accordion'


xadmin.site.register(views.CommAdminView, GlobalSetting)
xadmin.site.register(views.BaseAdminView, BaseSetting)


