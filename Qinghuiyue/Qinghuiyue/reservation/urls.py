from django.urls import path
import Qinghuiyue.reservation.views as views
urlpatterns=[
    path('manage/courts',views.get_reservations),
    path('book',views.book_first_come),
    path('manage/reservation/transfer',views.transfer_reservation),
    path('manage/reservation/cancel',views.cancel_reservation),
    path('draw',views.book_draw)
]