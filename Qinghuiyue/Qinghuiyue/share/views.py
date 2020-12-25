import json
from django.http import HttpResponse, JsonResponse
from Qinghuiyue.share.models import *
from Qinghuiyue.reservation.models import Reservation

from Qinghuiyue.utils import require
from Qinghuiyue.checkers.html_content_checker import check_html_content

@require('get')
def get_share_notifications(request):
    '''
    获取所有拼场信息，按时间排，有分页
    :param request: page:int size:int
    '''
    page = int(request.GET['page'])
    size = int(request.GET['size'])

    shares_all = Share_notification.objects().order_by("-time")
    total = len(shares_all)
    if page * size > total:
        shares_page = shares_all
    else:
        shares_page = shares_all[(page - 1) * size:page * size]
    shares = [
        {
            "user_id": share.user_id,
            "share_id": share.share_id,
            "content": share.content,
            "publish_date": share.time,
            "reservation": Reservation.get_reservation_info(share.reservation),
            "status": share.status
        } for share in shares_page
    ]

    return JsonResponse({"message": "ok", "total": total, "shares": shares})


@require('get',online=True)
def get_user_shares(request):
    '''
    获取单个用户所有拼场
    :param request:
    :return:
    '''
    page = int(request.GET['page'])
    size = int(request.GET['size'])
    user_id = int(request.GET['user_id'])
    user = User.objects(user_id=user_id).first()
    if not user:
        return JsonResponse({"message": "找不到此用户"}, status=400)
    shares_all = Share_notification.objects(id__in=user.invitation).order_by("-time")
    total = len(shares_all)
    if page * size > total:
        shares_page = shares_all
    else:
        shares_page = shares_all[(page - 1) * size:page * size]
    shares = [
        {
            "user_id": share.user_id,
            "share_id": share.share_id,
            "content": share.content,
            "publish_date": share.time,
            "reservation": Reservation.get_reservation_info(share.reservation),
            "status": share.status
        } for share in shares_page
    ]
    return JsonResponse({"message": "ok", "total": total, "shares": shares})

@require('post',check_id=True)
def create_share(request):
    '''
    创建拼场通知，一个成功订单才能对应一个拼场信息，必须检查
    '''

    params = json.loads(request.body)
    ok,message=check_html_content(params['content'])
    if not ok:
        return JsonResponse({'message':message},status=400)

    ok, message = Share_notification.create(params)
    if ok:
        return JsonResponse(message)
    else:
        return JsonResponse(message, status=400)

@require('post',online=True)
def update_share(request):
    '''
    更新拼场通知，同时会更新拼场通知的时间
     :param request:
    :return:
    '''
    try:
        params = json.loads(request.body)
        share = Share_notification.objects(share_id=params['share_id']).first()
        if share.user_id!=request.session.get('user_id'):
            return JsonResponse({"message": "没有更改权限"}, status=403)
        ok, message = check_html_content(params['content'])
        if not ok:
            return JsonResponse({'message': message}, status=400)
        share.content = params['content']
        share.time = datetime.datetime.now()
        share.save()
        return JsonResponse({"message": "ok"})
    except Exception:
        return JsonResponse({"message": "服务器内部错误"}, status=500)

@require('post',online=True)
def delete_share(request):
    '''
    删除拼场
    '''
    params = json.loads(request.body)
    share = Share_notification.objects(share_id=params['share_id']).first()
    user = User.objects(user_id=share.user_id).first()
    if share.user_id != request.session.get('user_id'):
        return JsonResponse({"message": "没有更改权限"}, status=403)
    try:
        user.invitation.remove(share.id)
    except Exception:
        # 可能由于某些原因用户对这条记录没有引用，那么直接删除即可
        pass
    user.save()
    share.delete()
    return JsonResponse({"message": "ok"})
