"""reboot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin

from django.urls import path, re_path, include
from reboot.settings import MEDIA_ROOT
from reboot.settings import STATIC_ROOT,DEBUG
from django.views.static import serve

import notifications.urls
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),

    path('',include('users.urls'),name='users'),
    path("workorder/", include('work_order.urls'),name="workorder"),
    path("deploy/", include('deploy.urls'),name="deploy"),
    re_path("media/(?P<path>.*)",  serve, {"document_root": MEDIA_ROOT}),
    re_path("static/(?P<path>.*)", serve, {"document_root": STATIC_ROOT}),
    path('inbox/notifications/', include(notifications.urls, namespace='notifications')),
    path('notice/', include('notice.urls', namespace='notice')),


]
