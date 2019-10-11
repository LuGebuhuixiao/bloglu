from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'
    # admin站点显示中文
    verbose_name = '用户操作'
