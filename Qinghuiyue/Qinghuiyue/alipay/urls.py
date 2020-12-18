import Qinghuiyue.alipay.views as views
from django.urls import path
urlpatterns=[
    path('result/',views.pay_result),
    path('update_order/',views.update_order),
    path('index/',views.index)
]