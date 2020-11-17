from django.http import HttpResponse, JsonResponse

from Qinghuiyue.models import *
from Qinghuiyue.models.models import *
from Qinghuiyue.models.models import Stat
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

def get_venues_info(request):
    '''
    获取场馆信息
    :return:
    '''
    venue_id=request.GET['id']
    venue=Venue.objects(venue_id=venue_id).first()
    courts=venue.courts
    notices_id=venue.notices
    feedbacks=Feedback.objects(court__in=courts).order_by("-time")
    if len(feedbacks):
        feedback=feedbacks[0]
        review={
                "content":feedback.content,
                "stars":feedback.stars,
                "time":feedback.time
            }
    else:
        review={}

    notices_raw=Notification.objects(id__in=notices_id).order_by("-time")[:3]
    notices = []
    for notice in notices_raw:
        notices.append({"title": notice.title, "content": notice.content, "time": notice.time})
    return JsonResponse({
        "message": "ok",
        "venue_info":{
            "name":venue.name,
            "intro":venue.intro,
            "img":venue.image,
            "review":review,
            "notices":notices
        }
    })