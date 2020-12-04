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
from Qinghuiyue import views
from Qinghuiyue import admin_venue
import Qinghuiyue.admin_venue.views
from Qinghuiyue import admin_notice
import Qinghuiyue.admin_notice.views
from Qinghuiyue import admin_course
import Qinghuiyue.admin_course.views
import Qinghuiyue.feedback.views
from Qinghuiyue import venus
urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('api/main/notices', views.get_notices),
                  path('api/', include('Qinghuiyue.users.urls')),
                  path('api/',include('Qinghuiyue.venus.urls')),

                  path('api/manage/share', include('Qinghuiyue.share.urls')),
                  path('api/manage/feedback', include('Qinghuiyue.feedback.urls')),
                  path('api/admin/reply/feedback',Qinghuiyue.feedback.views.reply_feedback),
                  path('api/',include('Qinghuiyue.reservation.urls')),
                  path('api/admin/create/venue', Qinghuiyue.admin_venue.views.create_venue),
                  path('api/admin/create/court', Qinghuiyue.admin_venue.views.create_court),
                  path('api/admin/update/court', Qinghuiyue.admin_venue.views.update_court),
                  path('api/admin/update/venue', Qinghuiyue.admin_venue.views.update_venue),

                  path('api/admin/create/notice', Qinghuiyue.admin_notice.views.create_notice),
                  path('api/admin/delete/notice', Qinghuiyue.admin_notice.views.delete_notice),
                  path('api/admin/update/notice', Qinghuiyue.admin_notice.views.update_notice),

                  path('api/admin/create/course', Qinghuiyue.admin_course.views.create_course),
                  path('api/admin/update/course', Qinghuiyue.admin_course.views.update_course),
                  path('api/admin/delete/course', Qinghuiyue.admin_course.views.delete_course),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)





