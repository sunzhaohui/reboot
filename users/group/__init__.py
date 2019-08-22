# _*_ encoding:utf-8 _*_
__author__ = 'sunzhaohui'
__date__ = '2019-08-05 17:20'

from django.shortcuts import render

from django.http import HttpResponse,QueryDict,HttpResponseRedirect,JsonResponse,Http404
from django.urls import reverse
from django.conf import settings

from users.models import UserProfile
from django.contrib.auth.models import Group
from django.db.models import Q

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from users.forms import RoleProfileForm

from django.contrib.auth.hashers import make_password

from django.views.generic import View,DetailView,ListView
from django.contrib.auth import authenticate, login, logout
# Create your views here.

# 用户认证及权限管理模块导入
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from pure_pagination.mixins import PaginationMixin


class RoleListView(LoginRequiredMixin,PermissionRequiredMixin,PaginationMixin,ListView):
    model = Group
    template_name = "users/rolelist.html"

    context_object_name = "rolelist"
    login_url = '/login/'  # 用户没有通过或者权限不够时跳转的地址，默认是 settings.LOGIN_URL.
    # 把没通过检查的用户重定向到没有 "next page" 的非登录页面时，把它设置为 None ，这样它会在 URL 中移除。
    redirect_field_name = 'redirect_to'
    permission_required = ('users.view_group','users.delete_group','users.add_group','users.change_group')

    #@method_decorator(login_required(login_url='/login/'))
    paginate_by = 2
    keyword = ''

    #搜索
    def get_queryset(self):
        queryset = super(RoleListView, self).get_queryset()
        self.keyword = self.request.GET.get('keyword','').strip()
        print(self.keyword)
        if self.keyword:
            queryset = queryset.filter(Q(name__icontains=self.keyword) )
        return queryset
    #显示搜索关键字
    # def get_context_data(self, **kwargs):
    #     context = super(RoleListView,self).get_context_data(**kwargs)
    #
    #     context['keyword'] = self.keyword
    #     #context['user'] = self.request.user.username
    #     #rolelist = list(context["object_list"])
    #     rolelist = []
    #     for role in context["object_list"]:
    #         role_info = {}
    #         # role_name = role.name
    #         # role_username = role.user_set.all()
    #         role_info['id'] = role.id
    #         role_info['name'] = role.name
    #         role_info['member'] = role.user_set.all()
    #         role_info['permissions'] = role.permissions.all()
    #         rolelist.append(role_info)
    #     context['rolelist'] = rolelist
    #     print(context)
    #     return context


    #去前端展示
    def get_context_data(self, **kwargs):
        context = super(RoleListView, self).get_context_data(**kwargs)
        context['keyword'] = self.keyword

        return context

    #添加角色
    def post(self, request):
        _roleForm = RoleProfileForm(request.POST)
        if _roleForm.is_valid():
            try:
                data = _roleForm.cleaned_data
                print(data)
                self.model.objects.create(**data)
                res = {'code': 0, 'result': '添加角色成功'}
            except:
                # logger.error("create user  error: %s" % traceback.format_exc())
                res = {'code': 1, 'errmsg': '添加角色失败'}
        else:
            # 获取自定义的表单错误的两种常用方式
            print(_roleForm.errors)
            # <ul class="errorlist">
            #   <li>phone<ul class="errorlist"><li>手机号码非法</li></ul></li>
            #   <li>username<ul class="errorlist"><li>已存在一位使用该名字的用户。</li></ul></li>
            # </ul>
            print(_roleForm.errors.as_json())
            # {"phone": [{"message": "\u624b\u673a\u53f7\u7801\u975e\u6cd5", "code": "invalid"}],
            # "username": [{"message": "\u5df2\u5b4f7f\u7528\u8be5\u540d\u5b57\u7684\u7528\u6237\u3002",
            # "code": "unique"}]}
            # print(_roleForm.errors['phone'][0])  # 手机号码非法
            print(_roleForm.errors['name'][0])  # 已存在一位使用该名字的用户
            res = {'code': 1, 'errmsg': _roleForm.errors.as_json()}

        return JsonResponse(res, safe=True)

    def delete(self,request,**kwargs):
        print(kwargs)
        data = QueryDict(request.body).dict()
        id = data['id']
        print(id)

        try:
            self.model.objects.get(id=id).delete()
            res = {'code': 0, 'result': '删除角色成功'}
        except:
        # print(id)
            res = {'code': 1, 'errmsg': '删除角色失败'}

        return JsonResponse(res, safe=True)


class RolePowerView(LoginRequiredMixin,PermissionRequiredMixin, DetailView):
    login_url = '/login/'  # 用户没有通过或者权限不够时跳转的地址，默认是 settings.LOGIN_URL.
    # 把没通过检查的用户重定向到没有 "next page" 的非登录页面时，把它设置为 None ，这样它会在 URL 中移除。
    redirect_field_name = 'redirect_to'

    permission_required = ('users.view_group','users.delete_group','users.add_group','users.change_group')

    """
    更新角色及权限
    """
    template_name = 'users/role_power.html'
    model = Group
    context_object_name = 'role'

    # 返回所有组、权限，并将当前用户所拥有的组、权限显示
    def get_context_data(self, **kwargs):
        context = super(RolePowerView, self).get_context_data(**kwargs)
        context['role_has_users'],context['role_has_permissions'] = self._get_role_power()
        context['role_not_users'],context['role_not_permissions'] = self._get_role_not_power()
        return context

    # 获取当前角色所有用户，权限以列表形式返回
    def _get_role_power(self):
        pk = self.kwargs.get(self.pk_url_kwarg)
        try:
            role = self.model.objects.get(pk=pk)
            users = role.user_set.all()
            return users,role.permissions.all()
        except self.model.DoesNotExist:
            raise Http404

    # 获取当前角色没有的用户，权限，以列表形式返回
    def _get_role_not_power(self):
        pk = self.kwargs.get(self.pk_url_kwarg)
        try:
            role = self.model.objects.get(pk=pk)
            all_user = UserProfile.objects.all()
            users = [user for user in all_user if user not in role.user_set.all()]
            all_perms = Permission.objects.all()
            perms = [perm for perm in all_perms if perm not in role.permissions.all()]
            return users,perms
        except:
            return JsonResponse([], safe=False)

    #修改角色
    def post(self, request, **kwargs):
        #ops.user_set.set([2])
        print(request.POST)
        print(request.POST.getlist('users', []))
        user_id_list = request.POST.getlist('users_selected', [])
        permission_id_list = request.POST.getlist('perms_selected', [])
        pk = kwargs.get("pk")
        try:
            role = self.model.objects.get(pk=pk)
            # user.groups.set(group_id_list)
            print(user_id_list)
            role.user_set.set(user_id_list)
            role.permissions.set(permission_id_list)
            res = {'code': 0, 'next_url': reverse("users:role_list"), 'result': '角色权限更新成功'}
        except:
            res = {'code': 1, 'next_url': reverse("users:role_list"), 'errmsg': '角色权限更新失败'}
            #logger.error("edit  user group pwoer error: %s" % traceback.format_exc())
        return render(request, settings.JUMP_PAGE, res)