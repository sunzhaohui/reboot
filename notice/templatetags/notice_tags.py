# _*_ encoding:utf-8 _*_
__author__ = 'sunzhaohui'
__date__ = '2019-08-11 15:49'

from django import template
register = template.Library()


@register.filter(name='read_or_unread')
def read_or_unread(unread):
    """
    bool转未读或已读
    """
    if unread:
        return '未读'
    else:
        return '已读'

