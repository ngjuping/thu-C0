"""Qinghuiyue URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import TemplateView
from Qinghuiyue import views
import Qinghuiyue.feedback.views


urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('api/main/notices', views.get_notices),
                  path('api/', include('Qinghuiyue.users.urls')),
                  path('api/', include('Qinghuiyue.venues.urls')),

                  path('api/manage/share', include('Qinghuiyue.share.urls')),
                  path('api/manage/feedback', include('Qinghuiyue.feedback.urls')),
                  path('api/admin/reply/feedback',Qinghuiyue.feedback.views.reply_feedback),
                  path('api/',include('Qinghuiyue.reservation.urls')),

                  path('api',include('Qinghuiyue.admin_notice.urls')),
                  path('api',include('Qinghuiyue.admin_course.urls')),
                  path('api',include('Qinghuiyue.admin_venue.urls')),
                  path('api/pay/',include('Qinghuiyue.alipay.urls')),
                  path('',TemplateView.as_view(template_name="index.html"))

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

