# _*_ encoding:utf-8 _*_
__author__ = 'sunzhaohui'
__date__ = '2019-08-05 12:04'

from django import forms


from django.contrib.auth.models import Group, Permission
from .models import UserProfile
import re

class LoginForm(forms.Form):
    username = forms.CharField(required=True,max_length=20)
    password = forms.CharField(required=True,min_length=6)


##验证个人头像
class UserHeadportraitForm(forms.ModelForm):


    def clean_headportrait(self):
        headportrait = self.cleaned_data['headportrait']
        print(headportrait)

        if headportrait.content_type not in ['image/jpeg','image/png','image/gif']:
            print(forms.ValidationError('图片不合法',code='invalid'))
            raise forms.ValidationError('图片不合法',code='invalid')
        else:
            print(headportrait)
            return headportrait


# 添加用户表单验证
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        # fields = "__all__"
        fields = ['username', 'name_cn', 'phone','email']

    def clean_phone(self):
        """
        通过正则表达式验证手机号码是否合法
        """
        phone = self.cleaned_data['phone']
        phone_regex = r'^1[34578][0-9]{9}$'
        p = re.compile(phone_regex)
        if p.match(phone):
            return phone
        else:
            # forms.ValidationError自定义表单错误
            raise forms.ValidationError('手机号码非法', code='invalid')

# 更新用户表单验证
"""
UserProfileForm会联合model判断字段是否合法，同时也会检查数据库的唯一性索引，故而更新操作不能复用。
例如，更新一个 username=aa的用户，UserProfileForm先检查字段是否合法，然后检查数据库里有没有这个
用户。如果有则任务违反了唯一性索引，验证不通过。
"""


class UserUpdateForm(forms.Form):
    username = forms.CharField(required=True, max_length=10)
    name_cn = forms.CharField(required=True, max_length=30)
    phone = forms.CharField(required=True, max_length=11)

    def clean_phone(self):
        """
        通过正则表达式验证手机号码是否合法
        """
        phone = self.cleaned_data['phone']
        phone_regex = r'^1[34578][0-9]{9}$'
        p = re.compile(phone_regex)
        if p.match(phone):
            return phone
        else:
            # forms.ValidationError自定义表单错误
            raise forms.ValidationError('手机号码非法', code='invalid')

class ModifyPasswordFor(forms.Form):
    newpassword = forms.CharField(required=True,min_length=6)
    newpassword2 = forms.CharField(required=True, min_length=6)


    # def clean_password(self):
    #     newpassword = self.cleaned_data['newpassword']
    #     print('clean_password')
    #     print(newpassword)
    #     newpassword2 = self.cleaned_data['newpassword2']
    #     print(newpassword2)
    #     if newpassword == newpassword2:
    #         return self.cleaned_data
    #     else:
    #         # forms.ValidationError自定义表单错误
    #         raise forms.ValidationError('两次密码不一致', code='invalid')



# 添加角色表单验证
class RoleProfileForm(forms.ModelForm):
    class Meta:
        model = Group
        # fields = "__all__"
        fields = ['name']

    def clean_name(self):
        """
        通过正则表达式验证手机号码是否合法
        """
        name = self.cleaned_data['name']
        name_regex = r'\S{1,16}$'
        p = re.compile(name_regex)
        if p.match(name):
            return name
        else:
            # forms.ValidationError自定义表单错误
            raise forms.ValidationError('角色名非法', code='invalid')

# 添加权限表单验证
class PowerForm(forms.ModelForm):
    class Meta:
        model = Permission
        # fields = "__all__"
        fields = ['name','codename']


    # def clean_phone(self):
    #     """
    #     通过正则表达式验证手机号码是否合法
    #     """
    #     phone = self.cleaned_data['phone']
    #     phone_regex = r'^1[34578][0-9]{9}$'
    #     p = re.compile(phone_regex)
    #     if p.match(phone):
    #         return phone
    #     else:
    #         # forms.ValidationError自定义表单错误
    #         raise forms.ValidationError('手机号码非法', code='invalid')