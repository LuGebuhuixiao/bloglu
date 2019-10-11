import random, logging

from django.contrib.auth import logout, login, authenticate
from django.db.models import Q
from django.shortcuts import render, redirect, reverse
from django.views import View
from django.contrib.auth.hashers import check_password
from django.http import HttpResponse
from django_redis import get_redis_connection

from utils.json_fun import err_msg
from .forms import RegisterForm, LoginForm
from .models import Users


logger = logging.getLogger('django')
class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        print(request.POST, type(request.POST))
        data_dict = RegisterForm(request.POST)
        if not data_dict.is_valid():
            return render(request, 'register.html', context={'error_msg': err_msg(data_dict)})
        username = data_dict.cleaned_data.get('username')
        password = data_dict.cleaned_data.get('password')
        mobile = data_dict.cleaned_data.get('mobile')
        email = data_dict.cleaned_data.get('email')
        # 校验数据库中是否存在相同字段
        if Users.objects.filter(Q(username=username) | Q(mobile=mobile) | Q(email=email)).exists():
            return render(request, 'register.html', context={'error_msg': '用户名或手机号或邮箱已注册！'})  # 返回错误信息

        # # 生成6位短信验证码
        # sms_num = '{:06d}'.format(random.randint(0, 999999))
        # # 构建外键, 连接到redis
        # con_redis = get_redis_connection('verify_codes')
        # # 短信建  5分钟  sms_num
        # sms_text_flag = "sms_{}".format(mobile).encode('utf8')
        # # 过期时间
        # sms_flag_fmt = "sms_flag_{}".format(mobile).encode('utf8')
        # # 存到redis
        # con_redis.setex(sms_text_flag, 300, sms_num)
        # con_redis.setex(sms_flag_fmt, 60, 1)  # 邮箱验证码过期时间
        # # 发送邮箱验证码
        # logger.info('邮箱验证码:{}'.format(sms_num))
        # 注册
        user = Users.objects.create_user(username=username, mobile=mobile, password=password, email=email)

        if not user:
            return render(request, 'register.html', context={'error_msg': '注册失败，请重新填写'})
        return render(request, 'login.html')


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        data_dict = LoginForm(request.POST)
        if not data_dict.is_valid():
            return render(request, 'login.html', context={'errors': err_msg(data_dict)})
        username = data_dict.cleaned_data.get('username')
        password = data_dict.cleaned_data.get('password')
        # # 方法一（通用）
        # # 从数据库查询用户对象，返回对象或None
        # user = Users.objects.filter(username=username).first()
        # # 校验用户名是否存在，密码是否正确
        # if user and check_password(password, user.password):
        #     # 保存session信息
        #     request.session['username'] = username

        # 方法二，必须用户模型继承AbstractUser
        # 校验用户名，密码，返回用户对象
        user = authenticate(username=username, password=password)
        if not user:
            return render(request, 'login.html', context={'errors': '用户名或密码错误，请重新输入'})
        # 将用户对象保存在底层的request中
        login(request, user=user)
        return redirect(reverse('news:index'))


class LogoutView(View):
    def get(self, request):
        # 方法一（通用）
        # request.session.flush()
        logout(request)
        return render(request, 'login.html')

