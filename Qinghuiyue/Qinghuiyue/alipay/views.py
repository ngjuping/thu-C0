import json
import time
from urllib.parse import parse_qs
from datetime import datetime
from dateutil.parser import parse
from django.conf import settings
from django.shortcuts import render, redirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from Qinghuiyue.alipay.alipay import AliPay
from Qinghuiyue.reservation.models import Reservation
from Qinghuiyue.venus.models import Court
from Qinghuiyue.reservation.models import Reservation



def aliPay():
    obj = AliPay(
        appid="2021000116664022",  # 支付宝沙箱里面的APPI
        app_notify_url="http://58.87.86.11:8000/api/pay/update_order/",
        # 如果支付成功，支付宝会向这个地址发送POST请求（校验是否支付已经完成），此地址要能够在公网进行访问，需要改成你自己的服务器地址
        return_url="http://58.87.86.11:8000/api/pay/result/",  # 如果支付成功，重定向回到网站的地址。
        alipay_public_key_path=settings.ALIPAY_PUBLIC,  # 支付宝公钥
        app_private_key_path=settings.APP_PRIVATE,  # 应用私钥
        debug=True,  # 默认False,True表示使用沙箱环境测试
    )

    # 优化:在settings里面的设置后使用
    # obj = AliPay(
    #     appid=settings.APPID,
    #     app_notify_url=settings.NOTIFY_URL,
    #     return_url=settings.RETURN_URL,
    #     alipay_public_key_path=settings.PUB_KEY_PATH,
    #     app_private_key_path=settings.PRI_KEY_PATH,
    #     debug=True,
    # )
    return obj


@csrf_exempt
def index(request):
    # 假的index用于在没有前端的情况下测试2
    if request.method == "GET":
        return render(request, 'index.html')

    # 对购买的数据进行加密
    reservation_id = int(request.POST.get('reservation_id'))  # 保留俩位小数  前端传回的数据

    out_trade_no = str(reservation_id)  # 商户订单号   # 订单号可以有多中生成方式，可以百度一下

    reservation = Reservation.objects(reservation_id=reservation_id).first()
    if not reservation:
        return JsonResponse({"message": "该订单不存在！"}, status=500)
    # 1. 在数据库创建一条数据：状态（待支付）
    court = Court.objects(id=reservation.details['court']).first()
    if not court:
        return JsonResponse({"message": "该场地不存在！"}, status=501)
    # 实例化SDK里面的类AliPay
    alipay = aliPay()
    query_params = alipay.direct_pay(
        subject=court.name + "支付",  # 商品简单描述 这里一般是从前端传过来的数据
        out_trade_no=out_trade_no,  # 商户订单号  这里一般是从前端传过来的数据
        total_amount=court.price,  # 交易金额(单位: 元 保留俩位小数)   这里一般是从前端传过来的数据
        is_phone=1
    )
    # 拼接url，转到支付宝支付页面
    pay_url = "https://openapi.alipaydev.com/gateway.do?{}".format(query_params)
    response=JsonResponse({"message":"ok"},status=302)
    response["Location"]=pay_url
    return response


@csrf_exempt
def pay_for_reservation(request):
    params = json.loads(request.body)
    reservation = Reservation.objects(reservation_id=params['reservation_id']).first()
    # 只有存在的且为未支付的订单可以进入支付状态
    if not reservation:
        return JsonResponse({"message": "该订单不存在"}, status=500)

    if reservation.status != 1:
        return JsonResponse({"message": "该订单不可支付"}, status=401)

    court = Court.objects(id=reservation.details['court']).first()
    if not court:
        return JsonResponse({"message": "该场地不存在！"}, status=501)

    alipay = aliPay()

    out_trade_no = str(reservation.reservation_id)  # 商户订单号

    query_params = alipay.direct_pay(
        subject=court.name + "支付",  # 商品简单描述 这里一般是从前端传过来的数据
        out_trade_no=out_trade_no,  # 商户订单号  这里一般是从前端传过来的数据
        total_amount=court.price,  # 交易金额(单位: 元 保留俩位小数)   这里一般是从前端传过来的数据
        is_phone=params['isPhone'],
    )
    pay_url = "https://openapi.alipaydev.com/gateway.do?{}".format(query_params)
    response=JsonResponse({"message":"ok"},status=200)
    response["Location"]=pay_url
    return response



@csrf_exempt
def update_order(request):
    """
    支付成功后，支付宝向该地址发送的POST请求（用于修改订单状态）
    :param request:
    :return:
    """
    if request.method == 'POST':
        body_str = request.body.decode('utf-8')
        post_data = parse_qs(body_str)
        post_dict = {}
        for k, v in post_data.items():
            post_dict[k] = v[0]
        alipay = aliPay()
        sign = post_dict.pop('sign', None)
        status = alipay.verify(post_dict, sign)
        if status:
            # 根据订单号将数据库中的数据进行更新
            reservation = Reservation.objects(reservation_id=post_dict.get('out_trade_no')).first()
            reservation.status = 2
            reservation.details['paid_at'] = datetime.now()
            reservation.details['trade_no_alipay'] = post_dict.get('trade_no')
            reservation.details['price'] = float(post_dict.get('total_amount'))
            reservation.details['mode_of_pay'] = "alipay"
            reservation.save()

    return HttpResponse('success')  # 必须输出来告诉支付宝已经收到通知


@csrf_exempt
def pay_result(request):
    """
    支付完成后，跳转回的地址
    :param request:
    :return:
    """
    params = request.GET.dict()
    sign = params.pop('sign', None)

    alipay = aliPay()

    status = alipay.verify(params, sign)

    if status:
        return redirect("http://localhost:8081/manage")  # 之后换成支付成功/失败的页面
    return HttpResponse('支付失败')
