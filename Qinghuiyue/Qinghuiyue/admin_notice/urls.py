import Qinghuiyue.admin_notice.views as views
from django.urls import path
urlpatterns = [
	path('/admin/create/notice', views.create_notice),
	path('/admin/delete/notice', views.delete_notice),
	path('/admin/update/notice', views.update_notice),
	path('/notices', views.get_notice),
]