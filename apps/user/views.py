from django.shortcuts import render,redirect,reverse
from apps.user.models import User
from django.views.generic import View
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired
from django.conf import settings
from django.http import HttpResponse
from celery_tasks.tasks import send_register_active_email
from django.contrib.auth import authenticate,login

class RegisterView(View):
    '''注册'''
    def get(self,request):
        '''显示注册页面'''
        return render(request,'register.html')

    def post(self,request):
        '''进行注册处理'''
        # 接收数据
        username = request.POST.get("user_name")
        password = request.POST.get("pwd")
        email = request.POST.get("email")
        allow = request.POST.get("allow")
        # 进行数据校验
        if not all([username, password, email]):
            # 数据不完整
            return render(request, 'register.html', {'errmsg': '数据不完整'})
        if allow != "on":
            return render(request, 'register.html', {'errmsg': '请同意协议'})

        # 校验用户名是否重复
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            # 用户名不存在
            user = None

        if user:
            # 用户名已经存在
            return render(request, 'register.html', {'errmsg': '用户名已经存在'})

        # 进行业务处理，进行用户注册
        user = User.objects.create_user(username, email, password)
        user.is_active = 0
        user.save()

        #发送激活邮件,包含激活链接 127.0.0.1:8000/user/active/3
        #激活邮件包含用户的身份信息,并对信息进行加密处理
        #加密用户身份信息，生成激活token
        serializer = Serializer(settings.SECRET_KEY,3600)
        info = {'confirm':user.id}
        token = serializer.dumps(info) #bytes
        token = token.decode()

        #发邮件
        send_register_active_email.delay(email,username,token)

        # 返回应答和跳转到首页
        return redirect(reverse('goods:index'))

class ActiveView(View):
    '''激活用户'''
    def get(self,request,token):
        '''进行用户激活'''
        serializer  = Serializer(settings.SECRET_KEY,3600)
        try:
            info = serializer.loads(token)
            #获取待激活用户id
            user_id = info['confirm']
            #根据id获取用户信息
            user = User.objects.get(id=user_id)
            user.is_active = 1
            user.save()
            #跳转到登录页面
            return redirect(reverse('user:login'))
        except SignatureExpired as e:
            #激活链接已过期
            return HttpResponse("激活链接已过期")

class LoginView(View):
    '''登录'''
    def get(self,request):
        '''显示登录页面'''
        #判断是否记住了用户名
        if 'username' in request.COOKIES:
            username = request.COOKIES.get('username')
            checked = 'checked'
        else:
            username = ''
            checked = ''
        return render(request,'login.html',{'username':username,'checked':checked})

    def post(self,request):
        '''登录检验'''
        #接收数据
        username = request.POST.get("user_name")
        password = request.POST.get("pwd")
        #校验数据
        if not all([username,password]):
            return render(request,'login.html',{'errmsg':'数据不完整'})
        #业务处理，校验登录
        user = authenticate(username=username,password=password)
        if user is not None:
            if user.is_active:
                #用户已激活
                login(request,user)

                # 跳转到首页
                response = redirect(reverse('goods:index'))

                #判断是否需要记住用户名
                remember = request.POST.get("remember")
                if remember == "on":
                    #记住用户名
                    response.set_cookie('username',username,max_age=7*24*3600)
                else:
                    response.delete_cookie('username')

                return response

            else:
                #用户未激活
                return render(request,'login.html',{'error':'用户未激活'})
        else:
            return render(request,'login.html',{'error':'用户名或密码错误'})
        #返回应答


#/user/order
class UserInfoView(View):
    '''用户中心-信息页'''
    def get(self,request):
        '''显示'''
        return render(request,'user_center_info.html')

#/user/order
class UserOrderView(View):
    '''用户中心-订单页'''
    def get(self,request):
        return render(request,'user_center_order.html')

#/user/address
class AddressView(View):
    '''用户中心-地址页'''
    def get(self,request):
        '''显示'''
        return render(request,'user_center_site.html')

