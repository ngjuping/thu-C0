from django.urls import path
import Qinghuiyue.venues.views as views

urlpatterns = [
    path('main/venues', views.get_venues_info),
    path('main/venues/list', views.get_venues_list),
    path('booking', views.get_courts_info)
]
