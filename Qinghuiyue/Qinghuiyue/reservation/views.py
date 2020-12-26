import json
import datetime
from dateutil.parser import parse
from django.http import JsonResponse

from Qinghuiyue.feedback.models import Feedback
from Qinghuiyue.models.models import Stat
from Qinghuiyue.reservation.models import Reservation
from Qinghuiyue.share.models import Share_notification
from Qinghuiyue.users.models import User

from Qinghuiyue.venues.models import Court
from Qinghuiyue.utils import require


@require('get', online=True)
def get_reservations(request):
    '''
    获取用户当前预定信息
    :param request:

    '''
    user_id = int(request.GET['user_id'])
    user = User.objects(user_id=user_id)[0]
    rent_now_id = user.rent_now
    rent_now = Reservation.objects(id__in=rent_now_id).order_by("-reservation_id")
    courts = []
    for rent in rent_now:
        feedback = Feedback.objects(reservation_id=rent.reservation_id).first()
        if feedback:
            reviewed = feedback.feedback_id
        else:
            reviewed = 0
        share = Share_notification.objects(reservation=rent.id).first()
        if share:
            shared = share.share_id
        else:
            shared = 0
        try:
            court_name=Court.objects(id=rent.details['court'])[0].name
        except Exception:
            court_name="找不到场地信息"
        court = {
            "reservation_id": rent.reservation_id,
            "type": rent.type,
            "status": rent.status,
            "details": {
                "name": court_name,
                "start": rent.details['start'],
                "end": rent.details['end'],
                "created": rent.details['created']+datetime.timedelta(hours=8)
            },
            "reviewed": reviewed,
            "shared": shared
        }

        if rent.status == 2:
            court["details"]["paid_at"] = rent.details["paid_at"]+datetime.timedelta(hours=8)

        courts.append(court)
    return JsonResponse({
        "message": "ok",
        "courts": courts
    })


@require('post', online=True)
def book_draw(request):
    '''
    用户抽签预定
    params:user_id,court_id,start,end
    '''
    book_info = json.loads(request.body)
    court = Court.objects(court_id=book_info['court_id']).first()
    court_status = court.Status
    book_info['start'] = parse(book_info['start'])
    book_info['end'] = parse(book_info['end'])
    user = User.objects(user_id=request.session.get("user_id")).first()
    if not user:
        return JsonResponse({"message": "用户不存在"}, status=400)
    draw_now = Reservation.objects(id__in=user.rent_now, status=5).count()
    if draw_now >= 3:
        return JsonResponse({"message": "您最多同时参与三场抽签", "draw_now": draw_now}, status=400)
    for status in court_status:
        if status['start'] == book_info['start'] \
                and status['end'] == book_info['end']:
            if status['code'] == 3:  # 可供抽签
                if user.user_id in status['users_id']:
                    return JsonResponse({"message": "您已经预定过这个场地了"}, status=400)
                reservation = Reservation(type=court.enum_id, details={
                    "court": court.id,
                    "user_id": user.user_id,
                    "start": book_info["start"],
                    "end": book_info["end"],
                    "created": datetime.datetime.now()
                }, reservation_id=Stat.add_object("reservation"), status=5)  # 5是等待抽签
                reservation.save()  # 应该先保存，不然会导致读取不出id

                if 'reservation_ids' not in status.keys():
                    status['reservation_ids'] = []
                status['reservation_ids'].append(reservation.id)
                status['users_id'].append(user.user_id)
                user.rent_now.append(reservation.id)
                court.save()
                user.save()

                return JsonResponse({"message": "ok", "reservation_id": reservation.reservation_id})
    return JsonResponse({"message": "找不到需要预定的时间段"}, status=400)

@require('post',online=True)
def book_first_come(request):
    """
     先到先得预定，接受用户id和要预定的场馆和时间段
:
     """
    book_info = json.loads(request.body)
    print(book_info)
    court = Court.objects(court_id=book_info['court_id']).first()
    court_status = court.Status
    book_info['start'] = parse(book_info['start'])
    book_info['end'] = parse(book_info['end'])
    user = User.objects(user_id=request.session.get("user_id")).first()
    if not user:
        return JsonResponse({"message": "用户不存在或登陆过期，请重新登陆"}, status=400)

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
                    "end": book_info["end"],
                    "created": datetime.datetime.now()

                }, reservation_id=stat.data['reservation'] + 1, status=1)
                reservation.save()  # 应该先保存，不然会导致读取不出id
                stat.data['reservation'] += 1
                user.rent_now.append(reservation.id)

                court.save()
                user.save()
                stat.save()
                return JsonResponse({"message": "ok", "reservation_id": reservation.reservation_id})

    return JsonResponse({"message": "error"}, status=400)

