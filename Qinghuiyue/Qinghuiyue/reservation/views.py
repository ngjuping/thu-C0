import json

from django.http import JsonResponse

from Qinghuiyue.feedback.models import Feedback
from Qinghuiyue.models.models import Stat
from Qinghuiyue.reservation.models import Reservation
from Qinghuiyue.share.models import Share_notification
from Qinghuiyue.users.models import User
from Qinghuiyue.utils.time import str2datetime
from Qinghuiyue.venus.models import Court
import datetime

def get_reservations(request):
    '''
    获取用户当前预定信息
    :param request:
    :return:
    '''
    # print(request.session.get('user_id'))
    user_id = request.GET['user_id']
    user = User.objects(user_id=user_id)[0]
    rent_now_id = user.rent_now
    rent_now = Reservation.objects(id__in=rent_now_id)
    # print(len(rent_now))
    # print(rent_now[0].details['court'])
    '''
    courts = [{
        "reservation_id": rent.reservation_id,
        "type": rent.type,
        "status": rent.status,
        "details": {
            "name": Court.objects(id=rent.details['court'])[0].name,
            "start": rent.details['start'],
            "end": rent.details['end'],
            "created":rent.details['created'],
            "paid_at":rent.details['paid']
        }
    } for rent in rent_now]'''
    courts = []
    for rent in rent_now:
        feedback=Feedback.objects(reservation_id=rent.reservation_id).first()
        if feedback:
            reviewed=feedback.feedback_id
        else:
            reviewed=0

        share=Share_notification.objects(reservation=rent.id).first()
        if share:
            shared=share.share_id
        else:
            shared=0
        court = {
            "reservation_id": rent.reservation_id,
            "type": rent.type,
            "status": rent.status,
            "details": {
                "name": Court.objects(id=rent.details['court'])[0].name,
                "start": rent.details['start'],
                "end": rent.details['end'],
                "created": rent.details['created']
            },
            "reviewed":reviewed,
            "shared":shared
        }
        if rent.status==2:
            court["details"]["paid_at"]=rent.details["paid_at"]
        courts.append(court)
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
    # print(court.name)
    court_status = court.Status
    # print(court_status)
    book_info['start'] = str2datetime(book_info['start'])

    book_info['end'] = str2datetime(book_info['end'])
    # print(book_info)
    print(request.session.get("user_id"))
    user = User.objects(user_id=request.session.get("user_id")).first()
    for status in court_status:
        # print(status['start'], status['end'])
        if status['start'] == book_info['start'] \
                and status['end'] == book_info['end']:
            if status['code'] == 1:  # 场地状态1，先到先得还能订此时用户就是第一个到的，时间段和场地状态都符合要求，直接预定成功
                status["user_id"] = user.user_id
                status["code"] = 2  # 2是已经定了
                stat = Stat.objects(name="size_of_collection")[0]
                reservation = Reservation(type=court.enum_id, details={
                    "court": court.id,
                    "user_id": user.user_id,
                    "start": book_info["start"],
                    "end": book_info["end"]
                }, reservation_id=stat.data['reservation'] + 1, status=1)
                reservation.save()  # 应该先保存，不然会导致读取不出id
                stat.data['reservation'] += 1
                user.rent_now.append(reservation.id)

                court.save()
                user.save()
                stat.save()

                return JsonResponse({"message": "ok"})
    return JsonResponse({"message": "error"}, status=400)


def transfer_reservation(request):
    '''
    转让场地
    :param request:
    :return:
    '''
    # 疑问，是直接把订单转移，还是新建一个订单，原来的状态改为已经转移
    params = json.loads(request.body)
    reservation = Reservation.objects(reservation_id=params['reservation_id']).first()
    if not reservation:
        return JsonResponse({"message": "找不到订单"}, status=400)
    if reservation.status not in [1, 2]:
        return JsonResponse({"message": "该订单不可转让"}, status=400)
    if reservation.details['start']<datetime.datetime.now():
        return JsonResponse({"message": "该订单已经过期了"},status=400)
    user_now = User.objects(user_id=reservation.details['user_id']).first()
    if user_now.user_id != request.session.get('user_id'):
        return JsonResponse({"message": "你没有转移权限！"}, status=400)
    user_new = User.objects(user_id=params['new_user_id']).first()
    if not user_new:
        return JsonResponse({"message": "找不到目标用户"}, status=400)
    new_reservation = Reservation.objects.create(type=reservation.type, details=reservation.details,
                                                 reservation_id=Stat.add_object("reservation"),
                                                 status=reservation.status)

    new_reservation.details['user_id'] = user_new.user_id
    new_reservation.save()
    user_new.rent_now.append(new_reservation.id)
    reservation.status = 4
    user_new.save()
    user_now.save()
    reservation.save()
    # 再到court里面去修改status,可能可以抽象成函数
    court = Court.objects(id=reservation.details['court']).first()
    for status in court.Status:
        if status['start'] == reservation.details['start'] and \
                status['end'] == reservation.details['end']:
            status['user_id'] = user_new.user_id
            break
    court.save()
    return JsonResponse({"message": "ok"})


def cancel_reservation(request):
    '''
    取消订单，把订单状态改为3，并且在场馆处修改状态。当多种方式混合预定的时候再增加条件判断。
    :param request:
    :return:
    '''
    params = json.loads(request.body)
    reservation = Reservation.objects(reservation_id=params['reservation_id']).first()
    if not reservation:
        return JsonResponse({"message": "找不到订单"}, status=400)
    user = User.objects(user_id=reservation.details['user_id']).first()
    if user.user_id != request.session.get('user_id'):
        return JsonResponse({"message": "你没有取消权限！"}, status=400)

    reservation.status = 3
    reservation.save()
    court = Court.objects(id=reservation.details['court']).first()
    for status in court.Status:
        if status['start'] == reservation.details['start'] and \
                status['end'] == reservation.details['end']:
            status['user_id'] = -1
            status['code'] = 1
            break
    court.save()

    return JsonResponse({"message": "ok"})