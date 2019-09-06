# _*_ encoding:utf-8 _*_
__author__ = 'sunzhaohui'
__date__ = '2019-08-25 15:53'


import gitlab

from reboot.settings import GITLAB_HTTP_URI, GITLAB_TOKEN

#mygitlab
from reboot.settings import EXMAPLE_HTTP_URI,EXMAPLE_TOKEN


#gl = gitlab.Gitlab(GITLAB_HTTP_URI, GITLAB_TOKEN, api_version=4)

#mygitlab
gl = gitlab.Gitlab(EXMAPLE_HTTP_URI, EXMAPLE_TOKEN, api_version=4)


def get_user_projects(request):
    """
    获取gitlab里所有的项目，和登录用户所拥有的项目,以及登录用户所拥有项目的项目成员。本项目只实现用户的项目，不做做组
    :return: []
    """
    user_projects = []
    all_projects = gl.projects.list()
    print(all_projects)
    print(request.user.username)
    print(all_projects)

    # 查出所有项目中包含登录用户的项目,即查出当前用户所有的项目
    for project in all_projects:
        for member in project.members.list():
            if member.username == request.user.username:
            # if member.username == 'zp':

                user_projects.append(project)
    return user_projects


def get_project_versions(project_id):
    project = gl.projects.get(project_id)

    tags = project.tags.list()

    print(tags)
    return tags

def get_project_branchs(project_id):
    project = gl.projects.get(project_id)
    branches = project.branches.list()
    return branches





