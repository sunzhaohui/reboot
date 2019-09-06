# _*_ encoding:utf-8 _*_
__author__ = 'sunzhaohui'
__date__ = '2019-09-01 11:37'


from reboot.celery import app
from django.core.mail import send_mail

from utils.python_jenkins import JenkinsApi
import traceback
import time

from reboot.settings import EMAIL_FROM


from deploy.models import Deploy

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

def send_deploy_mail_task(pk):
    deploy = Deploy.objects.get(pk=pk)
    title = '代码部署通知'
    name = deploy.name
    version = deploy.version
    status = deploy.status
    status_display = deploy.get_status_display()
    if status <= 1:
        deployer = deploy.reviewer
        start_time = deploy.review_time
    else:
        deployer = deploy.handler
        start_time = deploy.deploy_time
    mark = deploy.version_desc
    url = deploy.build_url
    body = '''
    项目: {}
    版本: {}
    状态: {}
    发布人: {}
    开始时间: {}
    备注: {}
    url: {}
    '''.format(name,version,status_display,deployer,start_time,mark,url)
    print(body)
    to_email_list = ['413108892@qq.com']

    send_mail(subject=title,message=body,from_email=EMAIL_FROM,recipient_list=to_email_list)


@app.task
def build_job_task(name,parameters):
    jenkinsapi = JenkinsApi()
    jenkinsapi.build_job(name,parameters)


@app.task
def check_build_result_task(name,number,pk):
    jenkinsapi = JenkinsApi()

    while True:
        job_exists = jenkinsapi.check_job_number_exists(name,number)
        if job_exists:

            info = jenkinsapi.get_build_info(name,number)
            print(info)
            building_bool = info['building']
            if not building_bool:
                result = info['result']
                if result == 'SUCCESS':
                    deploy = Deploy.objects.get(pk=pk)
                    if deploy.status == 0:
                        deploy.status = 1
                        deploy.save()
                    elif deploy.status == 1:
                        deploy.status = 4
                        deploy.end_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(info['timestamp']/1000))
                        deploy.save()
                    send_deploy_mail_task(pk)
                    #send_mail(deploy.name,deploy.build_url+deploy.get_status_display(),EMAIL_FROM,['413108892@qq.com'])

                    break
                else:
                    deploy = Deploy.objects.get(pk=pk)
                    deploy.status = 5
                    deploy.save()

                    #send_mail(deploy.name, deploy.build_url + deploy.get_status_display(), EMAIL_FROM,['413108892@qq.com'])
                    send_deploy_mail_task(pk)
                    break
            else:
                print(name,number,'正在building')
            time.sleep(1)
            continue
        else:
            time.sleep(1)





