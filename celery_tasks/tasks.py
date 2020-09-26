#使用celery
from celery import Celery
from django.core.mail import send_mail
from django.conf import settings
import time

#在任务处理者一端加这几句
# import os
# import django
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'JDjangoDemo.settings')
# django.setup()

#创建一个Celery类的实例对象
app = Celery('celery_taskj.tasks',broker='redis://192.168.229.132:6379/8')

#定义任务函数
@app.task
def send_register_active_email(to_email,username,token):
    '''发送激活邮件'''
    #组织邮件信息
    subject = "taskj用户系统欢迎信息"
    message = ""
    sender = settings.EMAIL_FROM
    receiver = [to_email]
    html_message = '<h1>%s,欢迎您成为taskj系统会员<h1>请点击下面链接激活您的账户</br><a href="http://127.0.0.1:8000/user/active/%s">激活</a>' % (
    username, token)
    send_mail(subject, message, sender, receiver, html_message=html_message)
    time.sleep(5)