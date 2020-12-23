import Qinghuiyue.share.views as views
from django.urls import path
urlpatterns=[
    path('/delete',views.delete_share),
    path('/update',views.update_share),
    path('/create',views.create_share),
    path('/user',views.get_user_shares),
    path('',views.get_share_notifications)
]