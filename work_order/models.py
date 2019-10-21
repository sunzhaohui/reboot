from django.db import models
from users.models import UserProfile
import uuid
from django.urls import reverse
# Create your models here.

def file_upload_to(instance,filename):
    return 'orderfiles/{uuid}/{filename}'.format(uuid=uuid.uuid4().hex, filename=filename)



class WorkOrder_File(models.Model):
    #file = models.FileField(upload_to='orderfiles/%Y/%m', verbose_name='工单附件', blank=True, null=True)
    file = models.FileField(upload_to=file_upload_to, verbose_name='工单附件', blank=True, null=True)

    upload_time = models.DateTimeField(auto_now_add=True, verbose_name='上传时间')
    filetype = models.CharField(max_length=100,verbose_name="文件类型",null=True,default=None)
    fileowner = models.ForeignKey(UserProfile, verbose_name='上传人', on_delete=models.CASCADE, related_name='file_owner',blank=True,null=True,default=None)



    class Meta:
        verbose_name = 'workorder_file'
        verbose_name_plural = verbose_name
        ordering = ['upload_time']


class WorkOrder(models.Model):
    STATUS = (
        (0, '申请'),
        (1, '处理中'),
        (2, '完成'),
        (3, '失败'),
        (4, '已取消'),

    )
    title = models.CharField(max_length=100, verbose_name='工单标题')
    order_contents = models.TextField(verbose_name='工单内容')
    # orderfiles = models.FileField(upload_to='orderfiles/%Y/%m', verbose_name='工单附件', blank=True, null=True)
    applicant = models.ForeignKey(UserProfile, verbose_name='申请人', on_delete=models.CASCADE, related_name='workorder_applicant')
    assign = models.ForeignKey(UserProfile, verbose_name='指派人', on_delete=models.CASCADE, related_name='workorder_assign')
    handler = models.ForeignKey(UserProfile, verbose_name='最终处理人', blank=True, null=True,on_delete=models.CASCADE, related_name='workorder_handler')
    status = models.IntegerField(choices=STATUS, default=0, verbose_name='工单状态')
    result_desc = models.TextField(verbose_name='处理结果', blank=True, null=True)
    apply_time = models.DateTimeField(auto_now_add=True, verbose_name='申请时间')
    handle_time = models.DateTimeField(auto_now=False, verbose_name='处理时间',null=True)
    complete_time = models.DateTimeField(auto_now=False, verbose_name='处理完成时间',null=True)
    files = models.ManyToManyField(WorkOrder_File,related_name='files',verbose_name='附件')

    def __str__(self):
        return self.title

    def get_detail_url(self):
        return  reverse('workorder:detail', kwargs={'pk': self.id})

    class Meta:
        verbose_name = 'workorder'
        verbose_name_plural = verbose_name
        ordering = ['-complete_time']





class WorkOrder_Reply(models.Model):
     TYPE = (
         (0,'text'),
         (1,'markdown'),
     )
     title = models.ForeignKey(WorkOrder,verbose_name='工单标题',on_delete=models.CASCADE,related_name='workoder_title')
     reply_contents = models.TextField(verbose_name='回复内容', blank=True, null=True)
     replyer = models.ForeignKey(UserProfile, verbose_name='回复人', blank=True, null=True,on_delete=models.CASCADE, related_name='replyer')
     reply_time = models.DateTimeField(auto_now_add=True, verbose_name='申请时间',null=True)
     type = models.IntegerField(choices=TYPE, default=0, verbose_name='回复类型')






