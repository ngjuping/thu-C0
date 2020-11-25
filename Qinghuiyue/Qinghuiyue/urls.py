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
from django.urls import path

from Qinghuiyue import views
import Qinghuiyue.users.views
from Qinghuiyue import venus
import Qinghuiyue.venus.views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/main/notices',views.get_notices),
    path('api/booking',Qinghuiyue.venus.views.get_courts_info),
    path('api/signup', Qinghuiyue.users.views.signup),
    path('api/login', Qinghuiyue.users.views.login),
    path('api/logout', Qinghuiyue.users.views.logout),
    path('api/main/venues',Qinghuiyue.venus.views.get_venues_info),
    path('api/main/venues/list',Qinghuiyue.venus.views.get_venues_list),
    path('api/manage/courts',views.get_reservations),
    path('api/book',views.book_first_come)
]
