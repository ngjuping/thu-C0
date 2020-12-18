import Qinghuiyue.admin_course.views as views
from django.urls import path
urlpatterns = [
				  path('/admin/create/course', views.create_course),
                  path('/admin/update/course', views.update_course),
                  path('/admin/delete/course', views.delete_course),
                  path('/courses', views.get_course),
]