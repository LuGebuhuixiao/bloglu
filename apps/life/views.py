from django.shortcuts import render
from django.views import View
from django.http import JsonResponse

from life.forms import BlogForm
from .models import Message as Mes, Comment


def about(request):
    return render(request, 'aboutme.html')

def time(request):
    return render(request, 'time.html')


class Message(View):
    def get(self,request):
        # 评论表单
        blog_form = BlogForm()
        message = Mes.objects.all()
        return render(request, 'message.html', {'blog_form': blog_form, 'message':message})

    def post(self, request):
        blog_form = BlogForm(request.POST)
        if blog_form.is_valid():
            username = request.POST.get('username')
            content = request.POST.get('content')

            Mes.objects.create(username=username, content=content)
            message = Mes.objects.all()
            blog_form = BlogForm()
            return render(request, 'message.html', {'blog_form': blog_form, 'message':message})


