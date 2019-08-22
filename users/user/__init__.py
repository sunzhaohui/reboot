# _*_ encoding:utf-8 _*_
__author__ = 'sunzhaohui'
__date__ = '2019-08-05 17:20'

from django.conf import settings
from django.shortcuts import render

from django.http import HttpResponse,QueryDict,HttpResponseRedirect,JsonResponse,Http404
from django.urls import reverse

from users.models import UserProfile
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q

from users.forms import UserProfileForm,UserUpdateForm,ModifyPasswordFor



from django.contrib.auth.hashers import make_password

from django.views.generic import View,ListView,DetailView
from django.contrib.auth import authenticate, login, logout
# Create your views here.

# 用户认证及权限管理模块导入
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from pure_pagination.mixins import PaginationMixin


class UserListView(LoginRequiredMixin,PermissionRequiredMixin,PaginationMixin,ListView):

    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    permission_required = ('users.view_userprofile','users.delete_userprofile','users.add_userprofile','users.change_userprofile')


    model = UserProfile
    template_name = "users/user_list.html"
    context_object_name = "userlist"

    paginate_by = 2
    keyword = ''


    #搜索
    def get_queryset(self):
        queryset = super(UserListView, self).get_queryset()
        self.keyword = self.request.GET.get('keyword','').strip()
        print(self.keyword)
        if self.keyword:
            queryset = queryset.filter(Q(name_cn__icontains=self.keyword)| Q(username__icontains=self.keyword) )
        return queryset
    #显示搜索关键字
    def get_context_data(self, **kwargs):
        context = super(UserListView,self).get_context_data(**kwargs)
        context['keyword'] = self.keyword

        return context

    """
        创建用户
        """

    def post(self, request):
        print(request.POST)
        _userForm = UserProfileForm(request.POST)
        #print(_userForm.cleaned_data)

        if _userForm.is_valid():
            try:
                _userForm.cleaned_data['password'] = make_password("12345678")
                _userForm.cleaned_data['is_active'] = True
                data = _userForm.cleaned_data
                print(data)
                self.model.objects.create(**data)
                res = {'code': 0, 'result': '添加用户成功'}
            except:
                #logger.error("create user  error: %s" % traceback.format_exc())
                res = {'code': 1, 'errmsg': '添加用户失败'}
        else:
            # 获取自定义的表单错误的两种常用方式
            print(_userForm.errors)
            # <ul class="errorlist">
            #   <li>phone<ul class="errorlist"><li>手机号码非法</li></ul></li>
            #   <li>username<ul class="errorlist"><li>已存在一位使用该名字的用户。</li></ul></li>
            # </ul>
            print(_userForm.errors.as_json())
            # {"phone": [{"message": "\u624b\u673a\u53f7\u7801\u975e\u6cd5", "code": "invalid"}],
            # "username": [{"message": "\u5df2\u5b4f7f\u7528\u8be5\u540d\u5b57\u7684\u7528\u6237\u3002",
            # "code": "unique"}]}
            # print(_userForm.errors['phone'][0])  # 手机号码非法
            # print(_userForm.errors['username'][0])  # 已存在一位使用该名字的用户
            res = {'code': 1, 'errmsg': _userForm.errors.as_json()}

        return JsonResponse(res, safe=True)

    def delete(self,request,**kwargs):
        print(kwargs)
        data = QueryDict(request.body).dict()
        id = data['id']

        try:
            self.model.objects.get(id=id).delete()
            res = {'code': 0, 'result': '删除用户成功'}
        except:
        # print(id)
            res = {'code': 1, 'errmsg': '删除用户失败'}

        return JsonResponse(res, safe=True)


