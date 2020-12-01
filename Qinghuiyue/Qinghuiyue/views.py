from django.http import HttpResponse, JsonResponse

from Qinghuiyue.models import *
from Qinghuiyue.models.models import *
from Qinghuiyue.models.models import Stat
from Qinghuiyue.users.models import User
from Qinghuiyue.venus.models import Court
import json
import datetime
from Qinghuiyue.utils.time import str2datetime
import dateutil.parser

def get_notices(request):
    '''
    首页获取前三个通知
    :return:
    '''
    try:
        notices_raw = Notification.objects().order_by("-time")[:3]  # 排序且只取前三个
        notices = []
        #print(request.session['user_id'])
        for notice in notices_raw:
            notices.append({"title": notice.title, "content": notice.content, "time": notice.time})

        return JsonResponse({
            "message": "ok",
            "notices": notices
        })
    except Exception:
        return HttpResponse(status=400)


def get_reservations(request):
    '''
    获取用户当前预定信息
    :param request:
    :return:
    '''
    #print(request.session.get('user_id'))
    user_id = request.GET['user_id']
    user = User.objects(user_id=user_id)[0]
    rent_now_id = user.rent_now
    rent_now = Reservation.objects(id__in=rent_now_id)
    #print(len(rent_now))
    #print(rent_now[0].details['court'])
    courts = [{
        "reservation_id": rent.reservation_id,
        "type": rent.type,
        "status": rent.status,
        "details": {
            "name": Court.objects(id=rent.details['court'])[0].name,
            "start": rent.details['start'],
            "end": rent.details['end']
        }
    } for rent in rent_now]
    return JsonResponse({
        "message": "ok",
        "courts": courts
    })


def book_first_come(request):
    '''
    先到先得预定，接受用户id和要预定的场馆和时间段
    :param request:
    :return:
    '''
    book_info = json.loads(request.body)
    print(book_info)
    court = Court.objects(court_id=book_info['court_id']).first()
    #print(court.name)
    court_status = court.Status
    #print(court_status)
    book_info['start'] = str2datetime(book_info['start'])

    book_info['end'] = str2datetime(book_info['end'])
    #print(book_info)
    print(request.session.get("user_id"))
    user = User.objects(user_id=request.session.get("user_id")).first()
    for status in court_status:
        #print(status['start'], status['end'])
        if status['start'] == book_info['start'] \
                and status['end'] == book_info['end']:
            if status['code'] == 1:  # 场地状态1，先到先得还能订此时用户就是第一个到的，时间段和场地状态都符合要求，直接预定成功
                status["user_id"] = user.user_id
                status["code"]=2#2是已经定了
                stat = Stat.objects(name="size_of_collection")[0]
                reservation = Reservation(type=court.enum_id, details={
                    "court": court.id,
                    "user_id": user.user_id,
                    "start": book_info["start"],
                    "end": book_info["end"]
                }, reservation_id=stat.data['reservation'] + 1, status=1)
                reservation.save()#应该先保存，不然会导致读取不出id
                stat.data['reservation'] += 1
                user.rent_now.append(reservation.id)

                court.save()
                user.save()
                stat.save()

                return JsonResponse({"message": "ok"})
    return JsonResponse({"message": "error"}, status=400)
