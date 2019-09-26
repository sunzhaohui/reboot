from django.shortcuts import render,get_object_or_404,Http404
from django.http import HttpResponseRedirect, JsonResponse, QueryDict,HttpResponse
from django.urls import reverse
from django.views.generic import View, ListView, DetailView
from django.db.models import Q
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionDenied
from pure_pagination.mixins import PaginationMixin
import  datetime
from utils import upload_file
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import  permission_required

import traceback, logging
from django.core.mail import send_mail
# 自定义模块导入
from .models import WorkOrder,WorkOrder_Reply,WorkOrder_File
from .forms import WorkOrderApplyForm,WorkOrderResultForm,WorkOrderReplyForm
from django.conf import settings



#task
from .tasks import hello,task_send_mail

from utils.remove_file import remove_file


logger = logging.getLogger("reboot")

class WorkOrderApplyView(LoginRequiredMixin, View):
    def get(self, request):
        forms = WorkOrderApplyForm()
        logger.error('工单申请页')
        return render(request, 'order/workorder_apply.html', {'forms': forms})
    def post(self, request):
        #file_list = request.FILES.getlist('orderfiles')

        #print(request.POST)
        forms = WorkOrderApplyForm(request.POST or None, request.FILES or None)
        if forms.is_valid():
            try:
                #print(forms.cleaned_data)
                title = forms.cleaned_data["title"]
                order_contents = forms.cleaned_data["order_contents"]
                #print(order_contents)
                # assign = forms.cleaned_data["assign"]
                assign_id = forms.cleaned_data["assign_id"]

                #orderfiles = forms.cleaned_data["orderfiles"]
                #print(orderfiles)

                data = forms.cleaned_data
                data.pop('orderfiles',None)
                data['applicant_id'] = request.user.id
                print(data)
                WorkOrder_obj = WorkOrder.objects.create(**data)
                print(WorkOrder_obj)
                for file_obj in request.FILES.getlist('orderfiles'):
                    WorkOrder_File_obj = WorkOrder_File()
                    WorkOrder_File_obj.file = file_obj
                    WorkOrder_File_obj.filetype = file_obj.content_type
                    WorkOrder_File_obj.fileowner = self.request.user
                    WorkOrder_File_obj.save()
                    WorkOrder_obj.files.add(WorkOrder_File_obj)


                # work_order = WorkOrder()
                # work_order.title = title
                # work_order.order_contents = order_contents
                #
                # work_order.assign_id = assign_id
                # work_order.orderfiles = orderfiles
                # work_order.applicant = request.user
                # work_order.status = 0
                # work_order.save()
                # send_mail(title,
                #           order_contents,
                #           settings.EMAIL_FROM,
                #           ['413108892@qq.com'],
                #           fail_silently=False, )
                task_send_mail.delay(title,order_contents,settings.EMAIL_FROM,['413108892@qq.com'])

                return HttpResponseRedirect(reverse('workorder:list'))
            except Exception as e:
                print(e)
                return render(request, 'order/workorder_apply.html', {'forms': forms, 'errmsg': '工单提交出错！'})
        else:
            return render(request, 'order/workorder_apply.html', {'forms': forms, 'errmsg': '工单填写格式出错！'})





class WorkOrderListView(LoginRequiredMixin, PaginationMixin, ListView):
    """
    待处理工单列表展示
    """
    model = WorkOrder
    template_name = 'order/workorder_list.html'
    context_object_name = "orderlist"
    paginate_by = 10
    keyword = ''




    def get_queryset(self):
        queryset = super(WorkOrderListView, self).get_queryset()
        # 只显示状态小于2，即申请和处理中的工单
        queryset = queryset.filter(status__lt=2)
        # 如果不是sa组的用户只显示自己申请的工单，别人看不到你申请的工单，管理员可以看到所有工单
        if 'sa' not in [group.name for group in self.request.user.groups.all()]:
            queryset = queryset.filter(applicant=self.request.user)

        self.keyword = self.request.GET.get('keyword', '').strip()
        if self.keyword:
            queryset = queryset.filter(Q(title__icontains = self.keyword)|
                                       Q(order_contents__icontains = self.keyword)|
                                       Q(result_desc__icontains=self.keyword))
        hello.delay(self.request.user.username)
        #print(self.request.user.username)
        return queryset



    def get_context_data(self, **kwargs):
        context = super(WorkOrderListView, self).get_context_data(**kwargs)
        context['keyword'] = self.keyword

        return context


    def delete(self,request,**kwargs):
        #取消工单
        data = QueryDict(request.body).dict()
        id = data['id']
        #
        try:

            work_order = self.model.objects.get(id=id)
            work_order.status = 4
            work_order.complete_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            work_order.save()
            res = {'code': 0, 'result': '取消成功'}
        except:
             res = {'code': 1, 'errmsg': '取消失败'}
             logger.error("delete order  error: %s" % traceback.format_exc())
        return JsonResponse(res, safe=True)






