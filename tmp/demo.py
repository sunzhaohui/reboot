# _*_ encoding:utf-8 _*_
__author__ = 'sunzhaohui'
__date__ = '2019-08-21 11:33'


import markdown
from markdown.extensions.toc import TocExtension





body = '''
### Hello there
How are you?

I have bellow task for you :

Select from this text...
Click the bold on THIS WORD and make THESE ONE italic
Link GOOGLE to google.com
Test to insert image (and try to tab after write the image description)
Test Preview
And ending here... Click "List"

Enjoy!

### 测试代码块
```
class IndexView(View):
     """
     登出功能
     """
     # login_url 用户没有通过测试时跳转的地址，默认是 settings.LOGIN_URL
     @method_decorator(login_required(login_url='/login/'))
     def get(self, request):
         return render(request, 'index.html')
```

'''

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

print(markdown_to_html(body))