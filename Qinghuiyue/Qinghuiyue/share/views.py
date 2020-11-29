from Qinghuiyue.venus.models import *
from Qinghuiyue.users.models import User
from Qinghuiyue.share.models import *
from django.http import HttpResponse, JsonResponse
from Qinghuiyue.models.models import Reservation
import json

def get_share_notifications(request):
    '''
    获取所有拼场信息，按时间排，有分页
    :param request: page:int size:int
    :return:
    '''
    page=int(request.GET['page'])
    size=int(request.GET['size'])

    shares_all=Share_notification.objects().order_by("-time")
    total=len(shares_all)
    if page*size>total:
        shares_page = shares_all
    else:
        shares_page = shares_all[(page-1)*size:page*size]
    shares=[
        {
            "share_id":share.share_id,
            "content":share.content,
            "publish_time":share.time,
            "reservation":Reservation.get_reservation_info(share.reservation),
            "status":share.status
        } for share in shares_page
    ]

    return JsonResponse({"message":"ok","total":total,"shares":shares})

def create_share(request):
    '''
    创建拼场通知，一个成功订单才能对应一个拼场信息，必须检查，要检查用户session(还没实现
    :param request:
    :return:
    '''
    params = json.loads(request.body)
    ok,message=Share_notification.create(params)
    if ok:
        return JsonResponse(message)
    else:
        return JsonResponse(message,status=400)

def update_share(request):
    '''
    更新拼场通知，同时会更新拼场通知的时间,要检查用户session(还没实现
     :param request:
    :return:
    '''
    try:
        params = json.loads(request.body)
        share=Share_notification.objects(share_id=params['share_id']).first()
        share.content=params['content']
        share.time=datetime.datetime.now()
        share.save()
        return JsonResponse({"message":"ok"})
    except Exception:
        return JsonResponse({"message":"服务器内部错误"},status=500)

def delete_share(request):
    '''
    删除拼场，要检查用户session(还没实现
    :param request:
    :return:
    '''
    params = json.loads(request.body)
    share = Share_notification.objects(share_id=params['share_id']).first()
    user=User.objects(user_id=share.user_id).first()
    user.invitation.remove(share.id)
    user.save()
    share.delete()
    return JsonResponse({"message":"ok"})
