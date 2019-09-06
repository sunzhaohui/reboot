# _*_ encoding:utf-8 _*_
__author__ = 'sunzhaohui'
__date__ = '2019-08-27 16:50'

from jenkins import Jenkins
from reboot.settings import JENKINS_URL, JENINS_TOKEN,JENKINS_USERNAME,JENKINS_PASSWORD
import os
import json,time


class JenkinsApi:
    def __init__(self):
        self.url = JENKINS_URL
        #self.token = JENINS_TOKEN
        self.username = JENKINS_USERNAME
        self.password = JENKINS_PASSWORD
        self.server = self.connect()

    def connect(self):
        """
        连接jenkins（实例化jenkins）
        :return:
        """
        server = Jenkins(self.url, self.username,self.password)
        return server

    def get_next_build_number(self, name):
        """
        获取下一次构建号
        :param name: 任务名称(项目名称)
        :return: "int" number
        """
        return self.server.get_job_info(name)['nextBuildNumber']

    def build_job(self, name, parameters=None):
        """
        构建任务
        :param name: "str" 任务名称
        :param parameters: "dict" 参数
        :return: "int" queue number
        """
        return self.server.build_job(name=name, parameters=parameters)

        #eg: server.build_job(name="51reboot", parameters={'tag': "version3.0"})


    def get_build_console_output(self, name, number):
        """
        获取终端输出结果
        :param name: "str" 任务名称
        :param number: "int" 构建号
        :return: "str" 结果
        """
        return self.server.get_build_console_output(name, number)

    def get_job_url(self,name):
        return self.server.get_job_info(name)['url']

    def get_next_build_url(self, name):
        url = self.get_job_url(name)
        number = self.get_next_build_number(name)
        return os.path.join(url,str(number))

    def get_running_builds(self):
        #[{'name': 'reboot', 'number': 66, 'url': 'http://172.33.0.82:8080/job/reboot/66/', 'node': '(master)', 'executor': 1}]
        return self.server.get_running_builds()





    def check_job_number_exists(self,name,number):
        #验证job build序号是否已构建
        last_number = dict(self.server.get_job_info(name))['lastBuild']['number']
        running_list = self.get_running_builds()
        if running_list:
            for i in running_list:
                if name == i['name']:
                    last_number = i['number']
        if  int(last_number) >= number:
            return True
            # 已构建
        else:
            return False
            #未构建

    def get_build_info(self,name, number):

        try:
            return self.server.get_build_info(name,int(number))
        except Exception as e:
            print(e)
            return {'building':True}












