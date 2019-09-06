# _*_ encoding:utf-8 _*_
__author__ = 'sunzhaohui'
__date__ = '2019-08-11 15:49'

from django import template
register = template.Library()


@register.filter(name='groupsobj_2_groupslist')
def groupsobj_2_groupslist(groupsobj):
    """
    将组对象的列表转成 组名列表
    """
    return [group.name for group in groupsobj]

