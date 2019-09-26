
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


import uuid
# Create your models here.

def image_upload_to(instance,filename):
    print(instance.username)
    return 'headportrait/{id}/{filename}'.format(id=instance.id, filename=instance.username+'.png')


class UserProfile_HeadPortrait(models.Model):
    image = models.ImageField(upload_to=image_upload_to,verbose_name='用户头像',blank=True,null=True,default='headportrait/default.png')
    height_field = models.IntegerField(default=160)
    width_field = models.IntegerField(default=160)
    upload_time = models.DateTimeField(auto_now_add=True, verbose_name='上传时间')

class UserProfile(AbstractUser):
    name_cn = models.CharField('中文名',max_length=30)
    phone = models.CharField('手机',max_length=11,null=True,blank=True)
    headportrait = models.ImageField(upload_to=image_upload_to,verbose_name='头像',default='headportrait/default.png')

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

        def __str__(self):
            return self.username



