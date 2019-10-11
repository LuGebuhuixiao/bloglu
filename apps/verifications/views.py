import logging
from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, JsonResponse
from django_redis import get_redis_connection
from django.conf import settings
from django.core.mail import send_mail

from utils.captcha.captcha import captcha
from users.models import Users
from utils.json_fun import to_json_data

logger = logging.getLogger('django')
class ImageCode(View):
    """图片验证码缓存到redis"""
    def get(self, request, image_code_id):
        text, image = captcha.generate_captcha()
        conn_redis = get_redis_connection('verify_codes')  # 连接到redis数据库
        conn_redis.setex('img_{}'.format(image_code_id), 300, text)  # 设置图片验证码过期时间

        logger.info('图片验证码:{}'.format(text))
        return HttpResponse(content=image, content_type='image/jpg')


class UsernameView(View):
    """用户名校验"""
    def get(self, request, username):
        # 1、创建对象接受js前端数据
        count = Users.objects.filter(username=username).count()
        data = {'name': username, 'count': count}
        # 2、数据库查询count()
        # (1)count = 0用户名可以使用
        # (2)count = 1用户名已存在
        # 3、返回数据给js前端
        # return to_json_data(data=data)
        return JsonResponse({'data': data})

    def post(self):
        pass


class MobileView(View):
    """手机号校验"""
    def get(self, request, mobile):
        count = Users.objects.filter(mobile=mobile).count()
        data = {'mobile': mobile, 'count': count}
        return to_json_data(data=data)


class Register(View):
    def post(self, request):
        pass


def send(message, email):
    """message:邮件内容；
    email：收件人邮箱"""
    msg='<a href="http://www.itcast.cn/subject/pythonzly/index.shtml" target="_blank">点击激活</a>'
    # 邮件主题
    subject = '这是来自bloglu的邮件'
    # 邮件内容
    message = '邮件正文'
    # 发件人
    sender = settings.EMAIL_FROM
    # 收件人
    # receiver = [email]
    send_mail(subject,message,sender,
              ['w15971466561@163.com'],
              )
    return HttpResponse('ok')