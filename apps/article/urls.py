from django.urls import path
from . import views


app_name = 'article'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('info/', views.InfoView.as_view(), name='info'),
    path('study/<name>', views.StudyView.as_view(), name='study'),
]

