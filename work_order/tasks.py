# _*_ encoding:utf-8 _*_
__author__ = 'sunzhaohui'
__date__ = '2019-09-01 11:37'


from reboot.celery import app
from django.core.mail import send_mail



import traceback
import time

@app.task
def hello(name):
    time.sleep(10)
    print('hello {}!'.format(name))
    return 'hello {}!'.format(name)




@app.task
def task_send_mail(title,order_contents,EMAIL_FROM,to_email_list ):


    send_mail(title,
                              order_contents,
                              EMAIL_FROM,
                              to_email_list,
                              fail_silently=False
                               )