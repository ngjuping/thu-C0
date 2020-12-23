import Qinghuiyue.admin_venue.views as views
from django.urls import path
urlpatterns = [
	path('/admin/create/venue', views.create_venue),
	path('/admin/create/court', views.create_court),
	path('/admin/update/court', views.update_court),
	path('/admin/update/venue', views.update_venue),
	path('/admin/schedule',views.make_schedule),
	path('/admin/delete/venue',views.delete_venue),
	path('/admin/delete/court',views.delete_court),
	path('/admin/court/list',views.list_court),
 	path('/admin/csv/generate',views.generate_csv)

]