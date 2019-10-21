# _*_ encoding:utf-8 _*_
__author__ = 'sunzhaohui'
__date__ = '2019-09-26 16:45'

from django.urls import path
from . import views

app_name = 'notice'

urlpatterns = [
    # 通知列表
    # path('unread/', views.CommentNoticeUnreadView.as_view(), name='unread'),
    # 更新通知状态
    path('update/', views.CommentNoticeUpdateView.as_view(), name='update'),
    path('all/',views.CommentNoticeAllView.as_view(),name='all'),
    # path('list/', views.CommentNoticeUnreadView.as_view(), name='unread'),

]