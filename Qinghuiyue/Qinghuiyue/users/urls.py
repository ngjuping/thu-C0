import Qinghuiyue.users.views as views
from django.urls import path
urlpatterns=[
    path('signup',views.signup),
    path('login',views.login),
    path('logout',views.logout),
    path('manage/getuserids',views.get_name_by_id)
]