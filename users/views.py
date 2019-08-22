from django.shortcuts import render

from django.http import HttpResponse,QueryDict,HttpResponseRedirect,JsonResponse
from django.urls import reverse

from users.models import UserProfile
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType



from django.contrib.auth.hashers import make_password

from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
# Create your views here.

# 用户认证及权限管理模块导入
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

#导入自定义模块
from .forms import LoginForm







# class UserListView(LoginRequiredMixin,View):
#     login_url = '/login/'  # 用户没有通过或者权限不够时跳转的地址，默认是 settings.LOGIN_URL.
#     # 把没通过检查的用户重定向到没有 "next page" 的非登录页面时，把它设置为 None ，这样它会在 URL 中移除。
#     redirect_field_name = 'redirect_to'
#     #@method_decorator(login_required(login_url='/login/'))
#     def get(self,request):
#         userlist = UserProfile.objects.all()
#         return render(request, 'users/userlist.html', {'users': userlist})
# class RoleListView(LoginRequiredMixin,View):
#     login_url = '/login/'  # 用户没有通过或者权限不够时跳转的地址，默认是 settings.LOGIN_URL.
#     # 把没通过检查的用户重定向到没有 "next page" 的非登录页面时，把它设置为 None ，这样它会在 URL 中移除。
#     redirect_field_name = 'redirect_to'
#     #@method_decorator(login_required(login_url='/login/'))
#     def get(self,request):
#         rolelist = Group.objects.all()
#         print(rolelist)
#         return render(request, 'rolelist.html', {'rolelist': rolelist})

# class PowerListView(LoginRequiredMixin,View):
#     login_url = '/login/'  # 用户没有通过或者权限不够时跳转的地址，默认是 settings.LOGIN_URL.
#     # 把没通过检查的用户重定向到没有 "next page" 的非登录页面时，把它设置为 None ，这样它会在 URL 中移除。
#     redirect_field_name = 'redirect_to'
#     #@method_decorator(login_required(login_url='/login/'))
#     def get(self,request):
#         permissionlist = Permission.objects.values()
#         #permissionlist = list(permissionlist)
#         permissionlist=list(permissionlist)
#         for i in permissionlist:
#             i['content_type'] = ContentType.objects.get(id=i['content_type_id'])
#         #print(len(permissionlist))
#
#         print(permissionlist)
#
#
#
#
#         return render(request, 'users/powerlist.html', {'permissionlist': permissionlist})


class IndexView(LoginRequiredMixin,View):
    """
    登录模块
    """
    login_url = '/login/'      # 用户没有通过或者权限不够时跳转的地址，默认是 settings.LOGIN_URL.
    # 把没通过检查的用户重定向到没有 "next page" 的非登录页面时，把它设置为 None ，这样它会在 URL 中移除。
    redirect_field_name = 'redirect_to'

    #@method_decorator(login_required(login_url='/login/'))
    def get(self, request):
        #return render(request, "index2.html")
        #if not request.user.is_authenticated:
        #    return HttpResponseRedirect(reverse("users:login"))
        #users = UserProfile.objects.all()
        # users = [{'username':'wd','name_cn':'wd','age':18},{'username':'wd2','name_cn':'wd2','age':18},{'username':'wd3','name_cn':'wd3','age':18}]
        print(request.user.is_authenticated)
        print(request.user.username)

        return render(request, 'index.html', {'request': request})

class LoginView(View):


    def get(self, request):
        return render(request, "login.html")


    # def post(self, request):
    #     username = request.POST.get("username", None)
    #     password = request.POST.get("password", None)
    #     print(username)
    #     user = authenticate(username=username, password=password)
    #     print(user)
    #     if user:
    #         if user.is_active:
    #             # 默认为当前登录用户创建session
    #             login(request, user)
    #             # 登录成功则跳到首页
    #             #return HttpResponseRedirect('/userlist/')
    #             # 命名空间的写法
    #             return HttpResponseRedirect(reverse("users:index"))
    #         else:
    #             return render(request, "login.html", {"msg": "用户未激活！"})
    #     else:
    #         return render(request, "login.html", {"msg": "用户名或密码错误！"})

    #ajax数据提交
    def post(self,request):
        res = {"code":0}
        #通过form 验证数据格式是否合法
        login_form = LoginForm(request.POST)
        print('login_form:{}'.format(login_form))
        if login_form.is_valid():
            data = login_form.cleaned_data



            user = authenticate(**data)
            if user is not None:
                if user.is_active:
                    login(request,user)  # 默认为当前登录用户创建session
                    res['next_url'] = '/'
                else:
                    res['code'] =1
                    res['errmsg'] = '用户被禁用'
            else:
                res['code'] = 1
                res['errmsg'] = '用户名或密码错误'
        else:
            res['code'] = 1
            res['errmsg'] = '用户名或密码不合法'
        return JsonResponse(res,safe=True)


class LogoutView(View):
    """
    登出功能
    """

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse("users:login"))
