from django.urls import path,re_path
from . import views

app_name = 'verifications'
urlpatterns = [
    # path('image_codes/', views.ImageCode.as_view(), name='image_code'),
    path('image_codes/<uuid:image_code_id>/', views.ImageCode.as_view(), name='image_codes'),
    re_path('username/(?P<username>\w{5,20})/', views.UsernameView.as_view(), name='username'),
    re_path('mobiles/(?P<mobile>1[3-9]\d{9})/', views.MobileView.as_view(), name='mobiles'),
    path('send/',views.send)
]
