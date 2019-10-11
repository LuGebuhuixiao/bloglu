from django.urls import path
from . import views


app_name = 'life'
urlpatterns = [
    path('time/', views.time, name='time'),
    path('about/', views.about, name='about'),
    path('message/', views.Message.as_view(), name='message'),
]

