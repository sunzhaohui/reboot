# _*_ encoding:utf-8 _*_
__author__ = 'sunzhaohui'
__date__ = '2019-08-04 14:57'

from django.urls import path,re_path

from . import views
from .group import RoleListView,RolePowerView
from .user import  UserListView,UserDetailView,UserGroupPowerView,ModifyPasswordView,UserView,UserPasswordView
from .power import PowerListView,PowerView



app_name='users'
urlpatterns = [
    #path('login',views.login,name='login'),

    #path("login", views.login, name='login'),
    path('userlist/',UserListView.as_view(),name='user_list'),   #用户列表
    re_path('modifypassword/',ModifyPasswordView.as_view(), name= 'modify_pwd'),  #修改用户密码
    re_path('usergrouppower/(?P<pk>[0-9]+)?/$', UserGroupPowerView.as_view(), name='user_group_power'),   #修改用户权限
    re_path('userdetail/(?P<pk>[0-9]+)?/$', UserDetailView.as_view(), name='user_detail'),  #用户详情
    #####################################################################################################
    path('rolelist/',RoleListView.as_view(),name='role_list'),   #角色列表
    re_path('rolepower/(?P<pk>[0-9]+)?/$', RolePowerView.as_view(), name='role_power'),   #修改角色权限
    ######################################################################################################
    path('powerlist/',PowerListView.as_view(),name='power_list'),   # 权限列表
    re_path('modifypower/(?P<pk>[0-9]+)?/$',PowerView.as_view(),name='modify_power'),
    ######################################################################################################
    path('user/', UserView.as_view(), name='user'),  # 用户中心
    path('userpassword/',UserPasswordView.as_view(),name='userpassword'),

    # http://ip:8000/
    path("", views.IndexView.as_view(), name='index'),
    # http://ip:8000/login/
    path("login/", views.LoginView.as_view(), name='login'),
    # http://ip:8000/logout/
    path("logout/", views.LogoutView.as_view(), name='logout'),
    #re_path('hello/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/',views.index,name='index'),
    ]