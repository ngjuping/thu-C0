import Qinghuiyue.admin_venue.views as views
from django.urls import path
urlpatterns = [
	path('/admin/create/venue', views.create_venue),
	path('/admin/create/court', views.create_court),
	path('/admin/update/court', views.update_court),
	path('/admin/update/venue', views.update_venue)
]