@require('post',online=True)
def transfer_reservation(request):
    '''
    转让场地
    :param request:
    :return:
    '''

    # 是新建一个订单，原来的状态改为已经转移,只有已经预定成功（含未付款）才能转让
    params = json.loads(request.body)
    reservation = Reservation.objects(reservation_id=params['reservation_id']).first()
    if not reservation:
        return JsonResponse({"message": "找不到订单"}, status=400)
    if reservation.status not in [1, 2]:
        return JsonResponse({"message": "该订单不可转让"}, status=400)
    if reservation.details['start'] < datetime.datetime.now():
        return JsonResponse({"message": "该订单已经过期了"}, status=400)
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
    Share_notification.del_share(reservation.id)
    # 再到court里面去修改status,可能可以抽象成函数
    court = Court.objects(id=reservation.details['court']).first()
    for status in court.Status:
        if status['start'] == reservation.details['start'] and \
                status['end'] == reservation.details['end']:
            status['user_id'] = user_new.user_id
            break
    court.save()
    return JsonResponse({"message": "ok"})

@require('post',online=True)
def cancel_reservation(request):
    '''
    取消订单，把订单状态改为3，并且在场馆处修改状态。
    对于未付款(1)的，将对应场地状态制空，可供先到先得
    对于已付款的，认为不能取消了（退款功能没有实现，可以转让）
    对于未抽签(5)的，将其从队列里面删除
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
    court = Court.objects(id=reservation.details['court']).first()
    if reservation.status == 1:
        reservation.status = 3
        reservation.save()
        for status in court.Status:
            if status['start'] == reservation.details['start'] and \
                    status['end'] == reservation.details['end']:
                status['user_id'] = -1
                status['code'] = 1
                break
        court.save()
    elif reservation.status == 5:
        reservation.status = 3
        reservation.save()
        for status in court.Status:
            if status['start'] == reservation.details['start'] and \
                    status['end'] == reservation.details['end']:
                try:
                    status['reservation_ids'].remove(reservation.id)
                    status['users_id'].remove(user.user_id)
                except:
                    return JsonResponse({"message": "您已经从抽签中退出"}, status=400)
                break
        court.save()
    else:
        return JsonResponse({"message": "当前状态不可取消预定"}, status=400)

    Share_notification.del_share(reservation.id)
    return JsonResponse({"message": "ok"})

@require('post',online=True)
def pay_offline(request):
    '''
    线下支付
    '''
    params = json.loads(request.body)
    reservation = Reservation.objects(reservation_id=params['reservation_id']).first()
    # 只有存在的且为未支付的订单可以进入支付状态
    if not reservation:
        return JsonResponse({"message": "该订单不存在"}, status=500)
    if reservation.status != 1:
        return JsonResponse({"message": "该订单不可支付"}, status=401)
    if reservation.details['user_id']!=request.session.get('user_id'):
        return JsonResponse({"message":"这不是您的订单，请确认登陆信息"},status=403)
    court = Court.objects(id=reservation.details['court']).first()
    if not court:
        return JsonResponse({"message": "该场地不存在！"}, status=501)

    reservation.status = 2
    reservation.details['paid_at'] = datetime.datetime.now()
    reservation.details['mode_of_pay'] = "offline"
    reservation.details['price'] = court.price
    reservation.save()

    return JsonResponse({"message": "ok"})


def test_draw(request):
    '''仅用于手动测试抽签'''
    from Qinghuiyue.cronjobs.cronjobs import start_draw, set_court_next_week
    # set_court_next_week()
    start_draw()
    return JsonResponse({"message": "ok"})


def test_set(request):
    from Qinghuiyue.cronjobs.cronjobs import set_court_next_week
    set_court_next_week()
    return JsonResponse({"message": "ok"})
