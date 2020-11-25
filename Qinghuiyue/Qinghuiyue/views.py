from django.http import HttpResponse, JsonResponse

from Qinghuiyue.models import *
from Qinghuiyue.models.models import *
from Qinghuiyue.models.models import Stat
from Qinghuiyue.users.models import User
from Qinghuiyue.venus.models import Court
import json




def get_notices(request):
    '''
    首页获取前三个通知
    :return:
    '''
    try:
        notices_raw=Notification.objects().order_by("-time")[:3]#排序且只取前三个
        notices=[]
        for notice in notices_raw:
            notices.append({"title":notice.title,"content":notice.content,"time":notice.time})
        return JsonResponse({
            "message":"ok",
            "notices":notices
        })
    except Exception:
        return HttpResponse(status=400)

def get_reservations(request):
    '''
    获取用户当前预定信息
    :param request:
    :return:
    '''
    user_id=request.GET['user_id']
    user=User.objects(user_id=user_id)[0]
    rent_now_id=user.rent_now
    rent_now=Reservation.objects(id__in=rent_now_id)
    courts=[{
        "id":rent.reservation_id,
        "type":rent.type,
        "status":rent.status,
        "details":{
            "name":Court.objects(id=rent.details['court'])[0].name,
            "start":rent.details['start'],
            "end":rent.details['end']
        }
    } for rent in rent_now]
    return JsonResponse({
        "message":"ok",
        "courts":courts
    })
