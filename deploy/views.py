
# Create your views here.


from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse,QueryDict
from django.urls import reverse
from django.views.generic import View, TemplateView, ListView, DetailView
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin

# 分页
from pure_pagination import Paginator, PageNotAnInteger
from pure_pagination.mixins import PaginationMixin

# 自定义模块
from utils.gitlab_api import get_user_projects, get_project_versions,get_project_branchs
from utils.python_jenkins import JenkinsApi

from deploy.models import Deploy
import json, logging, traceback
import  datetime

#form
from deploy.forms import ApplyForm,DeployForm

#task
from .tasks import check_build_result_task,task_send_mail,build_job_task

jenkinsapi = JenkinsApi()


class ApplyView(LoginRequiredMixin, TemplateView):
    """
    申请发布
    """

    template_name = 'deploy/apply.html'
    def get_context_data(self, **kwargs):
        context = super(ApplyView, self).get_context_data(**kwargs)
        context['user_projects'] = get_user_projects(self.request)
        return context

    def post(self, request):
        forms = ApplyForm(request.POST)
        print(forms)
        if forms.is_valid():
            name = request.POST.get('name', '')
            version = request.POST.get('version', '')
            version_desc = request.POST.get('version_desc', '')
            update_detail = request.POST.get('update_detail', '')
            has_apply = Deploy.objects.filter(name=name.split('/')[1], status__lt=2)
            if has_apply:
                return render(request, 'deploy/apply.html',
                              {'errmsg': '该项目已经申请上线，但是上线还没有完成，上线完成后方可再次申请！'})
            try:
                apply_release = Deploy()
                apply_release.name = name.split('/')[1]
                apply_release.version = version
                apply_release.version_desc = version_desc
                apply_release.update_detail = update_detail
                apply_release.status = 0
                apply_release.applicant = request.user
                apply_release.save()
                return HttpResponseRedirect(reverse('deploy:list'))
            except:
                return render(request, 'deploy/apply.html', {'errmsg': '申请失败，请查看日志'})
        else:
            return render(request, 'deploy/apply.html', {'forms': forms, 'errmsg': '申请格式错误！'})

class ProjectListView(LoginRequiredMixin, View):
    """
    当前登陆用户的项目列表
    """

    def get(self, request):
        my_projects = get_user_projects(request)
        print(my_projects)
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(my_projects, 10, request=request)
        projects = p.page(page)

        return render(request, 'deploy/project_list.html', {'page_obj': projects, 'p': p})

class GetProjectVersionsView(LoginRequiredMixin, View):
    """
    获取指定项目的所有版本
    """

    def get(self, request):
        project_id = request.GET.get('project_id', '').split('/')[0]
        print(project_id)
        tags = get_project_versions(int(project_id))
        tags = [[tag.name, tag.message] if tag.message else  [tag.name, '无描述'  ] for tag in tags]
        branchs = get_project_branchs(int(project_id))
        branchs = [[b.name, '无描述'] for b in branchs]
        tags.extend(branchs)
        print(tags)
        return HttpResponse(json.dumps(tags), content_type='application/json')
class GetBuildConsoleView(LoginRequiredMixin,View):
    #获取build console
    def get(self,request):
        id = request.GET.get('id')
        deploy = Deploy.objects.get(id=id)

        name = deploy.name
        url = deploy.build_url
        number = deploy.build_serial
        status = deploy.status

        print('查看console',name,url,number,status)

        #调用jenkins api 函数 得到build结果
        if number:
            try:
                console = jenkinsapi.get_build_console_output(name,number)
            except Exception as e:
                console = '准备构建中...'
                #print(e)

        else:
            console = '准备构建中...'

        res = {'url':url,'console':console,'status':status}
        #print('getconsole: {}'.format(console))
        #return HttpResponse(json.dumps(console), content_type='application/json')

        return JsonResponse(res, safe=True)


class GetBuildingStatusView(LoginRequiredMixin,View):
    def get(self,request):

        id = request.GET.get('id')
        number = request.GET.get('number')
        #print('request number:{}'.format(number))
        deploy = Deploy.objects.get(id=id)
        name = deploy.name
        #number = jenkinsapi.get_next_build_number(name)
        info = jenkinsapi.get_build_info(name,number)
        #print('查看构建状态',name,number,info)
        building_bool = info['building']
        if not building_bool:
            result = info['result']
            if result == 'SUCCESS':
                res = {'code': 0 ,'status':'SUCCESS'}
            else:
                res = {'code': 1,'status':'FAILED'}

        else:

            res = {'code': 2, 'status': 'Building'}
        return JsonResponse(res, safe=True)


class GetNextBuildNmberView(LoginRequiredMixin,View):
    def get(self,request):
        id = request.GET.get('id')
        deploy = Deploy.objects.get(id=id)
        name = deploy.name
        number = jenkinsapi.get_next_build_number(name)
        res = {'number':number}
        #print('已返回下一个构建数',res)
        return JsonResponse(res,safe=True)



class ApplyListView(LoginRequiredMixin, PaginationMixin, ListView):
    """
    申请发布列表
    """

    model = Deploy
    template_name = "deploy/apply_list.html"
    context_object_name = "apply_list"
    paginate_by =10
    keyword = ''

    def get_queryset(self):
        queryset = super(ApplyListView, self).get_queryset()
        queryset = queryset.filter(status__lt=2)
        # 管理员能看到所有待上线列表，个人只能看到自己的
        if 'sa' not in [group.name for group in self.request.user.groups.all()]:
            queryset = queryset.filter(applicant=self.request.user)
        self.keyword = self.request.GET.get('keyword', '')
        if self.keyword:
            queryset = queryset.filter(Q(name__icontains=self.keyword) |
                                           Q(update_detail__icontains=self.keyword) |
                                           Q(version_desc__icontains=self.keyword))
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ApplyListView, self).get_context_data(**kwargs)
        context['keyword'] = self.keyword
        return context

    def post(self,request):
        # 取消工单
        data = QueryDict(request.body).dict()
        id = data['apply_id']
        #
        try:

            deploy = self.model.objects.get(id=id)
            deploy.status = 3
            deploy.complete_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            deploy.save()
            res = {'code': 0, 'result': '取消成功'}
        except:
            res = {'code': 1, 'errmsg': '取消失败'}
        return JsonResponse(res, safe=True)