class UserDetailView(LoginRequiredMixin,PermissionRequiredMixin,DetailView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    permission_required = ('users.view_userprofile','users.delete_userprofile','users.add_userprofile','users.change_userprofile')

    # 用户详情
    model = UserProfile  #UserProfile.objects.filter(pk=pk)
    template_name = "users/user_edit.html"
    context_object_name = "user"

    """
    更新用户信息
    """
    def get_context_data(self, **kwargs):
        context = super(UserDetailView,self).get_context_data(**kwargs)


        return context

    def post(self, request, **kwargs):
        print(request.POST)  # <QueryDict: {'id': ['7'], 'username': ['aa'], 'name_cn': ['bb'], 'phone': ['13305779168']}>
        print(kwargs)  # {'pk': '7'}
        print(request.body)  # b'id=7&username=aa&name_cn=bb&phone=13305779168'
        pk = kwargs.get("pk")
        data = QueryDict(request.body).dict()
        print(data)  # {'id': '7', 'username': 'aa', 'name_cn': 'bb', 'phone': '13305779168'}
        _userForm = UserUpdateForm(request.POST)
        if _userForm.is_valid():
            try:
                self.model.objects.filter(pk=pk).update(**data)
                res = {'code': 0, "next_url": reverse("users:user_list"), 'result': '更新用户成功'}
            except:
                res = {'code': 1, "next_url": reverse("users:user_list"), 'errmsg': '更新用户失败'}

        else:
            # 获取所有的表单错误
            print(_userForm.errors)
            res = {'code': 1, "next_url": reverse("users:user_list"), 'errmsg': _userForm.errors}
        return render(request, settings.JUMP_PAGE, res)

class ModifyPasswordView(LoginRequiredMixin,View):
    #modifypassword/?uid=2
    def get(self,request,**kwargs):

        uid = request.GET.get('uid')
        print(uid)
        user = UserProfile.objects.get(id=uid)
        return render(request, "users/modify_pwd.html",{"user":user})



    def post(self, request, **kwargs):
        print(request.POST)  # <QueryDict: {'id': ['7'], 'username': ['aa'], 'name_cn': ['bb'], 'phone': ['13305779168']}>
        print(kwargs)  # {'pk': '7'}
        print(request.body)  # b'id=7&username=aa&name_cn=bb&phone=13305779168'
        id = request.POST.get('id')
        data = {}
        newpassword = request.POST.get('newpassword')
        newpassword2 = request.POST.get('newpassword2')
        print(make_password(newpassword))
        user = UserProfile.objects.filter(id=id)
        if newpassword == newpassword2:
            data['password'] = make_password(newpassword)
            try:

                print(make_password(newpassword))

                user.update(**data)
                res = {'code': 0, "next_url": reverse("users:user_list"), 'result': '修改成功'}
                return render(request, settings.JUMP_PAGE, res)
            except:
                res = {'code': 1, "next_url": reverse("users:user_list"), 'errmsg': '修改失败'}
            return render(request, settings.JUMP_PAGE, res)
        else:
            return render(request,"users/modify_pwd.html",{"user":user,'errmsg': '密码不一致'})



#修改用户角色和权限
class UserGroupPowerView(LoginRequiredMixin,PermissionRequiredMixin ,DetailView):
    """
    更新用户角色及权限
    """
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    permission_required = ('users.view_userprofile', 'users.delete_userprofile', 'users.add_userprofile', 'users.change_userprofile')

    template_name = 'users/user_group_power.html'
    model = UserProfile
    context_object_name = 'user'

    # 返回所有组、权限，并将当前用户所拥有的组、权限显示
    def get_context_data(self, **kwargs):
        context = super(UserGroupPowerView, self).get_context_data(**kwargs)
        context['user_has_groups'], context['user_has_permissions'] = self._get_user_group_power()
        context['user_not_groups'], context['user_not_permissions'] = self._get_user_not_group_power()
        print(context['user_has_permissions'])
        return context

    # 获取当前用户所有组、权限以列表形式返回
    def _get_user_group_power(self):
        pk = self.kwargs.get(self.pk_url_kwarg)
        try:
            user = self.model.objects.get(pk=pk)
            return user.groups.all(), user.user_permissions.all()
            #获取用户最终权限: user.get_all_permissions()
        except self.model.DoesNotExist:
            raise Http404

    # 获取当前用户没有的组、权限，以列表形式返回
    def _get_user_not_group_power(self):
        pk = self.kwargs.get(self.pk_url_kwarg)
        try:
            user = self.model.objects.get(pk=pk)
            all_group = Group.objects.all()
            groups = [group for group in all_group if group not in user.groups.all()]
            all_perms = Permission.objects.all()
            perms = [perm for perm in all_perms if perm not in user.user_permissions.all()]
            return groups, perms
        except:
            return JsonResponse([], safe=False)

    def post(self, request, **kwargs):
        group_id_list = request.POST.getlist('groups_selected', [])
        permission_id_list = request.POST.getlist('perms_selected', [])
        pk = kwargs.get("pk")
        try:
            user = self.model.objects.get(pk=pk)
            user.groups.set(group_id_list)
            user.user_permissions.set(permission_id_list)
            res = {'code': 0, 'next_url': reverse("users:user_list"), 'result': '用户角色权限更新成功'}
        except:
            res = {'code': 1, 'next_url': reverse("users:user_list"), 'errmsg': '用户角色权限更新失败'}
            #logger.error("edit  user group pwoer error: %s" % traceback.format_exc())
        return render(request, settings.JUMP_PAGE, res)


class UserView(LoginRequiredMixin, View):
        login_url = '/login/'
        redirect_field_name = 'redirect_to'


        def get(self,request,**kwargs):
            id = self.request.user.id
            user = UserProfile.objects.get(id=id)
            all_powerlist = []
            powerlist = user.user_permissions.all()
            all_powerlist.extend(powerlist)
            rolelist = user.groups.all()
            roledict = {}
            for role in rolelist:
                r = Group.objects.get(name=role)
                r.permissions.all()
                all_powerlist.extend(r.permissions.all())
                roledict[role] = r.permissions.all()

            return render(request, "users/user.html", {'user':user,'powerlist':powerlist,'roledict':roledict,'all_powerlist':list(set(all_powerlist))})
        def post(self,request):
            data = QueryDict(self.request.body).dict()
            id = data['id']
            user = UserProfile.objects.filter(id=id)
            print(data)
            try:
                user.update(**data)
                res = {'code': 0, 'next_url': reverse("users:index"), 'result': '更新成功'}

            except Exception as e:
                print(e)
                res = {'code': 1, 'next_url': reverse("users:index"), 'result': '更新失败'}


            return render(request, settings.JUMP_PAGE, res)


class UserPasswordView(LoginRequiredMixin,View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    def get(self,request,**kwargs):

        id = self.request.user.id

        user = UserProfile.objects.get(id=id)

        return render(request, "users/modify_pwd.html",{"user":user})



    def post(self, request, **kwargs):
        id = self.request.user.id
        newpassword = request.POST.get('newpassword')
        newpassword2 = request.POST.get('newpassword2')
        print(make_password(newpassword))
        data = {}
        user = UserProfile.objects.filter(id=id)
        if newpassword == newpassword2:
            data['password'] = make_password(newpassword)
            try:

                print(make_password(newpassword))

                user.update(**data)
                res = {'code': 0, "next_url": reverse("users:user_list"), 'result': '修改成功'}
                return render(request, settings.JUMP_PAGE, res)
            except:
                res = {'code': 1, "next_url": reverse("users:user_list"), 'errmsg': '修改失败'}
            return render(request, settings.JUMP_PAGE, res)
        else:
            return render(request,"users/modify_pwd.html",{"user":user,'errmsg': '密码不一致'})