from django.urls import path,re_path
from apps.user.views import RegisterView,ActiveView,LoginView


app_name = "user"
urlpatterns = [
    path('register/',RegisterView.as_view(),name="register"), #注册
    re_path(r'^active/(.*)$',ActiveView.as_view(),name="active"), #激活用户
    path('login/',LoginView.as_view(),name="login") #登录
]
