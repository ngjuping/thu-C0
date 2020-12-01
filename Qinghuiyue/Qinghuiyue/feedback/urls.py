import Qinghuiyue.feedback.views as views
from django.urls import path
urlpatterns=[
    path('/delete',views.delete_feedback),
    path('/update',views.update_feedback),
    path('/create',views.create_feedback),
    path('',views.get_all_feedback)
]