class WorkOrderDetailView(LoginRequiredMixin, DetailView):
    """
    工单详情页，包括处理结果表单的填写
    """
    model = WorkOrder
    template_name = "order/workorder_detail.html"
    context_object_name = "workorder"

    queryset = WorkOrder.objects.all()
    def get_object(self, queryset=None):

        obj = super().get_object(queryset)
        print(obj.applicant_id)
        print(self.request.user.id)
        if obj.applicant_id == self.request.user.id or self.request.user.has_perms(['work_order.accept_workorder']):
            print('有权限')
            return obj
        else:
            print('无权限')
            #raise Http404
            raise PermissionDenied

    def get_context_data(self, **kwargs):

        pk = self.kwargs.get(self.pk_url_kwarg,None)

        context = super(WorkOrderDetailView, self).get_context_data(**kwargs)

        #print(self.request.user.get_all_permissions())
        #if self.request.user.has_perms(['work_order.delete_workorder_file']):
        #    print('有权限')
        context['MAX_UPLOAD_SIZE'] = settings.MAX_UPLOAD_SIZE
        reply_list = WorkOrder_Reply.objects.filter(title_id=pk)
        for i in reply_list:
            print(i.replyer)
        context['reply_list'] = reply_list
        files = context['workorder'].files.all()
        for f in files:
            print(f.id,f.file.name,f.filetype,f.fileowner,f.fileowner_id)
        return context




    def post(self, request, **kwargs):
        print(request.POST,request.FILES.getlist('file'))
        pk = kwargs.get("pk")
        work_order = self.model.objects.get(pk=pk)

        action =  request.POST.get('action','')
        reply_type = request.POST.get("reply_type",'')
        reply_contents = request.POST.get('reply_contents', '')
        print(action, reply_type)

        #接单
        try:
            if action == 'accept':
                if work_order.status == 0 and self.request.user.has_perms(['work_order.accept_workorder']):
                    work_order.status = 1
                    work_order.handler = request.user
                    work_order.handle_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    work_order.save()
                    data = {'code': 0,}
                else:
                    data = {'code': 1, 'errmsg': '没有接受权限'}
            #回复
            elif action == 'reply':
                print(action,reply_type)
                #if work_order.status == 1:
                forms = WorkOrderReplyForm(request.POST)
                if forms.is_valid():

                    data = {}
                    data['title_id'] = pk
                    data['reply_contents'] = reply_contents
                    data['replyer_id'] = request.user.id
                    data['type'] = int(reply_type)
                    print(data)
                    WorkOrder_Reply.objects.create(**data)
                    data = {
                        'code': 0,
                    }
                else:
                    data = {'code':1,'errmsg':'err'}
            #关闭
            elif action == 'close':
                if work_order.status == 1:
                    work_order.status = 2
                    work_order.complete_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    work_order.save()
                    data = {'code': 0,}
            #重新打开
            elif action == 'open':
                work_order.status = 1
                work_order.save()
                data = {'code':0,}
            #上传附件
            elif request.FILES.getlist('file'):
                print('发现新文件')
                print(request.POST)
                print(request.FILES.getlist('file'))
                for file_obj in request.FILES.getlist('file'):
                    if file_obj.size < int(settings.MAX_UPLOAD_SIZE):
                        WorkOrder_File_obj = WorkOrder_File()
                        WorkOrder_File_obj.file = file_obj

                        WorkOrder_File_obj.filetype = file_obj.content_type
                        WorkOrder_File_obj.fileowner = self.request.user
                        WorkOrder_File_obj.save()
                        print(file_obj.__dict__)
                        #{'file': <_io.BytesIO object at 0x10a290410>, '_name': '《K8S容器云平台工程师》高薪课程.pdf', 'size': 539999, 'content_type': 'application/pdf', 'charset': None, 'content_type_extra': {}, 'field_name': 'file'}
                        work_order.files.add(WorkOrder_File_obj)

                        data = {'code':0,}
                    else:
                        data = {'code':1,'errmsg':'文件 {} 太大'.format(file_obj._name)}
        except Exception as e:
            print(e)
            data = {
                'code': 1,
                'errmsg': str(e)
            }
        return JsonResponse(data)

    #@method_decorator(permission_required('workorder_file.delete_workorder_file', login_url='/'))

    #删除附件
    def delete(self,request, **kwargs):
        pk = kwargs.get("pk")
        workorder_obj = self.model.objects.get(pk=pk)
        data = QueryDict(request.body).dict()
        id = data['id']
        file_obj = WorkOrder_File.objects.get(id=id)

        workorder_obj = self.model.objects.get(pk=pk)

        if self.request.user.has_perms(['work_order.delete_workorder_file']) or self.request.user == file_obj.fileowner:
            try:

                workorder_obj.files.remove(file_obj)
                WorkOrder_File.delete(file_obj)
                res = {'code': 0, 'result': '删除成功'}
                file_path = file_obj.file.path
                remove_file(file_path)

            except:
            # print(id)
                res = {'code': 1, 'errmsg': '删除失败'}
        else:
            res = {'code': 1, 'errmsg': '没有权限'}

        return JsonResponse(res, safe=True)