class DeployView(LoginRequiredMixin, DetailView):
    """
    通过获取当前项目状态，执行代码发布功能
    """

    model = Deploy
    template_name = 'deploy/deploy_detail.html'
    context_object_name = 'deploy'


    def get_context_data(self, **kwargs):
        context = super(DeployView, self).get_context_data(**kwargs)
        context['request_user_groups'] = [ group.name for group in self.request.user.groups.all()]

        return context

    def post(self, request, **kwargs):

        forms = DeployForm(request.POST)
        pk = kwargs.get('pk')
        print(pk)
        deploy = Deploy.objects.get(pk=pk)
        name = deploy.name
        version = deploy.version
        version_desc = deploy.version_desc
        update_detail = deploy.update_detail
        #deploy.handler = request.user
        if forms.is_valid():
            if deploy:
                # 如果status为0,说明是申请状态，点击了仿真按钮，需要上线到仿真环境，并把status改为1
                #if deploy.status == 0:
                #获取最新一次构建序号
                #new_url, new_number = get_build_url_number(name)
                new_url = jenkinsapi.get_next_build_url(name)
                new_number = jenkinsapi.get_next_build_number(name)
                #print(new_number,new_number)

                deploy.build_serial = new_number  #记录构建序号
                #print('新构建号入库前:',new_number)

                deploy.build_url = new_url     #记录构建url
                deploy.save()
                #print('新构建号入库后:', deploy.build_serial)

                #构建


                #检查是否可以执行构建
                #if check_job(name,new_number):
                if jenkinsapi.check_job_number_exists(name,new_number):
                    print('已构建')
                else:

                    params = {'version': version, 'version_desc': version_desc, 'update_detail': update_detail}
                    #print('正在构建 {}'.format(new_url))
                    #obj = build_job(name, params) # 通过Jenkins api 操作将制定项目的代码推送到规定的服务器上去
                    #jenkinsapi.build_job(name,params)
                    if deploy.status == 0:
                        deploy.reviewer = request.user
                        deploy.review_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    elif deploy.status == 1:
                        deploy.handler = request.user
                        deploy.deploy_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    build_job_task.delay(name,params)
                    check_build_result_task.delay(name,new_number,pk)
                deploy.save()
                msg = '正在构建'
                # deploy.reviewer = request.user
                # deploy.review_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


                # # 如果状态为1 ，说明已经是仿真状态，点击上线按钮，讲代码推到正式环境，同时状态改为2
                # elif deploy.status == 1:
                #
                #     # 计算出该次次构建序号
                #     new_url = jenkinsapi.get_next_build_url(name)
                #     new_number = jenkinsapi.get_next_build_number(name)
                #     print(new_number, new_number)
                #
                #     deploy.build_serial = new_number  # 记录构建序号
                #
                #     deploy.build_url = new_url  # 记录构建url
                #     ## jenkins 发布成功
                #     params = {'version': version, 'version_desc': version_desc, 'update_detail': update_detail}
                #
                #     #if check_job(name, new_number):
                #     if jenkinsapi.check_job(name, new_number):
                #         #build_job(name, params)  # 通过Jenkins api 操作将制定项目的代码推送到规定的服务器上去
                #         jenkinsapi.build_job(name,params)
                #         print('正在构建 {}'.format(new_url))
                #
                #         deploy.handler = request.user
                #         deploy.deploy_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                #     msg = "正在构建"
                # else:
                #     return HttpResponseRedirect(reverse('deploy:history'))
                # deploy.save()
                #request_user_groups = [group.name for group in self.request.user.groups.all()]
                #return render(request, 'deploy/deploy_detail.html', {'deploy': deploy, 'msg': msg,'request_user_groups':request_user_groups})
                return HttpResponse(json.dumps(msg), content_type='application/json')

        else:
            #return render(request, 'deploy/deploy_detail.html', {'errmsg': "提交格式不正确", 'forms': forms})
            errmsg = '提交格式不正确'
            print(errmsg)
            return HttpResponse(json.dumps(errmsg), content_type='application/json')
#
class DeployHistoryView(LoginRequiredMixin, PaginationMixin, ListView):
    """
    历史发布列表
    """

    model = Deploy
    template_name = "deploy/history_list.html"
    context_object_name = "apply_list"
    paginate_by =10
    keyword = ''

    def get_queryset(self):
        queryset = super(DeployHistoryView, self).get_queryset()
        queryset = queryset.filter(status__gte=2)
        # 管理员能看到所有待上线列表，个人只能看到自己的
        if 'sa' not in [group.name for group in self.request.user.groups.all()]:
            queryset = queryset.filter(applicant=self.request.user)
        self.keyword = self.request.GET.get('keyword', '')
        if self.keyword:
            queryset = queryset.filter(Q(name__icontains=self.keyword) |
                                           Q(update_detail__icontains=self.keyword) |
                                           Q(version_desc__icontains=self.keyword))

        return queryset

    def get_context_data(self, **kwargs):
        context = super(DeployHistoryView, self).get_context_data(**kwargs)
        context['keyword'] = self.keyword
        context['request_user_groups'] = [ group.name for group in self.request.user.groups.all()]

        return context