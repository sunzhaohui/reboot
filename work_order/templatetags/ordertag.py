# _*_ encoding:utf-8 _*_
__author__ = 'sunzhaohui'
__date__ = '2019-08-11 15:49'

from django import template
register = template.Library()
import markdown
from markdown.extensions.toc import TocExtension


@register.filter(name='orderfile_name')
def orderfile_name(file_path):
    file_name = str(file_path).split('/')[-1]
    return file_name






@register.filter(name='markdown_to_html')
def markdown_to_html(body):
    new_body = markdown.markdown(body,
                      extensions=[
                          # 包含 缩写、表格等常用扩展
                          'markdown.extensions.extra',
                          # 语法高亮扩展
                          'markdown.extensions.codehilite',
                          # 允许我们自动生成目录
                          'markdown.extensions.toc',
                      ]

                      )
    return new_body

@register.filter(name='markdown_to_text')
def markdown_to_text(body):
    new_body = markdown.markdown(body,
                      extensions=[


                      ]

                      )
    return new_body



# 字节bytes转化kb\m\g
@register.filter(name='formatSize')
def formatSize(bytes):
    try:
        bytes = float(bytes)
        kb = bytes / 1024
    except:
        print("传入的字节格式不对")
        return "Error"

    if kb >= 1024:
        M = kb / 1024
        if M >= 1024:
            G = M / 1024
            return "{}G".format(round(G,2))
        else:
            return "{}M".format(round(M,2))
    else:
        return "{}kb".format((round(kb,2)))