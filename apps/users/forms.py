import re


from django import forms
from django.core.validators import RegexValidator  # 导入正则匹配的组件
from django.contrib.auth.hashers import check_password


from .models import Users

# 方法一RegisterForm
class RegisterForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=20, min_length=6,
                               validators=[RegexValidator(r'^[a-zA-Z]\w{5,19}$', "用户名必须字母开头")],
                               error_messages={
                                   'max_length': '用户名长度为6-20位',
                                   'min_length': '用户名长度为6-20位',
                                   'required': '用户名长度为6-20位',
                               })
    password = forms.CharField(label='密码', max_length=20, min_length=6,
                               error_messages={"min_length": "密码长度要大于6",
                                               "max_length": "密码长度要小于20",
                                               "required": "密码不能为空"},
                               )
    password_repeat = forms.CharField(label='确认密码', max_length=20, min_length=6,
                                      error_messages={"min_length": "密码长度要大于6",
                                                      "max_length": "密码长度要小于20",
                                                      "required": "确认密码不能为空"}
                                      )

    mobile = forms.CharField(label='手机号', max_length=11, min_length=11,
                             validators=[RegexValidator(r'^1[3-9]\d{9}$', "手机号格式不正确")],
                             error_messages={"min_length": "手机号长度有误",
                                             "max_length": "手机号长度有误",
                                             "required": "手机号不能为空"})
    
    email = forms.EmailField(label='邮箱')


    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_repeat = cleaned_data.get("password_repeat")
        if password != password_repeat:
            raise forms.ValidationError('2次输入密码不一致')




# 方法二（推荐）
class UsersForm(forms.ModelForm):
    """模型表单，通过数据库对字段的定义，校验数据"""
    password_repeat = forms.CharField(label='确认密码', max_length=20, min_length=6, required=True,
                                      error_messages={"min_length": "密码长度要大于6",
                                                      "max_length": "密码长度要小于20",
                                                      "required": "确认密码不能为空"}
                                      )

    class Meta:
        model = Users
        fields = ['username', 'password', 'mobile']
        # __all__校验所有字段，exclude不校验哪些字段，搭配使用
        # fields = '__all__'
        # exclude = ['first_name', 'date_joined', 'last_name']

    # 用户名校验
    def clean_username(self):
        # 获取用户名对象
        username = self.cleaned_data.get('username')
        # 用户名必须字母开头，6-20位字符，result为None或者username
        result = re.match(r'^[a-zA-Z]\w{5,19}$', username)
        if not result:
            raise forms.ValidationError('用户名必须字母开头')
        return username


class LoginForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=20, min_length=6,
                               validators=[RegexValidator(r'^[a-zA-Z]\w{5,19}$', "用户名必须字母开头")],
                               error_messages={'max_length': '用户名长度为6-20位',
                                               'min_length': '用户名长度为6-20位',
                                               'required': '用户名长度为6-20位'})

    password = forms.CharField(label='密码', max_length=20, min_length=6,
                               error_messages={"min_length": "密码长度要大于6",
                                               "max_length": "密码长度要小于20",
                                               "required": "密码不能为空"})

    # def clean_user_pwd(self):
    #     username = self.cleaned_data.get('username')
    #     password = self.cleaned_data.get('password')
    #     # 从数据库查询用户名
    #     # if not Users.objects.filter(username=username).exists():
    #     real_pwd = Users.objects.filter(username=username).first()
    #     if not real_pwd:
    #         raise forms.ValidationError('{}用户名不存在'.format(username))
    #     # 从数据库查询真实密码
    #     if not check_password(password, real_pwd.password):
    #         raise forms.ValidationError('密码输入错误')
    #     return username