class WorkOrderHistoryView(LoginRequiredMixin, PaginationMixin, ListView):
    """
    待处理工单列表展示
    """
    model = WorkOrder
    template_name = 'order/workorder_history.html'
    context_object_name = "orderlist"
    paginate_by = 10
    keyword = ''

    def get_queryset(self):
        queryset = super(WorkOrderHistoryView, self).get_queryset()
        # 只显示状态等于2，即已完成的工单
        queryset = queryset.filter(status__gte=2)
        # 如果不是sa组的用户只显示自己申请的工单，别人看不到你申请的工单，管理员可以看到所有工单
        if 'sa' not in [group.name for group in self.request.user.groups.all()]:
            queryset = queryset.filter(applicant=self.request.user)

        self.keyword = self.request.GET.get('keyword', '').strip()
        if self.keyword:
            queryset = queryset.filter(Q(title__icontains = self.keyword)|
                                       Q(order_contents__icontains = self.keyword)|
                                       Q(result_desc__icontains=self.keyword))
        return queryset
    def get_context_data(self, **kwargs):
        context = super(WorkOrderHistoryView, self).get_context_data(**kwargs)
        context['keyword'] = self.keyword
        for order in context['orderlist']:
            print(order.get_status_display)

        return context

    def delete(self,request, **kwargs):
        #删除工单
        data = QueryDict(request.body).dict()
        id = data['id']

        workorder_obj = self.model.objects.get(id=id)


        if self.request.user.has_perms(['work_order.delete_workorder']) or self.request.user.id == workorder_obj.applicant_id:
            try:
                files_id_list = []
                for f in workorder_obj.files.all():
                    files_id_list.append(f.id)



                workorder_obj.delete()

                # res = {'code': 0, 'result': '删除成功',"next_url": reverse("workorder:history")}
                res = {'code': 0, 'result': '删除成功'}


                #删除关联附件
                for file_id in files_id_list:

                    file_obj = WorkOrder_File.objects.get(id=file_id)
                    file_path = file_obj.file.path
                    WorkOrder_File.delete(file_obj)
                    remove_file(file_path)
                    print('已删除{}'.format(file_path))





            except:
            # print(id)
                res = {'code': 1, 'errmsg': '删除失败'}
        else:
            res = {'code': 1, 'errmsg': '没有权限'}

        return JsonResponse(res, safe=True)