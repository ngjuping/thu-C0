from django.http import HttpResponse, JsonResponse
from Qinghuiyue.models.models import *


def get_notices(request):
    '''
    首页获取前三个通知
    :return:
    '''
    try:
        notices_raw = Notification.objects().order_by("-time")[:3]  # 排序且只取前三个
        notices = []
        # print(request.session['user_id'])
        for notice in notices_raw:
            notices.append({"id":notice.notice_id,"title": notice.title, "content": notice.content, "time": notice.time})

        return JsonResponse({
            "message": "ok",
            "notices": notices
        })
    except Exception:
        return HttpResponse(status=400)



