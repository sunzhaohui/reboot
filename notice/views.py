from django.shortcuts import render, redirect
from django.shortcuts import render,get_object_or_404,Http404
from django.http import HttpResponseRedirect, JsonResponse, QueryDict,HttpResponse
from django.urls import reverse
from django.views.generic import View, ListView, DetailView
from django.db.models import Q
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionDenied
from pure_pagination.mixins import PaginationMixin
import  datetime

from work_order.models import WorkOrder

# Create your views here.




class CommentNoticeAllView(LoginRequiredMixin, ListView):
    """通知列表"""
    # 上下文的名称
    context_object_name = 'notices'
    # 模板位置
    template_name = 'notice/all.html'
    # 登录重定向
    login_url = '/login/'

    # 所有通知的查询集
    def get_queryset(self):
        return self.request.user.notifications.all()



class CommentNoticeReadView(LoginRequiredMixin, ListView):
    """通知列表"""
    # 上下文的名称
    context_object_name = 'notices'
    # 模板位置
    template_name = 'notice/read.html'
    # 登录重定向
    login_url = '/login/'

    # 所有通知的查询集
    def get_queryset(self):
        return self.request.user.notifications.read()



class CommentNoticeUnreadView(LoginRequiredMixin, ListView):
    """通知列表"""
    # 上下文的名称
    context_object_name = 'notices'
    # 模板位置
    template_name = 'notice/unread.html'
    # 登录重定向
    login_url = '/login/'

    # 未读通知的查询集
    def get_queryset(self):
        return self.request.user.notifications.unread()


class CommentNoticeUpdateView(View):
    """更新通知状态"""
    # 处理 get 请求
    def get(self, request):
        # 获取未读消息
        notice_id = request.GET.get('notice_id')
        # 更新单条通知
        if notice_id:
            target_id = request.GET.get('target_id')


            request.user.notifications.get(id=notice_id).mark_as_read()
            # print(work_order)
            target_detail_url = request.user.notifications.get(id=notice_id).target.get_detail_url()
            print(target_detail_url)
            return redirect(target_detail_url)
        # 更新全部通知
        else:
            request.user.notifications.mark_all_as_read()
            return redirect('notice:all')
